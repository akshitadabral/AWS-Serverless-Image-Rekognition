import boto3
from botocore.exceptions import ClientError
import json
import os

# ----------------------
# CONFIGURATION
# ----------------------
BUCKET_NAME = "image-rekognition-deploy-akshita"
FILE_NAME = "myproject.html"
FILE_PATH = os.path.join(os.getcwd(), FILE_NAME)
REGION = "ap-south-1"

# Initialize S3 client
s3 = boto3.client("s3", region_name=REGION)

# ----------------------
# Create bucket
# ----------------------
try:
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": REGION}
    )
    print(f"Bucket '{BUCKET_NAME}' created successfully.")
except ClientError as e:
    if "BucketAlreadyOwnedByYou" in str(e):
        print(f"Bucket '{BUCKET_NAME}' already exists and is owned by you.")
    else:
        print("Error creating bucket:", e)

# ----------------------
#Update public access settings
# ----------------------
try:
    s3.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False
        }
    )
    print("Public access settings updated.")
except ClientError as e:
    print("Error updating public access settings:", e)

# ----------------------
# Enable static website hosting
# ----------------------
try:
    s3.put_bucket_website(
        Bucket=BUCKET_NAME,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': FILE_NAME},
            'ErrorDocument': {'Key': FILE_NAME}
        }
    )
    print("Static website hosting enabled.")
except ClientError as e:
    print("Error enabling static website hosting:", e)

# ----------------------
#Apply bucket policy for public read
# ----------------------
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadAccess",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
        }
    ]
}

try:
    s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=json.dumps(bucket_policy))
    print("Bucket policy applied.")
except ClientError as e:
    print("Error setting bucket policy:", e)

# ----------------------
# Upload HTML file
# ----------------------
if os.path.exists(FILE_PATH):
    try:
        s3.upload_file(FILE_PATH, BUCKET_NAME, FILE_NAME, ExtraArgs={'ContentType': 'text/html'})
        print(f"File '{FILE_NAME}' uploaded successfully.")
    except ClientError as e:
        print("Error uploading file:", e)
else:
    print(f"File '{FILE_PATH}' not found. Check the path.")

# ----------------------
# Website URL
# ----------------------
website_url = f"http://{BUCKET_NAME}.s3-website.{REGION}.amazonaws.com"
print(f"Website deployed! Access it at: {website_url}")

