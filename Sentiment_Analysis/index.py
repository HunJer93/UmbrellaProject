import json
from multiprocessing.connection import Client
import re
import textblob as TextBlob
import json
import pandas as pd
import boto3
import logging
from botocore.exceptions import ClientError

# global constants

# sqs client
SQS = boto3.client('sqs')
# logger (and configuration)
LOGGER = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

DYNAMO_CLIENT = boto3.client('dynamodb')

# handle the import json from SQS
def lambda_handler(event, context):
  
  # local host endpoint url for sqs
  SQS_LOCAL_HOST_ENDPOINT = 'http://localhost:4566/queue/sentiment-analysis-queue'
  
  # receive sqs queue
  messages = receive_queue_message(SQS_LOCAL_HOST_ENDPOINT)
  
  # create array to hold the incoming sqs messages
  tweet_array_json = []
  
  # cycle the messages and load into array
  for msg in messages['Messages']:
    msg_body = msg['body']
    receipt_handle = msg['ReceiptHandle']
    
    # log the message body for testing
    LOGGER.info(f'The message body: {msg_body}')
    
    # put the message contents into the array
    tweet_array_json.append(msg_body) 
   
  # ######################################################
  # Might need to edit the data from below....
  
  # create the data structure for the data_frame
  d = {'Tweet': [tweet.text for tweet in tweet_array_json], 
      'Re-Tweet Count': [tweet.retweet_count for tweet in tweet_array_json],
      'Favorite Count': [tweet.favorite_count for tweet in tweet_array_json],
      'Place': [tweet.place for tweet in tweet_array_json]
      }
  
  # create the data frame from the 
  data_frame = pd.DataFrame(data = d)
  
  #sort by retweet count
  data_frame = data_frame.sort_values(['Re-Tweet Count', 'Favorite Count'], ascending= False)
  
  # clean the tweets from the column 'Tweets
  data_frame['Tweet'] = data_frame['Tweet'].apply(textScrubber)

  # create two columns for subjectivity and polarity
  data_frame['Subjectivity'] = data_frame['Tweet'].apply(getSubjectivity)
  data_frame['Polarity'] = data_frame['Tweet'].apply(getPolarity)

  # create a new column for the analysis. This will be done in the database for the project. 
  data_frame['Analysis'] = data_frame['Polarity'].apply(getAnalysis)
  
  # send the data frame to export to dynamo
  export_to_dynamo(data_frame)
  
  return 0

  
# receive_queue_message retrieves messages from the SQS queue
def receive_queue_message(queue_url):
  try:
    response = SQS.receive_message(QueueUrl=queue_url)
  except ClientError:
    LOGGER.exception(
      f'Could not receive the message from - {queue_url}.')
    raise
  else:
    return response
  
# delete_queue_message deletes the queue message when the information is extracted
def delete_queue_message(queue_url,receipt_handle):
  try:
    response = SQS.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
  except ClientError:
    LOGGER.exception(f'Could not delete the message from - {queue_url}.')
    raise
  else:
    return response
  
# export_to_dynamo exports the data frame created to a dynamo DB
def export_to_dynamo(data_frame):

  # for each record within the data frame, load the payload
  for record in data_frame:
    # try to post the record to the database
    try:
      'POST'(DYNAMO_CLIENT, record)
    except Exception as e:
      LOGGER.error(e)
    else:
      LOGGER.error('Post to database failed for an unknown reason')
      
# clean the raw tweet info using a text scrubber method
def textScrubber(text):
  # use a regular expression to look for @ mentions 
  text = re.sub(r'@[A-Za-z0-9:]+', '', text)
  text = re.sub(r'#', '', text) #removing the '#' from the tweet
  text = re.sub(r'RT[\s]+', '', text) #removes any retweets 
  text = re.sub(r'https?:\/\/\S+', '', text) # remove any hyper link. \ escapes the / used in the hyper link, and S+ is looking for any white space after the //.
  
  # clean up the white space
  text = text.strip()
  return text

# Create a function to get the subjectivity (gets positive/negative words from text) using TextBlob
# in the project, this will be the sentiment analysis lambda expression
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity (how positive or negative the text is)
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

# Create a function to compute the negative, neutral, and positive analysis of the words within the tweets
# getAnalysis takes a score and returns if it is a negative sentiment, positive, or neutral
def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else: 
    return 'Positive'
  