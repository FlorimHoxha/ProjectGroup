import boto3
import json
import pandas as pd
from io import StringIO
import src1.extract_transform
 
client = boto3.client("s3")

def lambda_handler(event, context):
  
  message = json.loads(event["Records"][0]["body"])
  print(message)
  bucket=message["Records"][0]["s3"]["bucket"]["name"]
  key=message["Records"][0]["s3"]["object"]["key"]

  
  file_dict = client.get_object(Bucket=bucket, Key=key)
  csv_file = file_dict["Body"]
  
  orders, products, order_item = src1.extract_transform.extract_transform_f(csv_file)
  
  key = key.split('/')[3]
  
  save_transformed_data(orders, 'orders_'+key)
  save_transformed_data(products, 'products_'+key)
  save_transformed_data(order_item,'orderitem_'+key)


def save_transformed_data(df, key):
  csv_buf = StringIO()
  df.to_csv(csv_buf, header=True, index=False)
  csv_buf.seek(0)
  
  client.put_object(Bucket='team3-transformed-data-tf', Body=csv_buf.getvalue(), Key=key)