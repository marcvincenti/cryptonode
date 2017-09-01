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

	block_reward = 4.5 #Reward of stakers + masternodes
	masternodes_cost = 10000
	blocks_per_day = 1440
	blocks_per_month = blocks_per_day  * 30.4368499
	url = 'http://178.254.23.111/~pub/DN/DN_masternode_payments_stats.html'

	table = dynamodb.Table(os.environ['DYNAMODB_CURRENCIES_TABLE'])
	
	content = urllib2.urlopen(url).read()
	pattern_mn = re.compile(r'Current Number of Masternodes: <b[^>]*> ([^<]+) </b>')
	pattern_supp = re.compile(r'Available Supply: <b[^>]*> ([^<]+) </b>')
	masternodes_count = int(re.findall(pattern_mn, content).pop())
	available_supply = int(re.findall(pattern_supp, content).pop())
	masternodes_rate = (float(masternodes_count) * 10000) / float(available_supply)

	if masternodes_rate <= 0.01 : masternodes_reward = block_reward * 0.90
	elif masternodes_rate <= 0.02 : masternodes_reward = block_reward * 0.88
	elif masternodes_rate <= 0.03 : masternodes_reward = block_reward * 0.87
	elif masternodes_rate <= 0.04 : masternodes_reward = block_reward * 0.86
	elif masternodes_rate <= 0.05 : masternodes_reward = block_reward * 0.85
	elif masternodes_rate <= 0.06 : masternodes_reward = block_reward * 0.84
	elif masternodes_rate <= 0.07 : masternodes_reward = block_reward * 0.83
	elif masternodes_rate <= 0.08 : masternodes_reward = block_reward * 0.82
	elif masternodes_rate <= 0.09 : masternodes_reward = block_reward * 0.81
	elif masternodes_rate <= 0.10 : masternodes_reward = block_reward * 0.80
	elif masternodes_rate <= 0.11 : masternodes_reward = block_reward * 0.79
	elif masternodes_rate <= 0.12 : masternodes_reward = block_reward * 0.78
	elif masternodes_rate <= 0.13 : masternodes_reward = block_reward * 0.77
	elif masternodes_rate <= 0.14 : masternodes_reward = block_reward * 0.76
	elif masternodes_rate <= 0.15 : masternodes_reward = block_reward * 0.75
	elif masternodes_rate <= 0.16 : masternodes_reward = block_reward * 0.74
	elif masternodes_rate <= 0.17 : masternodes_reward = block_reward * 0.73
	elif masternodes_rate <= 0.18 : masternodes_reward = block_reward * 0.72
	elif masternodes_rate <= 0.19 : masternodes_reward = block_reward * 0.71
	elif masternodes_rate <= 0.20 : masternodes_reward = block_reward * 0.70
	elif masternodes_rate <= 0.21 : masternodes_reward = block_reward * 0.69
	elif masternodes_rate <= 0.22 : masternodes_reward = block_reward * 0.68
	elif masternodes_rate <= 0.23 : masternodes_reward = block_reward * 0.67
	elif masternodes_rate <= 0.24 : masternodes_reward = block_reward * 0.66
	elif masternodes_rate <= 0.25 : masternodes_reward = block_reward * 0.65
	elif masternodes_rate <= 0.26 : masternodes_reward = block_reward * 0.64
	elif masternodes_rate <= 0.27 : masternodes_reward = block_reward * 0.63
	elif masternodes_rate <= 0.28 : masternodes_reward = block_reward * 0.62
	elif masternodes_rate <= 0.29 : masternodes_reward = block_reward * 0.61
	elif masternodes_rate <= 0.30 : masternodes_reward = block_reward * 0.60
	elif masternodes_rate <= 0.31 : masternodes_reward = block_reward * 0.59
	elif masternodes_rate <= 0.32 : masternodes_reward = block_reward * 0.58
	elif masternodes_rate <= 0.33 : masternodes_reward = block_reward * 0.57
	elif masternodes_rate <= 0.34 : masternodes_reward = block_reward * 0.56
	elif masternodes_rate <= 0.35 : masternodes_reward = block_reward * 0.55
	elif masternodes_rate <= 0.363 : masternodes_reward = block_reward * 0.54
	elif masternodes_rate <= 0.376 : masternodes_reward = block_reward * 0.53
	elif masternodes_rate <= 0.389 : masternodes_reward = block_reward * 0.52
	elif masternodes_rate <= 0.402 : masternodes_reward = block_reward * 0.51
	elif masternodes_rate <= 0.415 : masternodes_reward = block_reward * 0.50
	elif masternodes_rate <= 0.428 : masternodes_reward = block_reward * 0.49
	elif masternodes_rate <= 0.441 : masternodes_reward = block_reward * 0.48
	elif masternodes_rate <= 0.454 : masternodes_reward = block_reward * 0.47
	elif masternodes_rate <= 0.467 : masternodes_reward = block_reward * 0.46
	elif masternodes_rate <= 0.48 : masternodes_reward = block_reward * 0.45
	elif masternodes_rate <= 0.493 : masternodes_reward = block_reward * 0.44
	elif masternodes_rate <= 0.506 : masternodes_reward = block_reward * 0.43
	elif masternodes_rate <= 0.519 : masternodes_reward = block_reward * 0.42
	elif masternodes_rate <= 0.532 : masternodes_reward = block_reward * 0.41
	elif masternodes_rate <= 0.545 : masternodes_reward = block_reward * 0.40
	elif masternodes_rate <= 0.558 : masternodes_reward = block_reward * 0.39
	elif masternodes_rate <= 0.571 : masternodes_reward = block_reward * 0.38
	elif masternodes_rate <= 0.584 : masternodes_reward = block_reward * 0.37
	elif masternodes_rate <= 0.597 : masternodes_reward = block_reward * 0.36
	elif masternodes_rate <= 0.61 : masternodes_reward = block_reward * 0.35
	elif masternodes_rate <= 0.623 : masternodes_reward = block_reward * 0.34
	elif masternodes_rate <= 0.636 : masternodes_reward = block_reward * 0.33
	elif masternodes_rate <= 0.649 : masternodes_reward = block_reward * 0.32
	elif masternodes_rate <= 0.662 : masternodes_reward = block_reward * 0.31
	elif masternodes_rate <= 0.675 : masternodes_reward = block_reward * 0.30
	elif masternodes_rate <= 0.688 : masternodes_reward = block_reward * 0.29
	elif masternodes_rate <= 0.701 : masternodes_reward = block_reward * 0.28
	elif masternodes_rate <= 0.714 : masternodes_reward = block_reward * 0.27
	elif masternodes_rate <= 0.727 : masternodes_reward = block_reward * 0.26
	elif masternodes_rate <= 0.74 : masternodes_reward = block_reward * 0.25
	elif masternodes_rate <= 0.753 : masternodes_reward = block_reward * 0.24
	elif masternodes_rate <= 0.766 : masternodes_reward = block_reward * 0.23
	elif masternodes_rate <= 0.779 : masternodes_reward = block_reward * 0.22
	elif masternodes_rate <= 0.792 : masternodes_reward = block_reward * 0.21
	elif masternodes_rate <= 0.805 : masternodes_reward = block_reward * 0.20
	elif masternodes_rate <= 0.818 : masternodes_reward = block_reward * 0.19
	elif masternodes_rate <= 0.831 : masternodes_reward = block_reward * 0.18
	elif masternodes_rate <= 0.844 : masternodes_reward = block_reward * 0.17
	elif masternodes_rate <= 0.857 : masternodes_reward = block_reward * 0.16
	elif masternodes_rate <= 0.87 : masternodes_reward = block_reward * 0.15
	elif masternodes_rate <= 0.883 : masternodes_reward = block_reward * 0.14
	elif masternodes_rate <= 0.896 : masternodes_reward = block_reward * 0.13
	elif masternodes_rate <= 0.909 : masternodes_reward = block_reward * 0.12
	elif masternodes_rate <= 0.922 : masternodes_reward = block_reward * 0.11
	elif masternodes_rate <= 0.935 : masternodes_reward = block_reward * 0.10
	elif masternodes_rate <= 0.945 : masternodes_reward = block_reward * 0.09
	elif masternodes_rate <= 0.961 : masternodes_reward = block_reward * 0.08
	elif masternodes_rate <= 0.974 : masternodes_reward = block_reward * 0.07
	elif masternodes_rate <= 0.987 : masternodes_reward = block_reward * 0.06
	elif masternodes_rate <= 0.99 : masternodes_reward = block_reward * 0.05
	else : masternodes_reward = block_reward * 0.01

	masternodes_monthly_revenue = float(blocks_per_month * masternodes_reward) / float(masternodes_count)
	masternodes_reward_waiting_time = float(masternodes_count) / float(blocks_per_day)

	table.update_item(
		Key={
			'coin': 'PIVX'
		},
		UpdateExpression="set masternodes_count = :m, available_supply = :s, masternodes_reward = :r, masternodes_cost = :c, masternodes_monthly_revenue = :v, masternodes_reward_waiting_time = :w ",
		ExpressionAttributeValues={
			':m': masternodes_count,
			':s': available_supply,
			':r': decimal.Decimal(str(masternodes_reward)),
			':c': masternodes_cost,
			':v': decimal.Decimal(str(masternodes_monthly_revenue)),
			':w': decimal.Decimal(str(masternodes_reward_waiting_time)),
		},
		ReturnValues="UPDATED_NEW"
	)
