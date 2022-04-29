from decimal import Decimal
from pprint import pprint
import unittest
import json
import boto3 # AWS SDK for Python
from botocore.exceptions import ClientError
from moto import mock_dynamodb2
from database.get_analysis import get_analysis

from database.put_analysis import put_sentiment_analysis # since we're going to mock DynamoDB service

@mock_dynamodb2
class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        #Create database resource and mock table
        
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # import table here so it uses the mock dynamodb instead of "real" one
        from create_table import create_sentiment_table
        self.table = create_sentiment_table(self.dynamodb)

    def tearDown(self):
        #Delete database resource and mock table
        
        self.table.delete()
        self.dynamodb=None

        pass
    
    def test_table_exists(self):
        #Test if our mock table is ready
        
        def test_table_exists(self):
            self.assertIn('SentimentAnalysis', self.table.name)
            
    def test_put_analysis(self):
        from put_analysis import put_sentiment_analysis
        
        # define payload
        payload = {"Tweet":{"9":"LET'S TALK ABOUT THE SYNCHRONIZATION?? ","7":"Hmm\u2026I voted for Biden and never needed a bumper sticker or yard sign? Anyone else, raise you hand? \ud83d\ude4b\ud83c\udffb\u200d\u2640\ufe0f ","5":"Just Retweet Don't Ask Why \u2764\ufe0f\n\n\u0627\u0645\u067e\u0648\u0631\u0679\u0688_\u062d\u06a9\u0648\u0645\u062a_\u0646\u0627\u0645\u0646\u0638\u0648\u0631 \nIamImranKhan\nImranKhanLIVE\nTwitterTakeover ","2":"So... I made this art for a trans friend years ago. But it's probably a copyright issue. However, if anyone wants to make thei\u2026","6":"Superman and Lois new comic, I love this panel. SupermanAndLois ","0":"_Shayan08: KKing! After breaking Twitter world record in just 10 minutes!\n\u0627\u0645\u067e\u0648\u0631\u0679\u0688_\u062d\u06a9\u0648\u0645\u062a_\u0646\u0627\u0645\u0646\u0638\u0648\u0631 ","8":"[\ud83c\udfac inthelab247 | Instagram]\n\"\ud83d\udc9c\"\n\ud83d\udd17 \n\nBTS \ubc29\ud0c4\uc18c\ub144\ub2e8 Jimin JungKook _twt ","4":"_Asiff: Itne ghor se to mere dosto ne kbhy online lectures nahi sune hay jitne ghor se aaj khan ko sun rahe te \ud83d\ude02\u2665\ufe0f\nFan tk off kr di\u2026","3":"Elon Musk has an army of twitter bots to exaggerate popularity because he wants to be the Karl Rove of Twitter.\n\n","1":"  Is that what u do look up peoples usernames to see if they have social media \ud83d\ude05 what in\u2026 "},"Re-Tweet Count":{"9":9418,"7":2157,"5":561,"2":184,"6":90,"0":72,"8":37,"4":16,"3":1,"1":0},"Favorite Count":{"9":0,"7":0,"5":0,"2":0,"6":0,"0":0,"8":0,"4":0,"3":0,"1":0},"Subjectivity":{"9":0.0,"7":0.0,"5":0.0,"2":0.1,"6":0.5181818182,"0":0.0,"8":0.0,"4":0.5,"3":0.1,"1":0.0666666667},"Polarity":{"9":0.0,"7":0.0,"5":0.0,"2":0.2,"6":0.2954545455,"0":0.0,"8":0.0,"4":-0.5,"3":0.2,"1":0.0333333333}}
        
        # convert payload to decimal (the payload will come formatted already from SentimentAnalysis.py)
        payload = json.loads(json.dumps(payload), parse_float=Decimal)
        result = put_sentiment_analysis(123456, "Twitter", payload, self.dynamodb)
        
        self.assertEqual(200, result['ResponseMetadata']['HTTPStatusCode'])
        
    # test table with a given payload  
    # keep for now but look into testing actual payload  
    # def test_put_with_payload(self, payload):
    #     # get the put result
    #     put_result = put_sentiment_analysis(123456, "TestName", payload, self.dynamodb)
        
    #     return self.assertEqual(200, put_result['ResponseMetadata']['HTTPStatusCode'])
    
    # def test_get_with_payload(self, payload):
        
    #     put_sentiment_analysis(123456, "TestName", payload, self.dynamodb)
    #     get_result = get_analysis(123456, "TestName", self.dynamodb)
        
    #     return self.assertEqual(get_result, payload)
        
        
        
    # test if the get request works successfully
    def test_get_analysis(self):
        from put_analysis import put_sentiment_analysis
        from get_analysis import get_analysis
        
        # define payload
        payload = {"Tweet":{"9":"LET'S TALK ABOUT THE SYNCHRONIZATION?? ","7":"Hmm\u2026I voted for Biden and never needed a bumper sticker or yard sign? Anyone else, raise you hand? \ud83d\ude4b\ud83c\udffb\u200d\u2640\ufe0f ","5":"Just Retweet Don't Ask Why \u2764\ufe0f\n\n\u0627\u0645\u067e\u0648\u0631\u0679\u0688_\u062d\u06a9\u0648\u0645\u062a_\u0646\u0627\u0645\u0646\u0638\u0648\u0631 \nIamImranKhan\nImranKhanLIVE\nTwitterTakeover ","2":"So... I made this art for a trans friend years ago. But it's probably a copyright issue. However, if anyone wants to make thei\u2026","6":"Superman and Lois new comic, I love this panel. SupermanAndLois ","0":"_Shayan08: KKing! After breaking Twitter world record in just 10 minutes!\n\u0627\u0645\u067e\u0648\u0631\u0679\u0688_\u062d\u06a9\u0648\u0645\u062a_\u0646\u0627\u0645\u0646\u0638\u0648\u0631 ","8":"[\ud83c\udfac inthelab247 | Instagram]\n\"\ud83d\udc9c\"\n\ud83d\udd17 \n\nBTS \ubc29\ud0c4\uc18c\ub144\ub2e8 Jimin JungKook _twt ","4":"_Asiff: Itne ghor se to mere dosto ne kbhy online lectures nahi sune hay jitne ghor se aaj khan ko sun rahe te \ud83d\ude02\u2665\ufe0f\nFan tk off kr di\u2026","3":"Elon Musk has an army of twitter bots to exaggerate popularity because he wants to be the Karl Rove of Twitter.\n\n","1":"  Is that what u do look up peoples usernames to see if they have social media \ud83d\ude05 what in\u2026 "},"Re-Tweet Count":{"9":9418,"7":2157,"5":561,"2":184,"6":90,"0":72,"8":37,"4":16,"3":1,"1":0},"Favorite Count":{"9":0,"7":0,"5":0,"2":0,"6":0,"0":0,"8":0,"4":0,"3":0,"1":0},"Subjectivity":{"9":0.0,"7":0.0,"5":0.0,"2":0.1,"6":0.5181818182,"0":0.0,"8":0.0,"4":0.5,"3":0.1,"1":0.0666666667},"Polarity":{"9":0.0,"7":0.0,"5":0.0,"2":0.2,"6":0.2954545455,"0":0.0,"8":0.0,"4":-0.5,"3":0.2,"1":0.0333333333}}
        
        # convert payload to decimal (the payload will come formatted already from SentimentAnalysis.py)
        payload = json.loads(json.dumps(payload), parse_float=Decimal)
        # put the data into the test db
        put_sentiment_analysis(123456, "Twitter",payload, self.dynamodb)
        
        # get the data from the test db
        result = get_analysis(123456, "Twitter", self.dynamodb)
        
        # test the results
        self.assertEqual(123456, result['query_id'])
        self.assertEqual("Twitter", result['query_subject'])
        self.assertEqual(payload, result['raw_analysis'])

if __name__ == '__main__':
    unittest.main()
    
