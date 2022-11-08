import pandas as pd
import numpy as np
import hashlib


def hash(s: str) -> str:
    return str(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16))[:10]

def extract_transform_f(file):
    # PoC: Extract data from CSV file
    # ======================================
   
    headers = ['timestamp','store','customer_name','basket_items','total_price','cash_or_card','card_number']
    df = pd.read_csv(file, parse_dates=['timestamp'], infer_datetime_format=True, names = headers)

    #create column used to create hash
    df["order_id_pre_hash"] = df["timestamp"].astype(str) + df["store"] + df["customer_name"]
   
    
    # PoC: Transform - Remove sensitive data
    # ======================================
    df.drop(['customer_name', 'card_number'], axis = 1, inplace = True)

    # PoC: Transform - Normalise data to 3NF
    # ======================================

    # 1. Obtaining First Normal Form (1NF):
    # ----------------------------------
    df_1nf = df

    # 1.1 Remove multi-valued fields (multiple values in a single column) - timestamp:

    df_1nf.insert(loc=0, column='order_date', value=df_1nf.timestamp.dt.date)
    df_1nf.insert(loc=1, column='order_time', value=df_1nf.timestamp.dt.time)
    del df_1nf["timestamp"]

    # 1.2 Remove multi-valued fields (multiple values in a single column) - basket_items:
   
    # 1.2.a. Split the string containing 'basket items' to form a list of individual 'product - price' strings:
    df_1nf["basket_items"] = df_1nf["basket_items"].apply(lambda x: x.split(", "))

    # 1.2.b. Transform each element of a list-like to a row, replicating index values:
    df_1nf = df_1nf.explode("basket_items")

    # 1.2.c. Separate 'basket_items' column to form new column for 'product' and for 'price'
    # df['product2'] = df["basket_items"].apply(lambda x: x.rsplit("-", 1)[0])
    df_1nf["product_name"] = [x.rsplit(" -", 1)[0].title() for x in df_1nf["basket_items"]]
    df_1nf["price"] = [x.rsplit("- ", 1)[1]for x in df_1nf["basket_items"]]
    # print("exploding", df_1nf)
    del df_1nf["basket_items"]


    # 2. Obtaining Second Normal Form (2NF):
    # -------------------------------------
    # Remove partial dependencies
    # Split things that depend on product out to a new entity table
    df_2nf = df_1nf
   

    # 2.1a Create order_id
    # create hash of [timestamp + store + customer_name] column to create order id
    df_2nf["order_id"] = [hash(x) for x in df_2nf['order_id_pre_hash']]
   

    # 2.1b Create orders table (transforming and extracting from df_2nf)
    # NOTE: should not overwrite existing df_2nf as may lose some products
    orders_df = df_2nf.drop_duplicates(subset = ["order_id"]) # removing duplicate order ids in df_2nf and returned as a copy (inplace=False by default) called orders_df
    orders_df = orders_df[['order_id','order_date','order_time','store','total_price','cash_or_card']]
   

    # 2.2a Create product_id & apply to df_2nf table
    product_names = df_2nf['product_name'].unique() # obtaining unique product values as a numpy.ndarray
    product_names = pd.Series(np.arange(len(product_names)), product_names) # pandas series containing unique product_names and their ids as index
    df_2nf['product_id'] = df_2nf['product_name'].apply(product_names.get)  # assigning each product in df_1nf with their corresponding id
    # print("created product_id: ",df_2nf)    
   
    # 2.2b Create products table (transforming and extracting from df_2nf)
    products_df = df_2nf.drop_duplicates(subset = ["product_name"]) # removing duplicate product
    products_df = products_df[["product_id","product_name", "price"]]
   

    # 2.3 Create order_item table
    # order_item_df = df_2nf.groupby(['order_id','product_id','store_id','product_name'])['total_price'].count().reset_index(name='quantity')
    add_quantity = df_2nf.groupby(['order_id','product_id','store','product_name']).size()
    order_item_df = add_quantity.to_frame(name = 'quantity').reset_index()
   
    return orders_df, products_df, order_item_df