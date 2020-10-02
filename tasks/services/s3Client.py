import boto3
import json
import os
from botocore.exceptions import ClientError

class S3Client:

  def __init__(self):
    self.client = boto3.client(
      's3',
      aws_access_key_id=os.environ['AWS_KEY'],
      aws_secret_access_key=os.environ['AWS_SECRET'],
    )

  def put_object(self, key, data):
    try:
      self.client.put_object(
        Body=str(json.dumps(data)),
        Bucket=os.environ['BUCKET_STORAGE'],
        Key=key
      )
    except ClientError as e:
      return False
    
    return True

  def get_object(self, key):
    try:
      return self.client.get_object(
        Bucket=os.environ['BUCKET_STORAGE'],
        Key=key
      )
    except ClientError as e:
      return False