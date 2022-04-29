from email import message
import json
from multiprocessing.connection import Client
from pyexpat.errors import messages
import re
from regex import D
from textblob import TextBlob
import json
import pandas as pd
import boto3
import logging
import decimal
from botocore.exceptions import ClientError
from collections import defaultdict

# global constants

# sqs client (endpoint over ride for local host)
SQS = boto3.client('sqs', endpoint_url='http://localhost:4566')
# logger (and configuration)
LOGGER = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

# dynamo client (endpoint over ride for local host)
DYNAMO_CLIENT = boto3.client('dynamodb', endpoint_url='http://localhost:4566')


# handle the import json from SQS
def lambda_handler(event, context):
  
  # local host endpoint url for sqs
  SQS_LOCAL_HOST_ENDPOINT = 'http://localhost:4566/queue/sentiment-analysis-queue'
  
  # unpackage message payload
  messages = event['Records']['body']['Message']
    
  # create the data structure for the data_frame
  d = {'Text': [tweet['text'] for tweet in messages], 
      'Re-Tweet Count': [tweet['retweet_count']for tweet in messages],
      'Favorite Count': [tweet['favorite_count'] for tweet in messages]
      }
  
  # create the data frame from the 
  data_frame = pd.DataFrame(data = d)
  
  #sort by retweet count
  data_frame = data_frame.sort_values(['Re-Tweet Count', 'Favorite Count'], ascending= False)
  
  # clean the tweets from the column 'Tweets
  data_frame['Text'] = data_frame['Text'].apply(textScrubber)

  # create two columns for subjectivity and polarity
  data_frame['Subjectivity'] = data_frame['Text'].apply(getSubjectivity)
  data_frame['Polarity'] = data_frame['Text'].apply(getPolarity)

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

# export_to_dynamo exports the data frame created to a dynamo DB
def export_to_dynamo(data_frame):

  payload = {}
  # for each record within the data frame, load the payload
  # amazon needs the payload in a dictionary form with each data type having a key of S for string or N for number
  # each value must also be converted to a string
  for record in data_frame.itertuples(index=False, name=None):
    payload['Text']={'S': record[0]}
    payload['Re-Tweet Count']={'N': str(record[1])}
    payload['Favorite Count']={'N': str(record[2])}
    payload['Subjectivity']={'N': str(record[3])}
    payload['Polarity']={'N': str(record[4])}
    payload['Analysis']={'S': str(record[5])}
    
    try:

      DYNAMO_CLIENT.put_item(Item=payload,TableName='SentimentAnalysis')
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
  text = re.sub(r'\n', ' ', text) # removes next lines
  
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
  
def Convert(tup, di):
  for a, b in tup:
    di.setdefault(a,[]).append(b)
  return di
  

  