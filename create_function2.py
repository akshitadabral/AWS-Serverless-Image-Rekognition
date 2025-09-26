import boto3
import io
import zipfile

lambda_client = boto3.client('lambda', region_name='ap-south-1')
iam_client = boto3.client('iam')

function_name = "ProcessImageUpload"
role_name = "urlrole"

# Get role ARN
role_arn = iam_client.get_role(RoleName=role_name)['Role']['Arn']

lambda_code_str = """import boto3
from datetime import datetime

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

table = dynamodb.Table('ImageLabels')
sns_topic_arn = 'arn:aws:sns:ap-south-1:985539786698:ImageLabelNotifications'

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key}},
        MaxLabels=10,
        MinConfidence=80
    )
    labels = [label['Name'] for label in response['Labels']]

    table.put_item(Item={
        'ImageKey': key,
        'Labels': labels,
        'UploadTime': datetime.utcnow().isoformat()
    })

    sns.publish(
        TopicArn=sns_topic_arn,
        Message=f"Labels detected for {key}: {', '.join(labels)}"
    )

    return {'statusCode': 200, 'body': f"Processed {key} successfully"}
"""

# Create in-memory zip
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('process_image_upload.py', lambda_code_str)

zip_buffer.seek(0)

# Create Lambda function
try:
    lambda_client.get_function(FunctionName=function_name)
    print(f"Lambda function '{function_name}' already exists")
except lambda_client.exceptions.ResourceNotFoundException:
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.11',
        Role=role_arn,
        Handler='process_image_upload.lambda_handler',  # matches file inside zip
        Code={'ZipFile': zip_buffer.read()},
        Timeout=15,
        MemorySize=128,
        Publish=True
    )
    print(f"Lambda function '{function_name}' created successfully")
