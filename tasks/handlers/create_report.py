import json
import sys
import requests
sys.path.append(".")

from services.s3Client import S3Client
from services.dynamodbClient import DynamoDBClient

def main(event, context):
  filter_id = event

  dynamodb = DynamoDBClient()
  filterData = dynamodb.get_item({ 'id': { 'S': filter_id } }, 'filter')

  filter = {
    'min_buy_order': filterData['Item']['min_buy_order']['N'],
    'max_buy_order': filterData['Item']['max_buy_order']['N'],
    'min_sell_order': filterData['Item']['min_sell_order']['N'],
    'max_sell_order': filterData['Item']['max_sell_order']['N'],
    'location_id': filterData['Item']['location_id']['N'],
    'buy_tax': filterData['Item']['buy_tax']['N'],
    'sell_tax': filterData['Item']['sell_tax']['N'],
    'min_volume': filterData['Item']['min_volume']['N'],
    'max_volume': filterData['Item']['max_volume']['N'],
    'region_id': filterData['Item']['region_id']['N']
  }

  pathData = dynamodb.get_item({ 'region_id': { 'S': filter['region_id'] } }, 'orders-index')

  path = pathData['Item']['path']['S']

  s3 = S3Client()
  result = s3.get_object(path)
  data = json.loads(result['Body'].read().decode())


  pathData = dynamodb.get_item({ 'region_id': { 'S': filter['region_id'] } }, 'history-index')
  path = pathData['Item']['path']['S']

  s3 = S3Client()
  result = s3.get_object(path)
  dataHistory = json.loads(result['Body'].read().decode())

  report = list()

  for item_id in data[filter['location_id']]:
    item = data[filter['location_id']][item_id]

    volume = None
    if str(item_id) in dataHistory:
      volume = dataHistory[str(item_id)]['week']

    if (int(item['buy_order']) >= int(filter['min_buy_order']) and int(item['buy_order']) <= int(filter['max_buy_order'])) \
      and (int(item['sell_order']) >= int(filter['min_sell_order']) and int(item['sell_order']) <= int(filter['max_sell_order'])) \
      and (volume is not None and int(volume) >= int(filter['min_volume']) and int(volume) <= int(filter['max_volume'])):

      buy_with_tax = calculatePriceWithTax(float(item['buy_order']), float(filter['buy_tax']))
      sell_with_tax = calculatePriceWithTax(float(item['sell_order']), float(filter['sell_tax']))

      report.append({ 
        'type_id': item_id, 
        'buy_order': item['buy_order'], 
        'sell_order': item['sell_order'], 
        'buy_order_tax': buy_with_tax,
        'sell_order_tax': sell_with_tax,
        'benefit_value': sell_with_tax - buy_with_tax,
        'benefit_percent': ((100 * sell_with_tax) / buy_with_tax) - 100,
        'name': get_item_name(item_id),
        'volume': volume
      })

  dynamodb.update_item(
    { 'id': { 'S': filter_id } },
    'filter',
    'set report = :report',
    {
      ':report': { 'S': json.dumps(report) }
    }
  )

def calculatePriceWithTax(price, tax):
  return price + (price * tax / 100)

def get_item_name(type_id):
  response = requests.get('https://esi.evetech.net/latest/universe/types/{}/?datasource=tranquility&language=en-us'.format(type_id))
  data = response.json()

  return data['name']

if __name__ == "__main__":
    main("", "")