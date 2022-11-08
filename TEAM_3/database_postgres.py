import psycopg2
import psycopg2.extras
import sys, os
import extract_transform 
import pandas as pd

def create_db_f(password,dbname):
    connection = psycopg2.connect(
        host='localhost',
        user='root',
        password=password,
        database=dbname
    )

    # DB cursor
    cursor = connection.cursor()

    #Creating DB tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS stores(
                            store_id VARCHAR(10) PRIMARY KEY,
                            store VARCHAR(255) NOT NULL                       
                        )
                        '''
                    )

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            order_id SERIAL PRIMARY KEY,
                            order_date DATE NOT NULL,
                            order_time TIME NOT NULL,
                            store_id VARCHAR(10),
                            total_price DECIMAL(4,2),
                            cash_or_card VARCHAR(4),
                            FOREIGN KEY (store_id) REFERENCES stores(store_id)
                        )
                        '''
                     )


    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            product_id SERIAL PRIMARY KEY,
                            product_name VARCHAR(255) NOT NULL,
                            price DECIMAL(4,2) NOT NULL
                        )
                        '''
                    )
    

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_item (
                            order_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            store_id VARCHAR(10),
                            quantity INTEGER NOT NULL,
                            PRIMARY KEY (order_id, product_id),
                            FOREIGN KEY (order_id) REFERENCES orders(order_id),
                            FOREIGN KEY (product_id) REFERENCES products(product_id),
                            FOREIGN KEY (store_id) REFERENCES stores(store_id)
                            )
                  ''')
   
    connection.commit()

    cursor.close()
    return connection
create_db_f('password','finalproject')

# if __name__ == '__main__':
#     connection = create_db_f('password','finalproject')

connection = create_db_f('password','finalproject')

stores_df, orders_df, products_df, order_item_df = extract_transform.extract_transform_f()



def loading_stores():
    cursor = connection.cursor()
    try:
        store = stores_df.to_dict('records')
        for row in store:
             cursor.execute(f"""INSERT INTO stores(store_id, store)
                               SELECT * FROM (SELECT '{row['store_id']}', '{row['store']}') AS tmp
                               WHERE NOT EXISTS 
                               (SELECT store FROM stores WHERE store = '{row['store']}')""")
        connection.commit() 
        cursor.close()               
    except Exception as error:
        print("An error occurred: " + str(error))


def loading_orders():

    cursor = connection.cursor()
    try:
        orders = orders_df.to_dict('records')
        for row in orders:
            cursor.execute(f"""INSERT INTO orders(order_date, order_time, store_id, total_price, cash_or_card)
                                VALUES('{row['order_date']}', '{row['order_time']}', '{row['store_id']}',
                                       {row['total_price']}, '{row['cash_or_card']}')""")    
        connection.commit() 
        cursor.close()               
    except Exception as error:
        print("An error occurred: " + str(error))

   

def loading_products():
   
    cursor = connection.cursor()
    try:
        products = products_df.to_dict('records')
        for row in products:    
            cursor.execute(f"""INSERT INTO products(product_name, price)
                               SELECT * FROM (SELECT '{row['product_name']}', {row['price']}) AS tmp
                               WHERE NOT EXISTS 
                               (SELECT product_name FROM products WHERE product_name = '{row['product_name']}')""")  
        connection.commit() 
        cursor.close()               
    except Exception as error:
        print("An error occurred: " + str(error))

def loading_order_item():
  
    cursor = connection.cursor()   
    try:
        order_item = order_item_df.to_dict('records')
        for row in order_item:
            cursor.execute(f"""INSERT INTO order_item(order_id, product_id, store_id, quantity) 
                                 SELECT {row['order_id']}, product_id, '{row['store_id']}', {row['quantity']} 
                                 FROM products WHERE product_name = '{row['product_name']}'""")  
        connection.commit() 
        cursor.close()               
    except Exception as error:
        print("An error occurred: " + str(error))

loading_stores()
loading_orders()
loading_products()
loading_order_item()
