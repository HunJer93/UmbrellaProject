from urllib import response
from aiohttp import ClientError
import boto3

def get_analysis(query_id, query_subject,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
    
    table = dynamodb.Table('SentimentAnalysis')
    
    # try to get from the database 
    try:
        response = table.get_item(Key={'query_id': query_id, 'query_subject': query_subject})
    
    except ClientError as e:
        print(e.response['Error']['Message'])
        
    else:
        return response['Item']
    
if __name__ == '__main__':
    analysis = get_analysis(123456, "Twitter")
    if analysis:
        print("Get analysis succeeded:")
