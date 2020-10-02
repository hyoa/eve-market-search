import sys
import requests
import json
import time
import requests
import re
sys.path.append(".")

from services.concurrentFetcher import ConcurrentFetcher
from services.s3Client import S3Client
from services.dynamodbClient import DynamoDBClient

def main(event, context):
  region_id = event
  response = requests.head('https://esi.evetech.net/latest/markets/{}/types/?datasource=tranquility'.format(region_id))
  nbPages = int(response.headers["X-Pages"])

  urls = list()
  for index in range(nbPages):
    url = "https://esi.evetech.net/latest/markets/{}/types/?datasource=tranquility&page={}".format(region_id, index+1)
    urls.append(url)

  print('pulled pages {}'.format(len(urls)))
  fetcher = ConcurrentFetcher()
  result = fetcher.pull(urls)

  
  urls = list()
  for type_id in result:
    urls.append('https://esi.evetech.net/latest/markets/{}/history/?datasource=tranquility&type_id={}'.format(region_id, type_id))

  fetcher = ConcurrentFetcher(parse_data)
  result = fetcher.pull(urls)

  data = dict()
  for item in result:
    data[item['type_id']] = { 'week': item['week'], 'month': item['month'] }

  s3 = S3Client()
  key = 'history/{}/{}.json'.format(region_id, round(time.time()))
  put_result = s3.put_object(key, data)

  dynamodb = DynamoDBClient()
  item_to_store = { 'region_id': { 'S': region_id}, 'path': { 'S': key }}
  dynamodb.put_item(item_to_store, 'history-index')


def parse_data(data, url):
  regex = r"markets\/\d+\/history\/\?datasource=tranquility&type_id=(\d+)"
  matches = re.findall(regex, url)

  return {
    'week': calculate_average(data, 7),
    'month': calculate_average(data, 30),
    'type_id': matches[0]
  }
  

def calculate_average(data, average_day=7):
  last_items = data[-average_day:]

  if len(last_items) > 0:
    return sum(item['volume'] for item in last_items) / len(last_items)

  return 0

if __name__ == "__main__":
    main("", "")