import json
import re
import textblob as TextBlob
import json
import pandas as pd


# handle the import json from SQS
def lambda_handler(event, context):
  
  # create array to load json
  tweet_array_json = []
  # cycle each record from the event
  for record in event.records:
    
    # unpack the message body from the body
    message_body = json.loads(record['body'])
    
    # unpack the message from the message body
    message = json.loads(message_body['Message'])
    
    # load the message into the json array
    tweet_array_json.append(message)
    
  # create the data structure for the data_frame
  d = {'Tweet': [tweet.text for tweet in tweet_array_json], 
      'Re-Tweet Count': [tweet.retweet_count for tweet in tweet_array_json],
      'Favorite Count': [tweet.favorite_count for tweet in tweet_array_json],
      'Place': [tweet.place for tweet in tweet_array_json]
      }
  
  # create the data frame from the 
  data_frame = pd.DataFrame(data = d)
  
  #sort by retweet count
  dataFrame = dataFrame.sort_values(['Re-Tweet Count', 'Favorite Count'], ascending= False)
  
  # clean the tweets from the column 'Tweets
  dataFrame['Tweet'] = dataFrame['Tweet'].apply(textScrubber)

  # create two columns for subjectivity and polarity
  data_frame['Subjectivity'] = data_frame['Tweet'].apply(getSubjectivity)
  data_frame['Polarity'] = data_frame['Tweet'].apply(getPolarity)

  # create a new column for the analysis. This will be done in the database for the project. 
  data_frame['Analysis'] = data_frame['Polarity'].apply(getAnalysis)


  # store info in database
  
  # create API endpoint to send info/CRUD
  
  # return front end response (look up with API Gateway)

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
  
  # test gitHub set up