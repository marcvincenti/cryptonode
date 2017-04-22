import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')

def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

    # fetch all todos from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
		"headers": {
        	"Access-Control-Allow-Origin" : "*",
			"Access-Control-Allow-Methods" : "GET"
      	},
        "body": json.dumps(result['Items'])
    }

    return response
