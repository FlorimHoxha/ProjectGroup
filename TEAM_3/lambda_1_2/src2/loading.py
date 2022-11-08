import boto3
import pandas as pd
import psycopg2


def get_db_credentials(credential_name):
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=credential_name)
    creds_string = response["Parameter"]["Value"]
    db, user, password, host, port = creds_string.split(",")
    return db, user, password, host, port


db, user, password, host, port = get_db_credentials("team3-redshift-secrets")

connection = psycopg2.connect(f"dbname={db} user={user} password={password} host={host} port={port}")

schema ='team3_db_demo'


cursor = connection.cursor()

cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

# Orders table
#--------------
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {schema}.orders(
                    order_id VARCHAR(100) PRIMARY KEY,
                    order_date DATE NOT NULL,
                    order_time TIME NOT NULL,
                    store VARCHAR(40),
                    total_price DECIMAL(4,2),
                    cash_or_card VARCHAR(4)
                )
                '''
            )
# Products table
#---------------                
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {schema}.products (
                    product_id INT IDENTITY(1, 1) PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL,
                    price DECIMAL(4,2) NOT NULL
                )
                '''
            )

# Order_item table
#-----------------
cursor.execute(f'''CREATE TABLE IF NOT EXISTS {schema}.order_item (
                    order_id VARCHAR(100) NOT NULL,
                    product_id INTEGER NOT NULL,
                    store VARCHAR(40),
                    quantity INTEGER NOT NULL,
                    PRIMARY KEY (order_id, product_id),
                    FOREIGN KEY (order_id) REFERENCES {schema}.orders(order_id),
                    FOREIGN KEY (product_id) REFERENCES {schema}.products(product_id)
                )
                '''
            )

connection.commit()

# cursor.close()
# connection.close()


def loading_orders(orders_df):

    cursor = connection.cursor()
    try:
        orders = orders_df.to_dict('records')
        for row in orders:
            cursor.execute(f"""INSERT INTO {schema}.orders(order_id, order_date, order_time, store, total_price, cash_or_card)
                                VALUES('{row['order_id']}','{row['order_date']}', '{row['order_time']}', '{row['store']}',
                                       {row['total_price']}, '{row['cash_or_card']}')""")    
        connection.commit() 
        cursor.close()               
    except Exception as error:
        print("An error occurred: " + str(error))

   

def loading_products(products_df):
   
    cursor = connection.cursor()
    try:
        products = products_df.to_dict('records')
        for row in products:    
            cursor.execute(f"""INSERT INTO {schema}.products(product_name, price)
                               SELECT * FROM (SELECT '{row['product_name']}', {row['price']}) AS tmp
                               WHERE NOT EXISTS 
                               (SELECT product_name FROM {schema}.products WHERE product_name = '{row['product_name']}')""")  
        connection.commit() 
        cursor.close()               
    except Exception as error:
        print("An error occurred: " + str(error))

def loading_order_item(order_item_df):
  
    cursor = connection.cursor()   
    try:
        order_item = order_item_df.to_dict('records')
        for row in order_item:
            cursor.execute(f"""INSERT INTO {schema}.order_item(order_id, product_id, store, quantity) 
                                 SELECT {row['order_id']}, product_id,'{row['store']}', {row['quantity']} 
                                 FROM {schema}.products WHERE product_name = '{row['product_name']}'""")  
        connection.commit() 
        cursor.close()               
    except Exception as error:
        print("An error occurred: " + str(error))