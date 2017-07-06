import os
import boto3
import urllib2
import json
import re
import datetime
import decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def masternodes(event, context):

	masternodes_cost = 10000
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
			':m': masternodes_count,
			':r': decimal.Decimal(str(masternodes_reward)),
			':c': masternodes_cost,
			':v': decimal.Decimal(str(masternodes_monthly_revenue)),
			':w': decimal.Decimal(str(masternodes_reward_waiting_time)),
		},
		ReturnValues="UPDATED_NEW"
	)
