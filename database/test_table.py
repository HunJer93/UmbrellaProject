from pprint import pprint
import unittest
import boto3 # AWS SDK for Python
from botocore.exceptions import ClientError
from moto import mock_dynamodb2 # since we're going to mock DynamoDB service

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
        
        result = put_sentiment_analysis(123456, "Twitter",
            "{\"Tweet\":{\"9\":\"LET'STALKABOUTTHESYNCHRONIZATION??\",\"7\":\"Hmm\\u2026IvotedforBidenandneverneededabumperstickeroryardsign?Anyoneelse,raiseyouhand?\\ud83d\\ude4b\\ud83c\\udffb\\u200d\\u2640\\ufe0f\",\"5\":\"JustRetweetDon'tAskWhy\\u2764\\ufe0f\\n\\n\\u0627\\u0645\\u067e\\u0648\\u0631\\u0679\\u0688_\\u062d\\u06a9\\u0648\\u0645\\u062a_\\u0646\\u0627\\u0645\\u0646\\u0638\\u0648\\u0631\\nIamImranKhan\\nImranKhanLIVE\\nTwitterTakeover\",\"2\":\"So...Imadethisartforatransfriendyearsago.Butit'sprobablyacopyrightissue.However,ifanyonewantstomakethei\\u2026\",\"6\":\"SupermanandLoisnewcomic,Ilovethispanel.SupermanAndLois\",\"0\":\"_Shayan08:KKing!AfterbreakingTwitterworldrecordinjust10minutes!\\n\\u0627\\u0645\\u067e\\u0648\\u0631\\u0679\\u0688_\\u062d\\u06a9\\u0648\\u0645\\u062a_\\u0646\\u0627\\u0645\\u0646\\u0638\\u0648\\u0631\",\"8\":\"[\\ud83c\\udfacinthelab247|Instagram]\\n\\\"\\ud83d\\udc9c\\\"\\n\\ud83d\\udd17\\n\\nBTS\\ubc29\\ud0c4\\uc18c\\ub144\\ub2e8JiminJungKook_twt\",\"4\":\"_Asiff:Itneghorsetomeredostonekbhyonlinelecturesnahisunehayjitneghorseaajkhankosunrahete\\ud83d\\ude02\\u2665\\ufe0f\\nFantkoffkrdi\\u2026\",\"3\":\"ElonMuskhasanarmyoftwitterbotstoexaggeratepopularitybecausehewantstobetheKarlRoveofTwitter.\\n\\n\",\"1\":\"Isthatwhatudolookuppeoplesusernamestoseeiftheyhavesocialmedia\\ud83d\\ude05whatin\\u2026\"},\"Re-TweetCount\":{\"9\":9418,\"7\":2157,\"5\":561,\"2\":184,\"6\":90,\"0\":72,\"8\":37,\"4\":16,\"3\":1,\"1\":0},\"FavoriteCount\":{\"9\":0,\"7\":0,\"5\":0,\"2\":0,\"6\":0,\"0\":0,\"8\":0,\"4\":0,\"3\":0,\"1\":0},\"Geo\":{\"9\":null,\"7\":null,\"5\":null,\"2\":null,\"6\":null,\"0\":null,\"8\":null,\"4\":null,\"3\":null,\"1\":null},\"Subjectivity\":{\"9\":0.0,\"7\":0.0,\"5\":0.0,\"2\":0.1,\"6\":0.5181818182,\"0\":0.0,\"8\":0.0,\"4\":0.5,\"3\":0.1,\"1\":0.0666666667},\"Polarity\":{\"9\":0.0,\"7\":0.0,\"5\":0.0,\"2\":0.2,\"6\":0.2954545455,\"0\":0.0,\"8\":0.0,\"4\":-0.5,\"3\":0.2,\"1\":0.0333333333}}",
             self.dynamodb)
        
        self.assertEqual(200, result['ResponseMetadata']['HTTPStatusCode'])
        
    # test if the get request works successfully
    def test_get_analysis(self):
        from put_analysis import put_sentiment_analysis
        from get_analysis import get_analysis
        
        # put the data into the test db
        put_sentiment_analysis(123456, "Twitter",
            "{\"Tweet\":{\"9\":\"LET'STALKABOUTTHESYNCHRONIZATION??\",\"7\":\"Hmm\\u2026IvotedforBidenandneverneededabumperstickeroryardsign?Anyoneelse,raiseyouhand?\\ud83d\\ude4b\\ud83c\\udffb\\u200d\\u2640\\ufe0f\",\"5\":\"JustRetweetDon'tAskWhy\\u2764\\ufe0f\\n\\n\\u0627\\u0645\\u067e\\u0648\\u0631\\u0679\\u0688_\\u062d\\u06a9\\u0648\\u0645\\u062a_\\u0646\\u0627\\u0645\\u0646\\u0638\\u0648\\u0631\\nIamImranKhan\\nImranKhanLIVE\\nTwitterTakeover\",\"2\":\"So...Imadethisartforatransfriendyearsago.Butit'sprobablyacopyrightissue.However,ifanyonewantstomakethei\\u2026\",\"6\":\"SupermanandLoisnewcomic,Ilovethispanel.SupermanAndLois\",\"0\":\"_Shayan08:KKing!AfterbreakingTwitterworldrecordinjust10minutes!\\n\\u0627\\u0645\\u067e\\u0648\\u0631\\u0679\\u0688_\\u062d\\u06a9\\u0648\\u0645\\u062a_\\u0646\\u0627\\u0645\\u0646\\u0638\\u0648\\u0631\",\"8\":\"[\\ud83c\\udfacinthelab247|Instagram]\\n\\\"\\ud83d\\udc9c\\\"\\n\\ud83d\\udd17\\n\\nBTS\\ubc29\\ud0c4\\uc18c\\ub144\\ub2e8JiminJungKook_twt\",\"4\":\"_Asiff:Itneghorsetomeredostonekbhyonlinelecturesnahisunehayjitneghorseaajkhankosunrahete\\ud83d\\ude02\\u2665\\ufe0f\\nFantkoffkrdi\\u2026\",\"3\":\"ElonMuskhasanarmyoftwitterbotstoexaggeratepopularitybecausehewantstobetheKarlRoveofTwitter.\\n\\n\",\"1\":\"Isthatwhatudolookuppeoplesusernamestoseeiftheyhavesocialmedia\\ud83d\\ude05whatin\\u2026\"},\"Re-TweetCount\":{\"9\":9418,\"7\":2157,\"5\":561,\"2\":184,\"6\":90,\"0\":72,\"8\":37,\"4\":16,\"3\":1,\"1\":0},\"FavoriteCount\":{\"9\":0,\"7\":0,\"5\":0,\"2\":0,\"6\":0,\"0\":0,\"8\":0,\"4\":0,\"3\":0,\"1\":0},\"Geo\":{\"9\":null,\"7\":null,\"5\":null,\"2\":null,\"6\":null,\"0\":null,\"8\":null,\"4\":null,\"3\":null,\"1\":null},\"Subjectivity\":{\"9\":0.0,\"7\":0.0,\"5\":0.0,\"2\":0.1,\"6\":0.5181818182,\"0\":0.0,\"8\":0.0,\"4\":0.5,\"3\":0.1,\"1\":0.0666666667},\"Polarity\":{\"9\":0.0,\"7\":0.0,\"5\":0.0,\"2\":0.2,\"6\":0.2954545455,\"0\":0.0,\"8\":0.0,\"4\":-0.5,\"3\":0.2,\"1\":0.0333333333}}",
             self.dynamodb)
        
        # get the data from the test db
        result = get_analysis(123456, "Twitter", self.dynamodb)
        
        # test the results
        self.assertEqual(123456, result['query_id'])
        self.assertEqual("Twitter", result['query_subject'])
        self.assertEqual("{\"Tweet\":{\"9\":\"LET'STALKABOUTTHESYNCHRONIZATION??\",\"7\":\"Hmm\\u2026IvotedforBidenandneverneededabumperstickeroryardsign?Anyoneelse,raiseyouhand?\\ud83d\\ude4b\\ud83c\\udffb\\u200d\\u2640\\ufe0f\",\"5\":\"JustRetweetDon'tAskWhy\\u2764\\ufe0f\\n\\n\\u0627\\u0645\\u067e\\u0648\\u0631\\u0679\\u0688_\\u062d\\u06a9\\u0648\\u0645\\u062a_\\u0646\\u0627\\u0645\\u0646\\u0638\\u0648\\u0631\\nIamImranKhan\\nImranKhanLIVE\\nTwitterTakeover\",\"2\":\"So...Imadethisartforatransfriendyearsago.Butit'sprobablyacopyrightissue.However,ifanyonewantstomakethei\\u2026\",\"6\":\"SupermanandLoisnewcomic,Ilovethispanel.SupermanAndLois\",\"0\":\"_Shayan08:KKing!AfterbreakingTwitterworldrecordinjust10minutes!\\n\\u0627\\u0645\\u067e\\u0648\\u0631\\u0679\\u0688_\\u062d\\u06a9\\u0648\\u0645\\u062a_\\u0646\\u0627\\u0645\\u0646\\u0638\\u0648\\u0631\",\"8\":\"[\\ud83c\\udfacinthelab247|Instagram]\\n\\\"\\ud83d\\udc9c\\\"\\n\\ud83d\\udd17\\n\\nBTS\\ubc29\\ud0c4\\uc18c\\ub144\\ub2e8JiminJungKook_twt\",\"4\":\"_Asiff:Itneghorsetomeredostonekbhyonlinelecturesnahisunehayjitneghorseaajkhankosunrahete\\ud83d\\ude02\\u2665\\ufe0f\\nFantkoffkrdi\\u2026\",\"3\":\"ElonMuskhasanarmyoftwitterbotstoexaggeratepopularitybecausehewantstobetheKarlRoveofTwitter.\\n\\n\",\"1\":\"Isthatwhatudolookuppeoplesusernamestoseeiftheyhavesocialmedia\\ud83d\\ude05whatin\\u2026\"},\"Re-TweetCount\":{\"9\":9418,\"7\":2157,\"5\":561,\"2\":184,\"6\":90,\"0\":72,\"8\":37,\"4\":16,\"3\":1,\"1\":0},\"FavoriteCount\":{\"9\":0,\"7\":0,\"5\":0,\"2\":0,\"6\":0,\"0\":0,\"8\":0,\"4\":0,\"3\":0,\"1\":0},\"Geo\":{\"9\":null,\"7\":null,\"5\":null,\"2\":null,\"6\":null,\"0\":null,\"8\":null,\"4\":null,\"3\":null,\"1\":null},\"Subjectivity\":{\"9\":0.0,\"7\":0.0,\"5\":0.0,\"2\":0.1,\"6\":0.5181818182,\"0\":0.0,\"8\":0.0,\"4\":0.5,\"3\":0.1,\"1\":0.0666666667},\"Polarity\":{\"9\":0.0,\"7\":0.0,\"5\":0.0,\"2\":0.2,\"6\":0.2954545455,\"0\":0.0,\"8\":0.0,\"4\":-0.5,\"3\":0.2,\"1\":0.0333333333}}",
                         result['raw_analysis'])

if __name__ == '__main__':
    unittest.main()
    
