import boto3
from botocore.exceptions import ClientError

# Create S3 client
s3 = boto3.client("s3", region_name="ap-south-1")

bucket_name = "image-upload-bucket-akshita"

# Define CORS configuration
cors_config = {
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST", "HEAD"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": ["ETag"],
            "MaxAgeSeconds": 3000
        }
    ]
}

try:
    # Check if bucket already exists
    s3.head_bucket(Bucket=bucket_name)
    print(f" Bucket '{bucket_name}' already exists. Skipping creation.")

except ClientError as e:
    error_code = int(e.response["Error"]["Code"])
    if error_code == 404:  # Bucket not found
        try:
            # Create bucket
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": "ap-south-1"}
            )
            print(f"Bucket '{bucket_name}' created successfully in ap-south-1")
        except ClientError as ce:
            print(f"Error creating bucket: {ce}")
    else:
        print(f" Unexpected error: {e}")

# Apply/Update CORS configuration
try:
    s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_config)
    print(f" CORS configuration applied to '{bucket_name}'")
except ClientError as e:
    print(f" Error applying CORS: {e}")
