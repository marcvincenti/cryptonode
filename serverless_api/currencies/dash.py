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
		UpdateExpression="set price_usd = :u, price_eur = :e, price_btc = :b, available_supply = :s, symbol = :y ",
		ExpressionAttributeValues={
			':u': data.get('price_usd'),
			':e': data.get('price_eur'),
			':b': data.get('price_btc'),
			':s': data.get('available_supply'),
			':y': data.get('symbol'),
		},
		ReturnValues="UPDATED_NEW"
	)

def masternodes(event, context):
	
	masternodes_cost = "1000"
	blocks_per_day = 576
	blocks_per_month = blocks_per_day  * 30.4368499
	blocks_per_year = blocks_per_day  * 365.242199
	url = 'http://178.254.23.111/~pub/Dash/masternode_payments_stats.html'
	
	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	content = urllib2.urlopen(url).read().split('\n')
	pattern=re.compile(r'<b[^>]*> ([^<]+) </b>')
	block_number = re.findall(pattern, content[23]).pop()
	block_difficulty = re.findall(pattern, content[24]).pop()
	masternodes_count = re.findall(pattern, content[26]).pop()
	years_elapsed = int(float(block_number) / blocks_per_year)
	
	reward = int(2222222.0/pow(((float(block_difficulty)+2600.0)/9.0),2.0));
	if reward > 25 : reward = 25
	elif reward < 5 : reward = 5
	for x in range(years_elapsed) :
		reward = reward - (float(reward)/14)
	reward = 0.9 * reward
	
	masternodes_reward = reward / 2
	masternodes_monthly_revenue = float(blocks_per_month * masternodes_reward) / float(masternodes_count)
	masternodes_reward_waiting_time = float(masternodes_count) / float(blocks_per_day)

	table.update_item(
		Key={
			'coin': 'Dash'
		},
		UpdateExpression="set masternodes_count = :m, masternodes_cost = :c, masternodes_reward = :r, masternodes_monthly_revenue = :v, masternodes_reward_waiting_time = :w  ",
		ExpressionAttributeValues={
			':m': masternodes_count,
			':c': masternodes_cost,
			':r': str(masternodes_reward),
			':v': str(masternodes_monthly_revenue),
			':w': str(masternodes_reward_waiting_time),
		},
		ReturnValues="UPDATED_NEW"
	)

def masternodes_history(event, context):
	
	url = 'http://178.254.23.111/~pub/Dash/masternode_payments_stats.html'
	
	table = dynamodb.Table(os.environ['DYNAMODB_MASTERNODES_COUNT_TABLE'])
	
	content = urllib2.urlopen(url).read().split('\n')
	pattern=re.compile(r'<b[^>]*> ([^<]+) </b>')
	
	date = datetime.datetime.utcnow()
	masternodes_count = re.findall(pattern, content[26]).pop()

	table.update_item(
		Key={
			'coin': 'Dash',
			'timestamp': int(date.strftime("%s"))
		},
		UpdateExpression="set masternodes_count = :m",
		ExpressionAttributeValues={
			':m': masternodes_count,
		},
		ReturnValues="UPDATED_NEW"
	)
