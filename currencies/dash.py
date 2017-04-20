import os
import boto3
import urllib2
import json

dynamodb = boto3.resource('dynamodb')

def get(event, context):
	
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	result = table.get_item(
		Key={
			'coin': 'Dash'
		}
	)

	response = {
		"statusCode": 200,
		"headers": {
        	"Access-Control-Allow-Origin" : "*",
			"Access-Control-Allow-Methods" : "GET"
      	},
		"body": json.dumps(result['Item'])
	}

	return response

def price(event, context):
	
	url = 'https://api.coinmarketcap.com/v1/ticker/dash/?convert=EUR'
	
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])
	
	content = urllib2.urlopen(url).read()
	data = json.loads(content)[0]
	
	table.update_item(
		Key={
			'coin': 'Dash'
		},
		UpdateExpression="set price_usd = :u, price_eur = :e, price_btc = :b, available_supply = :s ",
		ExpressionAttributeValues={
			':u': data.get('price_usd'),
			':e': data.get('price_eur'),
			':b': data.get('price_btc'),
			':s': data.get('available_supply'),
		},
		ReturnValues="UPDATED_NEW"
	)

