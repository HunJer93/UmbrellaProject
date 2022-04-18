#!/bin/bash
echo "Configuring localstack components... Please hold."
set -x
#creation of resources using cloud templates
# set up SQS for scraper lambda
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name twitter-scraper-queue

# set up SQS for sentiment analysis lambda
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name sentiment-analysis-queue


# create TwitterScraper Lambda Function
aws --endpoint-url=http://localhost:4566 \
lambda create-function --function-name twitter-scraper \
--zip-file fileb://twitter-scraper.zip \
--handler index.lambda_handler --runtime python3.8 \
--role arn:aws:iam::000000000000:role/lambda-role 

# bind twitter-scraper-queue SQS to TwitterScraper Lambda
aws --endpoint-url=http://localhost:4566 lambda create-event-source-mapping --function-name twitter-scraper --batch-size 1 --event-source-arn arn:aws:sqs:us-east-1:000000000000:twitter-scraper-queue

# create SentimentAnalysis Lambda Function
aws --endpoint-url=http://localhost:4566 \
lambda create-function --function-name sentiment-analysis \
--zip-file fileb://sentiment-analysis.zip \
--handler index.lambda_handler --runtime python3.8 \
--role arn:aws:iam::000000000000:role/lambda-role

# bind sentiment-analysis-queue SQS to sentiment-analysis Lambda
aws --endpoint-url=http://localhost:4566 lambda create-event-source-mapping --function-name sentiment-analysis --batch-size 1 --event-source-arn arn:aws:sqs:us-east-1:000000000000:sentiment-analysis-queue

# manually send a message to the twitter-scraper-queue
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url  http://localhost:4566/000000000000/twitter-scraper-queue --message-body 'this is a message test for scraper'



set +x

