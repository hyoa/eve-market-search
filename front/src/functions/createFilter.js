const aws = require('aws-sdk')
const { v4: uuidv4 } = require('uuid')
aws.config.update({
  accessKeyId: process.env.AWS_KEY,
  secretAccessKey: process.env.AWS_SECRET,
  region: 'eu-west-3',
})
const tableName = process.env.FILTER_TABLE_NAME

exports.handler = async ({ body }, context, callback) => {
  const data = JSON.parse(body)
  
  const dynamodbParams = {
    TableName: tableName,
    Item: {
      id: uuidv4(),
      ...data
    }
  }

  const client = new aws.DynamoDB.DocumentClient()

  try {
    await client.put(dynamodbParams).promise()
  } catch (e) {
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