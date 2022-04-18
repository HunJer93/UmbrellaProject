import index
import pytest

# when textScrubber is called, people tagged with @ will be removed
def test_textScrubber_remove_at_mention():
    text = '@TestPerson check this out!'
    
    assert index.textScrubber(text) == 'check this out!'
    
# when textScrubber is called, # will be removed 
def test_textScrubber_remove_hashtag():
    text = '@TestPerson check this out! #thisisneat #wow'
    
    assert index.textScrubber(text) == 'check this out! thisisneat wow'
    
# when textScrubber is called, Retweets with RT will be removed
def test_textScrubber_remove_Retweet():
    text = 'RT@TestPerson check this out! #thisisneat #wow'
    
    assert index.textScrubber(text) == 'check this out! thisisneat wow'
    
# when textScrubber is called, any hyperlinks are removed
def test_textScrubber_remove_hyperlink():
    text = 'RT@TestPerson check this out! #thisisneat #wow https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    
    assert index.textScrubber(text) == 'check this out! thisisneat wow'
    
# when a payload is sent to the lambda_handler, it processes the payload
def test_lambda_handler():
    # dummy event
    event = {
    "resource": "/",
    "path": "/",
    "httpMethod": "GET",
    "requestContext": {
        "resourcePath": "/",
        "httpMethod": "GET",
        "path": "/Prod/",
    },
    "headers": {
        "accept": "text/html",
        "accept-encoding": "gzip, deflate, br",
        "Host": "xxx.us-east-2.amazonaws.com",
        "User-Agent": "Mozilla/5.0",
    },
    "multiValueHeaders": {
        "accept": [
            "text/html"
        ],
        "accept-encoding": [
            "gzip, deflate, br"
        ],
    },
    "queryStringParameters": {
        "postcode": 12345
        },
    "multiValueQueryStringParameters": "NULL",
    "pathParameters": "NULL",
    "stageVariables": "NULL",
    "body": {
        "Message": {
        'Query': 'Michael Bolton, Lonely Island',
        'Num_Tweets' : 10
    }},
    "isBase64Encoded": "False"
    }
    
    context = " "
    response = 200
    actual = index.lambda_handler(event, context)['ResponseMetadata']['HTTPStatusCode']
    assert  actual == response