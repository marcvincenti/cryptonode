import json
import os
import boto3
import decimal

dynamodb = boto3.resource('dynamodb')

# This is a workaround for: http://bugs.python.org/issue16535
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

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
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }

    return response
