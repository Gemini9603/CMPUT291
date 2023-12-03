import random
from random import sample
import pandas as pd
import sqlite3
conn = sqlite3.connect("./Large.db")     #TODO: Change the database name as required
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')

data = pd.read_csv(r'C:\Users\pooja\OneDrive\Documents\CMPUT291\Assignment3\olist_orders_dataset.csv')
column = data[["order_id", "customer_id"]]

c.execute('''DROP TABLE IF EXISTS Orders;''')
conn.commit()

c.execute('''CREATE TABLE Orders (
                                    order_id TEXT, 
                                    customer_id TEXT,
                                    PRIMARY KEY(order_id),
                                    FOREIGN KEY(customer_id) REFERENCES Customers(customer_id)
                                    );
          ''')
c.execute('''DROP TABLE IF EXISTS temp;''')
c.execute('''CREATE TABLE temp (
                                order_id TEXT,
                                customer_id TEXT,
                                PRIMARY KEY(order_id)
                                );
          ''')
conn.commit()

row = column.sample(n=99441)    #TODO: Change the number of rows according to database
df = pd.DataFrame(row)
df.to_sql('temp', conn, if_exists='replace', index=False)
conn.commit()

c.execute ('INSERT INTO Orders SELECT * FROM temp WHERE customer_id IN (SELECT customer_id FROM Customers);')
c.execute('''DROP TABLE temp;''')

c.execute('SELECT COUNT(*) FROM Orders;')
rows = c.fetchall()
print(rows)
conn.commit()
conn.close()
