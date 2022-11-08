import psycopg2
import csv

connection = psycopg2.connect(
    host='localhost',
    user='root',
    password='password',
    database='final_project'
    )

def loading_orders():
    cursor = connection.cursor()

    with open('orders.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            cursor.execute(
            "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s)",
            row
        )

    connection.commit()

def loading_products():
    cursor = connection.cursor()

    with open('products.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            cursor.execute(
            "INSERT INTO products VALUES (%s, %s, %s)",
            row
        )

    connection.commit()

def loading_order_item():
    cursor = connection.cursor()

    with open('order_item.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skip the header row.
        for row in reader:
            cursor.execute(
            "INSERT INTO order_item VALUES (%s, %s)",
            row
        )

    connection.commit()

loading_products()
loading_orders()
loading_order_item() # executed last as contains foreign keys that refer to records of other tables