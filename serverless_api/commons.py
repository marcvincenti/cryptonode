import os
import boto3
import decimal
import datetime
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
