import random
from random import sample
import pandas as pd
import sqlite3
conn = sqlite3.connect("./Large.db")
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')

data = pd.read_csv(r'C:\Users\pooja\OneDrive\Documents\CMPUT291\Assignment3\olist_sellers_dataset.csv')
column1 = data[["seller_id", "seller_zip_code_prefix"]]
column = column1.rename(columns = {'seller_zip_code_prefix':'seller_postal_code'})

c.execute('''DROP TABLE IF EXISTS Sellers;''')
conn.commit()

c.execute('''CREATE TABLE Sellers (
                                    seller_id TEXT, 
                                    seller_postal_code INTEGER,
                                    PRIMARY KEY(seller_id)
                                    );
          ''')
conn.commit()

c.execute('''DROP TABLE IF EXISTS temp;''')
c.execute('''CREATE TABLE temp (
                                seller_id TEXT,
                                seller_postal_code INTEGER,
                                PRIMARY KEY(seller_id)
                                );
          ''')
conn.commit()

row = column.sample(n=1000)

df = pd.DataFrame(row)
df.to_sql('temp', conn, if_exists='replace', index=False)
conn.commit()

c.execute ('INSERT INTO Sellers SELECT * FROM temp')
c.execute('''DROP TABLE temp;''')
conn.commit()

c.execute('SELECT COUNT(*) FROM Sellers;')
rows = c.fetchall()
print(rows)
conn.commit()
conn.close()