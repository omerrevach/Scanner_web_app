import boto3
import uuid
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'bucket-for-rekognition-text-extraction'

    # get the uploaded file from the event
    file_content = event['body']
    file_name = event['headers']['filename']
    extension = os.path.splitext(file_name)[1]

    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.gif']
    if extension.lower() not in allowed_extensions:
        return {"statusCode": 400, "body": "File type is not allowed"}

    unique_filename = f"{uuid.uuid4()}{extension}"
    s3.put_object(Bucket=bucket_name, Key=unique_filename, Body=file_content)

    return {"statusCode": 200, "body": unique_filename}
