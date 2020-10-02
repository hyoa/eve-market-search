import sys
sys.path.append(".")

from services.dynamodbClient import DynamoDBClient

def main(event, context):
  dynamodb = DynamoDBClient()
  filters = dynamodb.scan('filter')

  regions = list()
  ids = list()

  for filter in filters['Items']:
    if filter['region_id']['N'] not in regions:
      regions.append(filter['region_id']['N'])

    if filter['id']['S'] not in ids:
      ids.append(filter['id']['S'])

  return {
    'region_ids': regions,
    'filter_ids': ids
  }

if __name__ == "__main__":
    main("", "")