import json
import os
import boto3
import decimal
import datetime
from boto3.dynamodb.conditions import Key

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
    result = table.scan(
		ProjectionExpression="coin, available_supply, masternodes_cost, masternodes_count, masternodes_monthly_revenue, masternodes_reward, masternodes_reward_waiting_time, price_btc, price_eur, price_gbp, price_usd, symbol"
    )

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

def get(event, context):

	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	result = table.query(
		ProjectionExpression="#cn, available_supply, masternodes_cost, masternodes_count, masternodes_monthly_revenue, masternodes_reward, masternodes_reward_waiting_time, price_btc, price_eur, price_usd, symbol",
		ExpressionAttributeNames={ "#cn": "coin" },
		KeyConditionExpression=Key("coin").eq(os.environ['COIN_ID'])
	)

	response = {
		"statusCode": 200,
		"headers": {
        	"Access-Control-Allow-Origin" : "*",
			"Access-Control-Allow-Methods" : "GET"
      	},
		"body": json.dumps(result['Items'][0], cls=DecimalEncoder)
	}

	return response

def mn_count_history(event, context):

	table = dynamodb.Table(os.environ['DYNAMODB_MASTERNODES_COUNT_TABLE'])

	today = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds())
	last_week = today - 604800

	result = table.query(
		ProjectionExpression="#t, masternodes_count",
		ExpressionAttributeNames={"#t": "timestamp" },
		KeyConditionExpression=Key('coin').eq(os.environ['COIN_ID']) & Key('timestamp').gte(last_week)
	)

	response = {
		"statusCode": 200,
		"headers": {
        	"Access-Control-Allow-Origin" : "*",
			"Access-Control-Allow-Methods" : "GET"
      	},
		"body": json.dumps(result['Items'], cls=DecimalEncoder)
	}

	return response
