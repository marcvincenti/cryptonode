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

	masternodes_cost = 1000
	blocks_per_day = 576
	blocks_per_month = blocks_per_day  * 30.4368499
	blocks_per_year = blocks_per_day  * 365.242199
	url = 'http://178.254.23.111/~pub/Dash/masternode_payments_stats.html'

	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])

	content = urllib2.urlopen(url).read().split('\n')
	pattern=re.compile(r'<b[^>]*> ([^<]+) </b>')
	block_number = re.findall(pattern, content[23]).pop()
	block_difficulty = re.findall(pattern, content[24]).pop()
	masternodes_count = int(re.findall(pattern, content[26]).pop())
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
			':r': decimal.Decimal(str(masternodes_reward)),
			':v': decimal.Decimal(str(masternodes_monthly_revenue)),
			':w': decimal.Decimal(str(masternodes_reward_waiting_time)),
		},
		ReturnValues="UPDATED_NEW"
	)
