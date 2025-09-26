import boto3
import json


rekognition = boto3.client("rekognition")


def lambda_handler(event, context):
    try:
        # Handle proxy or non-proxy event
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event


        bucket = body["bucket"]
        key = body["key"]


        response = rekognition.detect_labels(
            Image={"S3Object": {"Bucket": bucket, "Name": key}},
            MaxLabels=10,
            MinConfidence=70
        )


        labels = [label["Name"] for label in response["Labels"]]


        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"labels": labels})
        }


    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
