import boto3
from botocore.exceptions import ClientError

# Create SNS client
sns = boto3.client("sns", region_name="ap-south-1")

topic_name = "ImageLabelNotifications"
email = "akshitadabral17@gmail.com"  # Replace with your email

try:
    # Create SNS topic
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    print(f" SNS topic '{topic_name}' created. ARN: {topic_arn}")

    # Subscribe email
    sns.subscribe(
        TopicArn=topic_arn,
        Protocol="email",
        Endpoint=email
    )
    print(f"Subscription request sent to {email}. Check your inbox to confirm.")

except ClientError as e:
    print(f" Error creating SNS topic: {e}")
