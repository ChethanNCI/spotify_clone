import boto3
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

# Create SNS client

# Initialize SNS client
sns = boto3.client('sns')
# Create a new SNS topic
response = sns.create_topic(Name='MyTopic')
topic_arn = response['TopicArn']
print(f"Topic ARN: {topic_arn}")
# Subscribe an email address
response = sns.subscribe(
 TopicArn=topic_arn,
 Protocol='email',
 Endpoint='x23297395@student.ncirl.ie' # Replace with your email
)
print(f"Subscription ARN: {response['SubscriptionArn']}")


def send_registration_email(username, email):
    """
    Sends a registration success email using AWS SNS.
    """
    try:
        subject = "Successfully Registered to TuneStream"
        message = f"Hello Chethan,\n\n {username}, have successfully registered to TuneStream using the email {email}."
        
        # Publish message to SNS topic
        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
    except Exception as e:
        print(f"Error sending email via SNS: {e}")
