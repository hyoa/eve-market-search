import sys
import requests
import json
import time
import requests
sys.path.append(".")

from services.concurrentFetcher import ConcurrentFetcher
from services.s3Client import S3Client
from services.dynamodbClient import DynamoDBClient

def main(event, context):
  region_id = event
  response = requests.head('https://esi.evetech.net/latest/markets/{}/orders/?datasource=tranquility&order_type=all'.format(region_id))
  nbPages = int(response.headers["X-Pages"])

  urls = list()
  for index in range(nbPages):
    url = "https://esi.evetech.net/latest/markets/{}/orders/?datasource=tranquility&order_type=all&page={}".format(region_id, index+1)
    urls.append(url)

  fetcher = ConcurrentFetcher()
  result = fetcher.pull(urls)

  data = dict()
  for item in result:
    if item['location_id'] not in data:
      data[item['location_id']] = dict()

    if item['type_id'] not in data[item['location_id']]:
      data[item['location_id']][item['type_id']] = {'buy_order': 0, 'sell_order': 999999999999999999}
    
  

    savedItem = data[item['location_id']][item['type_id']]
    if item['is_buy_order'] == False:
      if savedItem['sell_order'] > item['price']:
        data[item['location_id']][item['type_id']]['sell_order'] = item['price']
    else:
      if savedItem['buy_order'] < item['price']:
        data[item['location_id']][item['type_id']]['buy_order'] = item['price']


  s3 = S3Client()
  key = 'orders/{}/{}.json'.format(region_id, round(time.time()))
  put_result = s3.put_object(key, data)

  dynamodb = DynamoDBClient()
  item_to_store = { 'region_id': { 'S': region_id}, 'path': { 'S': key }}
  dynamodb.put_item(item_to_store, 'orders-index')

  return key

if __name__ == "__main__":
    main("", "")