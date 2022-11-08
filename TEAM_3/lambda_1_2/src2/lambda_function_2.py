import boto3
import json
import pandas as pd
import src2.load
import time


client = boto3.client("s3")

def lambda_handler(event, context):
    message = json.loads(event["Records"][0]["body"])
    bucket = message["Records"][0]["s3"]["bucket"]["name"]
    key = message["Records"][0]["s3"]["object"]["key"]
    
    
    file_dict = client.get_object(Bucket=bucket, Key=key)
    csv_file = file_dict["Body"]

    products_orders_loading(key,csv_file)
    
    time.sleep(20)
    
    orderitem_loading(key,csv_file)
    
def products_orders_loading(keys, file):   
    if keys.split('_')[0] == 'orders':
        src2.load.loading_orders(pd.read_csv(file))
    
    elif keys.split('_')[0] == 'products':
        src2.load.loading_products(pd.read_csv(file))
        
def orderitem_loading(keys, file):       
    if keys.split('_')[0] == 'orderitem':
        src2.load.loading_order_item(pd.read_csv(file))
    