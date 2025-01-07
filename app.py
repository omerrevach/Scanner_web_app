import boto3
from flask import Flask, request, render_template, jsonify
import uuid
import os.path

app = Flask(__name__)

s3 = boto3.client('s3', region_name='eu-west-1')
rekognition = boto3.client('rekognition', region_name='eu-west-1')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_image():

    bucket_name = 'bucket-for-rekognition-text-extraction'

    # fetches image the user uploaded
    if 'image' in request.files:
        file = request.files['image']
    else:
        return "no files uploaded", 400

    # extracts the extension at the end of the file uploaded
    extension = os.path.splitext(file.filename)[1]
    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.gif']
    if extension.lower() not in allowed_extensions:
        return "file type is not allowed", 400

    # this turns the file the user uploaded into a random uuid with the extension so that their wont be a file collision
    unique_filename = f"{uuid.uuid4()}{extension}"

    s3.upload_fileobj(file, bucket_name, unique_filename)

    response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket_name, 'Name': unique_filename}})
    detected_texts = [text['DetectedText'].strip() for text in response.get('TextDetections', [])]
    extracted_text = " ".join(detected_texts)  # Join all lines with a space

    # **Delete the image from S3 after text extraction**
    s3.delete_object(Bucket=bucket_name, Key=unique_filename)

    return render_template('result.html', extracted_text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)
