from http.client import responses

import boto3
from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

rekognition = boto3.client('rekognition', region_name='eu-north-1')

def scrape_images(url, labels_to_check):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_urls = []

    for img in soup.find_all('img'):
        if 'src' in img.attrs and img['src'].startswith(('http', 'https')):
            image_urls.append(img['src'])

    return image_urls
