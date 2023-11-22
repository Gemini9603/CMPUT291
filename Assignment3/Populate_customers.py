import random
from random import sample
import pandas as pd
import sqlite3
conn = sqlite3.connect("./Large.db")
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')

data = pd.read_csv(r'C:\Users\pooja\OneDrive\Documents\CMPUT291\Assignment3\olist_customers_dataset.csv')

column1 = data[["customer_id", "customer_zip_code_prefix"]]
column = column1.rename(columns = {'customer_zip_code_prefix':'customer_postal_code'})


c.execute('''DROP TABLE IF EXISTS Customers;''')
conn.commit()

c.execute ('''CREATE TABLE Customers(
                                    customer_id TEXT,                                   
                                    customer_postal_code INTEGER,
                                    PRIMARY KEY(customer_id)
                                   );
            ''')
conn.commit()

c.execute('''DROP TABLE IF EXISTS temp;''')
c.execute('''CREATE TABLE temp (
                                customer_id TEXT,
                                customer_postal_code INTEGER,
                                PRIMARY KEY(customer_id)
                                );
          ''')
conn.commit()


row = column.sample(n=33000)

df = pd.DataFrame(row)
df.to_sql('temp', conn, if_exists='replace', index=False)
conn.commit()

c.execute ('INSERT INTO Customers SELECT * FROM temp')
c.execute('''DROP TABLE temp;''')
conn.commit()

c.execute('SELECT COUNT(*) FROM Customers;')
rows = c.fetchall()
print(rows)
conn.commit()
conn.close()
