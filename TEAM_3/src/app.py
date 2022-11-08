from operator import index
import pymysql
import csv
import os
from sqlalchemy import create_engine
# from dotenv import load_dotenv
import pandas as pd
import datetime as dt
import numpy as np
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
port = os.environ.get("mysql_port")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")
connection = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="pass1",
    database="finalproject"
    )
cursor = connection.cursor()
create_order_table = """
CREATE TABLE IF NOT EXISTS orders(
  order_id int NOT NULL,
  order_date date,
  order_time time,
  store varchar(255),
  total_price decimal(4,2),
  cash_or_card varchar(255),
  primary key (order_id)
  );
"""
create_products_table = """
CREATE TABLE IF NOT EXISTS products(
  product_id int NOT NULL,
  product_name varchar(255),
  price decimal(4,2)
  );
"""
create_order_items = """
CREATE TABLE IF NOT EXISTS customers_products(
  customer_id int NOT NULL,
  product_id varchar(10),
  quantity int
  );
"""
#create the tables for the data
cursor.execute(create_order_table)
cursor.execute(create_products_table)
cursor.execute(create_order_items)
connection.commit()


def orders():
    try:
        with open('orders.csv', 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['order_id', 'order_date', 'order_time','store', 'total_price','cash_or_card'], delimiter=',')
            next(source_file) #ignore the header row
            for row in source_file:
                sql_query = f"""INSERT INTO orders(order_id, order_date, order_time, store, total_price, cash_or_card)
                                VALUES('{row['order_id']}', '{row['order_date']}', 
                                        '{row['order_time']}', '{row['store']}',
                                        {row['total_price']}, '{row['cash_or_card']}')"""
                cursor.execute(sql_query)
            connection.commit()
            cursor.close()
    except Exception as error:
        print("An error occurred: " + str(error))


def products():
    cursor.execute(create_products_table)
    try:
        with open('products.csv', 'r') as file:
            source_file = csv.DictReader(file, fieldnames=['product_id', 'product', 'price'], delimiter=',')
            next(source_file) #ignore the header row
            for row in source_file:
                sql_query = f"""INSERT INTO products(product_id, product_name, price)
                                VALUES('{row['product_id']}', '{row['product']}', 
                                        {row['price']})"""
                cursor.execute(sql_query)
            connection.commit()
            cursor.close()
    except Exception as error:
        print("An error occurred: " + str(error))


products()