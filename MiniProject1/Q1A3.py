import sqlite3
import time
import matplotlib.pyplot as plt
import numpy as np

conn = None
c = None

def connect(path):
    global conn, c
    conn = sqlite3.connect(path)
    c = conn.cursor()
    conn.commit()
    return

def rename1():
    global conn, c
    c.execute('ALTER TABLE Customers RENAME TO orig_Customers;')
    c.execute('ALTER TABLE Sellers RENAME TO orig_Sellers;')
    c.execute('ALTER TABLE Orders RENAME TO orig_Orders;')
    c.execute('ALTER TABLE Order_items RENAME TO orig_Order_items;')
    conn.commit()
    return

def uninformed():
    global conn, c
    c.execute("PRAGMA synchronous = OFF")
    c.execute("PRAGMA journal_mode = MEMORY")
    c.execute("PRAGMA auto_vacuum = NONE")
    c.execute('PRAGMA foreign_keys = OFF;')
    c.execute('PRAGMA automatic_index = OFF;')
    c.execute('''CREATE TABLE Customers(
                                        customer_id TEXT,                                   
                                        customer_postal_code INTEGER
                                       );
             ''')
    c.execute('''CREATE TABLE Sellers (
                                       seller_id TEXT, 
                                       seller_postal_code INTEGER
                                      );
             ''')
    c.execute('''CREATE TABLE Orders (
                                      order_id TEXT, 
                                      customer_id TEXT
                                     );
             ''')
    c.execute('''CREATE TABLE Order_items (
                                        order_id TEXT,
                                        order_item_id TEXT, 
                                        product_id TEXT,
                                        seller_id TEXT
                                        );
             ''')
    conn.commit()
    return

def insert_values():
    global conn, c
    c.execute('INSERT INTO Customers SELECT * FROM orig_customers;')
    c.execute('INSERT INTO Sellers SELECT * FROM orig_sellers;')
    c.execute('INSERT INTO Orders SELECT * FROM orig_orders;')
    c.execute('INSERT INTO Order_items SELECT * FROM orig_order_items;')
    conn.commit()
    return

def drop_tables():
    global conn, c
    c.execute('DROP TABLE IF EXISTS Customers;')
    c.execute('DROP TABLE IF EXISTS Sellers;')
    c.execute('DROP TABLE IF EXISTS Orders;')
    c.execute('DROP TABLE IF EXISTS Order_items;')
    conn.commit()
    return

def rename2():
    global conn, c
    c.execute('ALTER TABLE orig_Customers RENAME TO Customers;')
    c.execute('ALTER TABLE orig_Sellers RENAME TO Sellers;')
    c.execute('ALTER TABLE orig_Orders RENAME TO Orders;')
    c.execute('ALTER TABLE orig_Order_items RENAME TO Order_items;')
    conn.commit()
    return

def self_optimized():
    global conn, c
    c.execute('PRAGMA foreign_keys=ON;')
    c.execute('PRAGMA automatic_index = ON;')
    conn.commit()
    return

def user_optimized():
    global conn, c
    c.execute('PRAGMA foreign_keys=ON;')
    c.execute('CREATE INDEX orderid ON Orders(order_id);')
    c.execute('CREATE INDEX customerid ON Orders(customer_id);')
    conn.commit()
    return

def drop_index():
    global conn, c
    c.execute('DROP INDEX orderid;')
    c.execute('DROP INDEX customerid;')
    return

def Q1():
    global conn, c
    c.execute('SELECT customer_postal_code FROM Customers ORDER BY random() LIMIT 1')
    cpc = c.fetchone()
    conn.commit()
    c.execute('''SELECT order_id
                 FROM Customers, Orders
                 WHERE Orders.customer_id = Customers.customer_id
                 AND customer_postal_code = ?;''', (cpc))
    rows = c.fetchall()
    a = 0
    total = 0
    for i in rows:
        oid = rows[a]
        c.execute('''SELECT COUNT(DISTINCT Order_items.order_id)
                     FROM Order_items, Orders
                     WHERE Order_items.order_id = Orders.order_id
                     AND order_item_id>1 AND Order_items.order_id=?;''', (oid))
        count = c.fetchone()
        a = a + 1
        total = total + count[0]
    conn.commit()
    return

def avg_time():
    start = time.time()
    for i in range(50):
        Q1()
    end = time.time()
    avg = ((end-start)/50)* 10**3
    print(avg)
    return avg

def create_graph(small, medium, large):
    db = ("Small", "Medium", "Large")
    small1 = np.fromiter(small, float)
    medium1 = np.fromiter(medium, float)
    large1 = np.fromiter(large, float)
    avgtime = {
                  "Uninformed": np.array([small1[0], medium1[0], large1[0]]),
                  "Self-optimized": np.array([small1[1], medium1[1], large1[1]]),
                  "User-optimized": np.array([small1[2], medium1[2], large1[2]])
               }
    width = 0.5
    fig, ax = plt.subplots()
    bottom = np.zeros(3)
    for boolean, avgtime in avgtime.items():
        p = ax.bar(db, avgtime, width, label=boolean, bottom=bottom)
        bottom += avgtime
    ax.set_title("Average time taken to run the three scenarios")
    ax.legend(loc="upper left")
    plt.xlabel("Databases")
    plt.ylabel("Average Time in ms")
    plt.show()
    return

def database(size):
    global conn, c
    path = size
    connect(path)
    rename1()
    uninformed()
    insert_values()
    a = avg_time()
    drop_tables()
    rename2()
    conn.close()
    path = size
    connect(path)
    self_optimized()   
    b = avg_time()
    conn.close()
    path = size
    connect(path)
    user_optimized()   
    d = avg_time()
    drop_index()
    conn.close()
    return [a, b, d]

def main():
    global conn, c
    size = "./A3Small.db"
    small = database(size)
    size = "./A3Medium.db"
    medium = database(size)
    size = "./A3Large.db"
    large = database(size)
    create_graph(small, medium, large)

if __name__ == "__main__":
    main
