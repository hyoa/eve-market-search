import boto3
import os
from botocore.exceptions import ClientError

class DynamoDBClient:

  def __init__(self):
    self.client = boto3.client(
      'dynamodb',
      aws_access_key_id=os.environ['AWS_KEY'],
      aws_secret_access_key=os.environ['AWS_SECRET'],
    )
  
  def put_item(self, item, table_name):
    self.client.put_item(
      TableName='{}-{}'.format(os.environ['TABLE_PREFIX'], table_name),
      Item=item
    )

    return True

  def get_item(self, key, table_name):
    return self.client.get_item(
      TableName='{}-{}'.format(os.environ['TABLE_PREFIX'], table_name),
      Key=key
    )
  
  def scan(self, table_name):
    return self.client.scan(
      TableName='{}-{}'.format(os.environ['TABLE_PREFIX'], table_name)
    )

  def update_item(self, key, table_name, update_expression, attribute_values):
    return self.client.update_item(
      TableName='{}-{}'.format(os.environ['TABLE_PREFIX'], table_name),
      Key=key,
      UpdateExpression=update_expression,
      ExpressionAttributeValues=attribute_values,
      ReturnValues="UPDATED_NEW"
    )
