import os
import boto3
import decimal
import datetime
import urllib2
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def masternodes_history(event, context):

	coin = os.environ['COIN_ID']
	from_table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])
	to_table = dynamodb.Table(os.environ['DYNAMODB_MASTERNODES_COUNT_TABLE'])

	result = from_table.get_item(Key={'coin': coin})['Item']

	date = datetime.datetime.now()
	quarter_day = datetime.datetime(date.year, date.month, date.day, date.hour)

	to_table.update_item(
		Key={
			'coin': coin,
			'timestamp': int(quarter_day.strftime("%s"))
		},
		UpdateExpression="set masternodes_count = :m, price = :p, masternodes_reward = :r, available_supply = :a",
		ExpressionAttributeValues={
			':m': result.get('masternodes_count'),
			':p': result.get('price_btc'),
			':r': result.get('masternodes_reward'),
			':a': result.get('available_supply'),
		},
		ReturnValues="UPDATED_NEW"
	)

def price(event, context):
	coin = os.environ['COIN_ID']
	ticker = os.environ['COIN_TICKER']
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	url_eur = 'https://api.coinmarketcap.com/v1/ticker/'+ticker+'/?convert=EUR'
	content_eur = urllib2.urlopen(url_eur).read()
	data_eur = json.loads(content_eur)[0]

	url_gbp = 'https://api.coinmarketcap.com/v1/ticker/'+ticker+'/?convert=GBP'
	content_gbp = urllib2.urlopen(url_gbp).read()
	data_gbp = json.loads(content_gbp)[0]

	table.update_item(
		Key={
			'coin': coin
		},
		UpdateExpression="set price_usd = :u, price_eur = :e, price_btc = :b, price_gbp = :g, available_supply = :s, symbol = :y ",
		ExpressionAttributeValues={
			':u': decimal.Decimal(data_eur.get('price_usd')),
			':e': decimal.Decimal(data_eur.get('price_eur')),
			':b': decimal.Decimal(data_eur.get('price_btc')),
			':g': decimal.Decimal(data_gbp.get('price_gbp')),
			':s': decimal.Decimal(data_eur.get('available_supply')),
			':y': data_eur.get('symbol'),
		},
		ReturnValues="UPDATED_NEW"
	)
