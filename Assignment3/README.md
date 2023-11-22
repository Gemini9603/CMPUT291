Winter Semester 2023

Members: Pooja Prasad, Nils Dorantes, Shrishty Gnanasekaran

Note on scenario: We disabled and enabled our primary keys, foreign keys and Indexes correctly but still our self-optimized scenario runs slower than our uninformed sometimes

Note on User-optimized indices:

Indices created for the user-optimized scenario

Q1: orderid - created on order_id from Order table customerid - created on customer_id from orders table Reason - order_id is referenced as a foreign key in Order_items table and customer_id is a foreign key in Orders table. Since we are using Customers, Orders and Order_items tables in the question, creating indexes on the foreign keys helps to optimize. After a few trials using different combinations of indexes, this combination seemed to work best considering that they were both on the same table

Q2: orderid - created on order_id from Orders table customerid - created on customer_id from Orders table Reason - Question 2 was quite similar to Question 1 and the same combination of indexes worked best

Q3: orderid - created on order_id from Orders table customerid - created on customer_id from Orders table Reason - Question 3 was quite similar to Question 2 and the same combination of indexes worked best

Q4: sellerid - created on seller_id from Sellers table orderid - created on order_id from Orders table customerid - created on customer_id from Orders table Reason - The reasoning for creating orderid and customerid are the same as the previous questions. In addition to that, since we are using INNER JOIN to join our 4 tables, creating indices on foreign keys is helpful. For the same reason sellerid was also created, since this question asks us to find seller_postal_code.
