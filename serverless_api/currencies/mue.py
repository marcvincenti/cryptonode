import os
import boto3
import urllib2
import json
import re
import datetime
import decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def price(event, context):

	url = 'https://api.coinmarketcap.com/v1/ticker/monetaryunit/?convert=EUR'

	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	content = urllib2.urlopen(url).read()
	data = json.loads(content)[0]

	table.update_item(
		Key={
			'coin': 'MonetaryUnit'
		},
		UpdateExpression="set price_usd = :u, price_eur = :e, price_btc = :b, available_supply = :s, symbol = :y ",
		ExpressionAttributeValues={
			':u': decimal.Decimal(data.get('price_usd')),
			':e': decimal.Decimal(data.get('price_eur')),
			':b': decimal.Decimal(data.get('price_btc')),
			':s': decimal.Decimal(data.get('available_supply')),
			':y': data.get('symbol'),
		},
		ReturnValues="UPDATED_NEW"
	)

def masternodes(event, context):

	masternodes_cost = 500000
	blocks_per_day = 2160
	blocks_per_month = blocks_per_day  * 30.4368499
	url = 'https://chainz.cryptoid.info/explorer/index.data.dws?coin=mue'

	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	content = urllib2.urlopen(req).read()
	data = json.loads(content)
	pattern=re.compile(r'([^<]+) / ')

	masternodes_count = int(re.findall(pattern, data.get('masternodes')).pop())

	block_reward = 40.0
	masternodes_reward = block_reward * 0.45
	masternodes_monthly_revenue = float(blocks_per_month * masternodes_reward) / float(masternodes_count)
	masternodes_reward_waiting_time = float(masternodes_count) / float(blocks_per_day)

	table.update_item(
		Key={
			'coin': 'MonetaryUnit'
		},
		UpdateExpression="set masternodes_count = :m, masternodes_reward = :r, masternodes_cost = :c, masternodes_monthly_revenue = :v, masternodes_reward_waiting_time = :w ",
		ExpressionAttributeValues={
			':m': masternodes_count,
			':r': decimal.Decimal(str(masternodes_reward)),
			':c': masternodes_cost,
			':v': decimal.Decimal(str(masternodes_monthly_revenue)),
			':w': decimal.Decimal(str(masternodes_reward_waiting_time)),
		},
		ReturnValues="UPDATED_NEW"
	)
