import random
from random import sample
import pandas as pd
import sqlite3
conn = sqlite3.connect("./Large.db")     #TODO: Change the database name as required
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')

data = pd.read_csv(r'C:\Users\pooja\OneDrive\Documents\CMPUT291\Assignment3\olist_order_items_dataset.csv')
column = data[["order_id", "order_item_id", "product_id", "seller_id"]]

c.execute('''DROP TABLE IF EXISTS Order_items;''')
conn.commit()

c.execute('''CREATE TABLE Order_items (
                                    order_id TEXT,
                                    order_item_id TEXT, 
                                    product_id TEXT,
                                    seller_id TEXT,
                                    PRIMARY KEY(order_id, order_item_id, product_id, seller_id),
                                    FOREIGN KEY(order_id) REFERENCES Orders(order_id),
                                    FOREIGN KEY(seller_id) REFERENCES Sellers(seller_id)
                                    );
          ''')
c.execute('''DROP TABLE IF EXISTS temp;''')
c.execute('''CREATE TABLE temp (
                                order_id TEXT,
                                order_item_id TEXT,
                                product_id TEXT,
                                seller_id TEXT,
                                PRIMARY KEY(order_id, order_item_id, product_id, seller_id)
                                );
          ''')
conn.commit()

row = column.sample(n=112650)     #TODO: Change the number of rows according to the database
df = pd.DataFrame(row)
df.to_sql('temp', conn, if_exists='replace', index=False)
conn.commit()

c.execute ('INSERT INTO Order_items SELECT order_id, order_item_id, product_id, seller_id FROM temp WHERE order_id IN (SELECT order_id FROM Orders) AND seller_id IN (SELECT seller_id FROM Sellers);')
c.execute('DROP TABLE temp')
conn.commit()

c.execute('SELECT COUNT(*) FROM Order_items;')
rows = c.fetchall()
print(rows)
conn.commit()
conn.close()
