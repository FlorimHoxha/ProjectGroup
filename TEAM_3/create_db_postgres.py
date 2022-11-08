import psycopg2

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
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            order_id INTEGER PRIMARY KEY,
                            order_date DATE NOT NULL,
                            order_time TIME NOT NULL,
                            store VARCHAR(255),
                            total_price DECIMAL(4,2),
                            cash_or_card VARCHAR(4)
                        )
                        '''
                    )

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            product_id INTEGER PRIMARY KEY,
                            product_name VARCHAR(255) NOT NULL,
                            price DECIMAL(4,2) NOT NULL
                        )
                        '''
                    )

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_item (
                            order_id INTEGER NOT NULL,
                            product_id INTEGER NOT NULL,
                            FOREIGN KEY (order_id) REFERENCES orders(order_id),
                            FOREIGN KEY (product_id) REFERENCES products(product_id)
                        )
                        '''
                    )
                    
    connection.commit()

    cursor.close()
    return connection


if __name__ == '__main__':
    connection = create_db_f('password','final_project')
    connection.close()