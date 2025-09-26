import boto3
from botocore.exceptions import ClientError

# Create DynamoDB client
dynamodb = boto3.client("dynamodb", region_name="ap-south-1")

table_name = "ImageLabels"

try:
    # Create table
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "ImageKey", "KeyType": "HASH"}  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "ImageKey", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"  # On-demand, Free Tier eligible
    )
    print(f"DynamoDB table '{table_name}' creation started...")

    # Wait until the table exists
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    print(f"DynamoDB table '{table_name}' is now active and ready")

except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceInUseException':
        print(f" Table '{table_name}' already exists")
    else:
        print(f" Error creating table: {e}")
