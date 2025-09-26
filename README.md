# AWS-Serverless-Image-Rekognition

## Overview
This project is an **event-driven serverless image recognition system** built entirely on AWS. Users can upload images through a static website, and the system automatically detects objects, people, and scenes using **Amazon Rekognition**. Detected labels are stored in **DynamoDB**, and notifications are sent via **SNS**.  

![WhatsApp Image 2025-09-26 at 13 46 53_99d1794a](https://github.com/user-attachments/assets/f6cfb01a-3d9b-4404-9d00-a8d4219ab9da)


---

## Architecture
- **Frontend (S3 Static Website):** Upload images and view results.  
- **API Gateway & Lambda:**  
  - `/generate-upload-url` → GenerateUploadURLLambda: Provides pre-signed URL for secure S3 uploads.  
  - `/detect-labels` → DetectLabelsLambda: Retrieves labels from DynamoDB.  
- **Amazon S3:** Stores images; triggers processing Lambda on upload.  
- **Lambda Functions:**  
  - GenerateUploadURLLambda – Create secure S3 URLs.  
  - ProcessImageUploadLambda – Analyze images using Rekognition, store labels in DynamoDB, send SNS notification.  
  - DetectLabelsLambda – Fetch detected labels for the frontend.  
- **Amazon Rekognition:** Performs image analysis.  
- **Amazon DynamoDB:** Stores image metadata and detected labels.  
- **Amazon SNS:** Sends notifications.  
- **Amazon CloudWatch:** Monitors Lambda and API activity.

---

## AWS Services Used
- Amazon S3  
- AWS Lambda  
- Amazon Rekognition  
- Amazon DynamoDB  
- Amazon SNS  
- Amazon API Gateway  
- Amazon CloudWatch  

---

## Deployment Steps
1. **IAM User & AWS SDK:** Programmatic access via Boto3.  
2. **IAM Role:** Permissions for Lambda functions to access AWS services.  
3. **S3 Bucket:** Store uploaded images.  
4. **DynamoDB Table:** Store labels and metadata.  
5. **SNS Topic & Subscription:** Send notifications.  
6. **Lambda Functions:**  
   - GenerateUploadURLLambda  
   - ProcessImageUploadLambda  
   - DetectLabelsLambda  
7. **Connect S3 Event:** Trigger ProcessImageUploadLambda on new uploads.  
8. **API Gateway:**  
   - `/generate-upload-url` → GenerateUploadURLLambda  
   - `/detect-labels` → DetectLabelsLambda  
9. **Frontend Deployment:** Upload HTML/JS frontend to hosting S3 bucket.

---

## User Workflow
1. Open the static website on S3.  
2. Select and upload an image.  
3. System automatically:  
   - Uploads image securely to S3.  
   - Detects objects/scenes via Rekognition.  
   - Stores results in DynamoDB.  
   - Sends notification via SNS.  
4. User sees detected labels on the website.  

---

## Deployment Flow

**Automated Scripts**
1. create_urlrole.py – Creates IAM role for Lambda functions with required permissions.
2. create_bucket_with_cors.py – Creates S3 bucket and applies CORS configuration.
3. create_dynamotable.py – Creates DynamoDB table to store image labels and metadata.
4. create_sns.py – Creates SNS topic and subscription for email notifications.
5. create_function1.py – Deploys GenerateUploadURLLambda function.
6. create_function2.py – Deploys ProcessImageUploadLambda function.
7. create_s3trigger.py – Connects S3 bucket “ObjectCreated” event to trigger ProcessImageUploadLambda.

**Manual Steps on AWS Console**

1. API Gateway: /generate-upload-url
Create resource → Add POST method → Integrate with GenerateUploadURLLambda.
2. Lambda Function: DetectLabelsLambda
Manually create and paste detectlabels.py code.
3. API Gateway: /detect-labels
Create resource → Add POST method → Integrate with DetectLabelsLambda → Enable CORS.

**Frontend Setup*

1. Create or edit the frontend (static website).
2. Configure API endpoint URLs (/generate-upload-url and /detect-labels) in the frontend code.
3. Ensure S3 hosting bucket is created for the static website.

**Deployment**

1. create_deploy.py – Run this script to upload the frontend files to the S3 hosting bucket.
2. Open the S3 static website URL to test the application.

**Notes**

1.Pre-signed URLs ensure secure uploads without exposing S3 bucket credentials.
2.Serverless architecture allows automatic scaling with upload traffic.
3.CloudWatch logs provide monitoring and debugging.
