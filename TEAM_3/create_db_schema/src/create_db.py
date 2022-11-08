import pandas as pd
import psycopg2


def lambda_handler(event, context):
    db = "team3_project"
    user = "team3"
    password = "Team3pass"
    host = "redshiftcluster-bnfuhsmtsjms.c3ixzwdqenpm.eu-west-1.redshift.amazonaws.com"
    port = 5439

    connection = psycopg2.connect(f"dbname={db} user={user} password={password} host={host} port={port}")

    schema ='test10'

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

    cursor.close()
    connection.close()