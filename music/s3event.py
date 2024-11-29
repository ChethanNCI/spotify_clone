import boto3
# Create SNS client

# Initialize SNS client
sns = boto3.client('sns', region_name='us-east-1')
# Create a new SNS topic
response = sns.create_topic(Name='s3trigger')
topic_arn = response['TopicArn']
print(f"Topic ARN: {topic_arn}")
# Subscribe an email address
response = sns.subscribe(
 TopicArn=topic_arn,
 Protocol='email',
 Endpoint='mpchethan584@gmail.com' # Replace with your email
)
print(f"Subscription ARN: {response['SubscriptionArn']}")