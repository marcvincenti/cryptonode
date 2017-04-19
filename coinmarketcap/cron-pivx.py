import os
import boto3
import urllib2
import json

dynamodb = boto3.resource('dynamodb')
url = 'https://api.coinmarketcap.com/v1/ticker/pivx/?convert=EUR'

def currency(event, context):
	
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])
	
	content = urllib2.urlopen(url).read()
	data = json.loads(content)[0]
	
	table.update_item(
		Key={
			'coin': 'PIVX'
		},
		UpdateExpression="set price_usd = :u, price_eur = :e, price_btc = :b ",
		ExpressionAttributeValues={
			':u': data.get('price_usd'),
			':e': data.get('price_eur'),
			':b': data.get('price_btc'),
		},
		ReturnValues="UPDATED_NEW"
	)

