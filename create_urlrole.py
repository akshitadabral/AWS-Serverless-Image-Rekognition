import boto3
import json
import time

# Create IAM client
iam = boto3.client("iam")

role_name = "urlrole"

# Trust policy: allows Lambda to assume this role
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

# Step 1: Create IAM Role
try:
    response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(assume_role_policy),
        Description="Role for Lambda functions in Image Upload project"
    )
    print("Role created:", response["Role"]["Arn"])
except iam.exceptions.EntityAlreadyExistsException:
    print("Role already exists")

# Step 2: Attach required policies
policies = [
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/AmazonSNSFullAccess",
    "arn:aws:iam::aws:policy/AmazonRekognitionFullAccess",
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
]

for policy_arn in policies:
    try:
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(f" Attached policy: {policy_arn}")
    except Exception as e:
        print(f"Failed to attach policy {policy_arn}: {e}")


print("Waiting 10 seconds for IAM role propagation...")
time.sleep(10)
print("IAM role setup complete and ready for Lambda.")

