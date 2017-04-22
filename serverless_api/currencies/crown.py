import os
import boto3
import urllib2
import json
import re

dynamodb = boto3.resource('dynamodb')

def get(event, context):
	
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	result = table.get_item(
		Key={
			'coin': 'Crown'
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
	
	url = 'https://api.coinmarketcap.com/v1/ticker/crown/?convert=EUR'
	
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])
	
	content = urllib2.urlopen(url).read()
	data = json.loads(content)[0]
	
	table.update_item(
		Key={
			'coin': 'Crown'
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

def masternodes(event, context):
	
	masternodes_cost = "10000"
	blocks_per_day = 1440
	blocks_per_month = blocks_per_day  * 30.4368499
	url = 'https://chainz.cryptoid.info/explorer/index.data.dws?coin=crw'
	
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])
	
	req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	content = urllib2.urlopen(req).read()
	data = json.loads(content)
	pattern=re.compile(r'([^<]+) / ')
	
	masternodes_count = int(re.findall(pattern, data.get('masternodes')).pop())
	block_number = data.get('blocks')[0].get('height')
	
	halvings = int(block_number / 2100000)
	block_reward = 9.0 / pow(2.0, halvings)
	masternodes_reward = block_reward / 2.0
	masternodes_monthly_revenue = float(blocks_per_month * masternodes_reward) / float(masternodes_count)
	masternodes_reward_waiting_time = float(masternodes_count) / float(blocks_per_day)

	table.update_item(
		Key={
			'coin': 'Crown'
		},
		UpdateExpression="set masternodes_count = :m, masternodes_reward = :r, masternodes_cost = :c, masternodes_monthly_revenue = :v, masternodes_reward_waiting_time = :w ",
		ExpressionAttributeValues={
			':m': str(masternodes_count),
			':r': str(masternodes_reward),
			':c': masternodes_cost,
			':v': str(masternodes_monthly_revenue),
			':w': str(masternodes_reward_waiting_time),
		},
		ReturnValues="UPDATED_NEW"
	)
