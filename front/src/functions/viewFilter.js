const aws = require('aws-sdk')
const { v4: uuidv4 } = require('uuid')
aws.config.update({
  accessKeyId: process.env.ACCESS_KEY_ID,
  secretAccessKey: process.env.SECRET_ACCESS_KEY,
  region: 'eu-west-3',
})
const tableName = process.env.FILTER_TABLE_NAME

exports.handler = async (request, context, callback) => {  
  const dynamodbParams = {
    TableName: tableName,
    Key: {
      id: request.queryStringParameters.id
    }
  }

  try {
    const client = new aws.DynamoDB.DocumentClient()
    const data = await client.get(dynamodbParams).promise()

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data.Item)
    }
  } catch (e) {
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 'status': 'nok' })
    }
  }
}