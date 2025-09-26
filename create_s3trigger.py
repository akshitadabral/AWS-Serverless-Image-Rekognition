import boto3

s3 = boto3.client("s3", region_name="ap-south-1")
lambda_client = boto3.client("lambda", region_name="ap-south-1")

bucket_name = "image-upload-bucket-akshita"
lambda_name = "ProcessImageUpload"

# Get Lambda ARN
lambda_arn = lambda_client.get_function(FunctionName=lambda_name)["Configuration"]["FunctionArn"]

# Add permission for S3 to invoke Lambda
try:
    lambda_client.add_permission(
        FunctionName=lambda_name,
        StatementId="S3InvokeProcessImageUpload",
        Action="lambda:InvokeFunction",
        Principal="s3.amazonaws.com",
        SourceArn=f"arn:aws:s3:::{bucket_name}"
    )
    print("Permission added to Lambda for S3 trigger")
except lambda_client.exceptions.ResourceConflictException:
    print("Permission already exists")

# Configure S3 event notification
notification = {
    "LambdaFunctionConfigurations": [
        {
            "LambdaFunctionArn": lambda_arn,
            "Events": ["s3:ObjectCreated:*"]
        }
    ]
}

s3.put_bucket_notification_configuration(
    Bucket=bucket_name,
    NotificationConfiguration=notification
)

print(f" S3 bucket '{bucket_name}' is now configured to trigger Lambda '{lambda_name}' on upload")
