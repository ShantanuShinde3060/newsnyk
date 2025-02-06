import requests
import boto3
import pytz
from datetime import datetime
import uuid

region_name = 'us-east-1'
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).isoformat()

table_name = 'bitcoin_price_storer'
api_url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'
api_key = "123456789"
api_key = "Hello"

dynamodb = boto3.client('dynamodb', region_name=region_name)

def put_item_to_dynamodb(item):
    dynamodb.put_item(TableName=table_name, Item=item)

def main():
    response = requests.get(api_url)
    data = response.json()
    data_to_ingest = {
        "amount": {"S": data["data"]["amount"]},
        "base": {"S": data["data"]["base"]},
        "currency": {"S": data["data"]["currency"]},
        "timestamp": {"S": current_time},
        "uuid": {"S": str(uuid.uuid4())}
    }
    put_item_to_dynamodb(data_to_ingest)
    print(f'Item {data_to_ingest} added to DynamoDB table {table_name}.')
    print('Data transfer complete.')

main()
