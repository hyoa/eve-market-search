const aws = require('aws-sdk')
const { v4: uuidv4 } = require('uuid')
aws.config.update({
  accessKeyId: process.env.AWS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET,
  region: 'eu-west-3',
})
const tableName = process.env.FILTER_TABLE_NAME

exports.handler = async ({ body }, context, callback) => {  
  const dynamodbParams = {
    TableName: tableName,
  }

  const client = new aws.DynamoDB.DocumentClient()

  try {
    const data = await client.scan(dynamodbParams).promise()
    
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data.Items)
    }
  } catch (e) {
    console.log(e)
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 'status': 'nok' })
    }
  }
}