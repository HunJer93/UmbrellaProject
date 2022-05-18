import json

# test lambda to handle basic functions
def lambda_handler(event, context):
    records = event['Records']
    for item in records:
        body = json.loads(item["body"])
        value1 = body["key1"]
        stuff = { 'name': value1 } 
        print('hello: ' + value1)
        
    return {
        'statusCode': 200,
        'body': str(len(records)) + ' processed'
    }