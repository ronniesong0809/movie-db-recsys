import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

load_dotenv()

s3 = boto3.resource('s3',
  endpoint_url=os.environ.get('AWS_S3_ENDPOINT_URL'),
  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
  config=Config(signature_version='s3v4'),
  region_name=os.environ.get('AWS_S3_REGION_NAME'))

def upload_file(filename, key):
  s3.Bucket(os.environ.get('AWS_S3_BUCKET')).upload_file(filename, key)

upload_file('models/model.pkl', 'model.pkl')
upload_file('data/data.json', 'data.json')
upload_file('data/data.csv', 'data.csv')
