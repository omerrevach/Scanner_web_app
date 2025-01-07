import boto3

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition', region_name='eu-west-1')
    s3 = boto3.client('s3')

    bucket_name = 'bucket-for-rekognition-text-extraction'
    file_name = event['body']

    response = rekognition.detect_text(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': file_name}}
    )
    detected_texts = [text['DetectedText'].strip() for text in response.get('TextDetections', [])]
    extracted_text = " ".join(detected_texts)

    # delete the file from S3 because i want to free up space im not rich
    s3.delete_object(Bucket=bucket_name, Key=file_name)

    return {"statusCode": 200, "body": extracted_text}
