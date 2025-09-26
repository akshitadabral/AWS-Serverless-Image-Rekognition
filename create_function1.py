import boto3
import json
import zipfile
import os
import time
from botocore.exceptions import ClientError

# ------------------------
# CONFIGURATION
# ------------------------
role_name = "urlrole"  
function_name = "GenerateUploadURL"
bucket_name = "image-upload-bucket-akshita"
region = "ap-south-1"
lambda_file_name = "generate_upload_url.zip"  # Temporary zip for Lambda code

# ------------------------
# LAMBDA FUNCTION CODE
# ------------------------
lambda_code = """
import json
import boto3

s3_client = boto3.client('s3')
bucket_name = '{}'

def lambda_handler(event, context):
    print("Received event:", event)

    try:
        # Handle JSON body from API Gateway
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        file_name = body.get("fileName")
        if not file_name:
            return {{
                "statusCode": 400,
                "headers": {{
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }},
                "body": json.dumps({{"message": "fileName missing"}})
            }}

        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={{'Bucket': bucket_name, 'Key': file_name}},
            ExpiresIn=3600
        )

        return {{
            "statusCode": 200,
            "headers": {{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }},
            "body": json.dumps({{"uploadUrl": presigned_url}})
        }}

    except Exception as e:
        return {{
            "statusCode": 500,
            "headers": {{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }},
            "body": json.dumps({{"message": str(e)}})
        }}
""".format(bucket_name)

# ------------------------
# VERIFY IAM ROLE EXISTS
# ------------------------
iam_client = boto3.client("iam")

try:
    role = iam_client.get_role(RoleName=role_name)
    print(f"Using existing role '{role_name}' with ARN: {role['Role']['Arn']}")
except iam_client.exceptions.NoSuchEntityException:
    raise Exception(f"The IAM role '{role_name}' does not exist. Please create it first.")

# Wait a few seconds in case the role was just created
time.sleep(5)

# ------------------------
# WRITE LAMBDA CODE TO FILE AND ZIP
# ------------------------
with open("lambda_function.py", "w") as f:
    f.write(lambda_code)

with zipfile.ZipFile(lambda_file_name, 'w') as zipf:
    zipf.write("lambda_function.py")

# ------------------------
# CREATE LAMBDA FUNCTION
# ------------------------
lambda_client = boto3.client("lambda", region_name=region)

try:
    response = lambda_client.get_function(FunctionName=function_name)
    print(f"Lambda function '{function_name}' already exists")
except lambda_client.exceptions.ResourceNotFoundException:
    role_arn = iam_client.get_role(RoleName=role_name)['Role']['Arn']

    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime="python3.11",
        Role=role_arn,
        Handler="lambda_function.lambda_handler",
        Code={"ZipFile": open(lambda_file_name, 'rb').read()},
        Description="Generate S3 presigned URL for uploads",
        Timeout=10,
        MemorySize=128,
        Publish=True
    )
    print(f"Lambda function '{function_name}' created successfully")

# ------------------------
# CLEANUP
# ------------------------
os.remove("lambda_function.py")
os.remove(lambda_file_name)
print("Temporary files cleaned up. SDK Lambda deployment complete.")

