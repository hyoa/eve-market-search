const aws = require('aws-sdk')
const { v4: uuidv4 } = require('uuid')
aws.config.update({
  accessKeyId: process.env.AWS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET,
  region: 'eu-west-3',
})
const tableName = process.env.FILTER_TABLE_NAME

exports.handler = async ({ body }, context, callback) => {
  const data = JSON.parse(body)
  
  const dynamodbParams = {
    TableName: tableName,
    Key: {
      id: data.id,
    },
    UpdateExpression: "set filter_name = :filter_name, min_buy_order = :minbo, max_buy_order = :maxbo, min_sell_order = :minso, max_sell_order = :maxso, min_volume = :minv, max_volume = :maxv, buy_tax = :bt, sell_tax = :st, region_id = :ri, location_id = :li",
    ExpressionAttributeValues: {
      ':filter_name': data.filter_name,
      ':minbo': data.min_buy_order,
      ':maxbo': data.max_buy_order,
      ':minso': data.min_sell_order,
      ':maxso': data.max_sell_order,
      ':minv': data.min_volume,
      ':maxv': data.max_volume,
      ':bt': data.buy_tax,
      ':st': data.sell_tax,
      ':ri': data.region_id,
      ':li': data.location_id,
    },
    ReturnValues: 'UPDATED_NEW'
  }

  const client = new aws.DynamoDB.DocumentClient()

  try {
    await client.update(dynamodbParams).promise()
  } catch (e) {
    console.log(e)
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 'status': 'nok' })
    }
  }

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 'status': 'ok' })
  }
}