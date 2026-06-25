# ============================================================
# sql and sqlite data analysis notes
# ============================================================

# sql stands for structured query language.
# sql is used to create, read, update, delete, clean, join, and analyze data.

# sqlite is a lightweight database system.
# it stores the database in a local file such as ecommerce.db.

# python communicates with sqlite using the sqlite3 module.

import sqlite3


# ============================================================
# 1. connect to a database
# ============================================================

# concept:
# before using a database, python must connect to it.
# if the file does not exist, sqlite creates it.

# formula:
# connection = sqlite3.connect("database_name.db")

# example:

conn = sqlite3.connect("ecommerce.db")


# ============================================================
# 2. create a cursor
# ============================================================

# concept:
# a cursor is the object that sends sql commands to the database.
# python does not send sql directly.
# python uses the cursor to execute sql.

# formula:
# cursor = connection.cursor()

# example:

cursor = conn.cursor()


# ============================================================
# 3. turn on foreign keys
# ============================================================

# concept:
# sqlite does not enforce foreign keys unless we turn them on.
# this means sqlite will check table relationships correctly.

# formula:
# cursor.execute("pragma foreign_keys = on")

# example:

cursor.execute("pragma foreign_keys = on")


# ============================================================
# 4. reset old tables
# ============================================================

# concept:
# this removes old tables so the script starts clean every time.
# delete child tables first, then parent tables.

# formula:
# drop table if exists table_name

# example:

cursor.execute("drop table if exists order_items")
cursor.execute("drop table if exists orders")
cursor.execute("drop table if exists products")
cursor.execute("drop table if exists customers")

conn.commit()


# ============================================================
# 5. basic database structure
# ============================================================

# concept:
# a database contains tables.
# a table contains columns and rows.

# example:
# customers table
#
# customer_id | customer_name | city
# 1           | Sara Ahmed    | New York
# 2           | John Smith    | Boston

# column:
# one type of information.
# example: customer_name

# row:
# one full record.
# example: one customer

# data type:
# tells sqlite what kind of data is stored.

# common sqlite types:
# integer -> whole number
# real    -> decimal number
# text    -> words or dates
# null    -> missing value


# ============================================================
# 6. create first table: customers
# ============================================================

# concept:
# create table creates a new table.
# primary key uniquely identifies each row.

# formula:
# create table table_name (
#     column_name data_type constraint,
#     column_name data_type
# )

# example:

cursor.execute("""
create table customers (
    customer_id integer primary key,
    customer_name text,
    city text,
    signup_date text
)
""")


# ============================================================
# 7. create second table: products
 
cursor.execute("""
create table products (
    product_id integer primary key,
    product_name text,
    category text,
    unit_price real
)
""")


# ============================================================
# 8. foreign key concept
# ============================================================

# concept:
# a foreign key is a column in one table that points to a row in another table.
# it creates a relationship between tables.

# formula:
# foreign key (column_in_this_table)
# references other_table(column_in_other_table)

# important:
# the column names do not have to be the same.
# but the values must match.

# example meaning:
# orders.customer_id -> customers.customer_id

# this means:
# every customer_id in orders must already exist in customers.


# ============================================================
# 9. create third table: orders
# ============================================================

# concept:
# each order belongs to one customer.
# so orders has customer_id as a foreign key.

# formula:
# foreign key (customer_id)
# references customers(customer_id)

# example:

cursor.execute("""
create table orders (
    order_id integer primary key,
    customer_id integer,
    order_date text,
    status text,
    foreign key (customer_id) references customers(customer_id)
)
""")


# ============================================================
# 10. create fourth table: order_items
# ============================================================

# concept:
# one order can contain many products.
# order_items stores the products inside each order.

# each row means:
# this order contains this product with this quantity.

# formulas:
# foreign key (order_id) references orders(order_id)
# foreign key (product_id) references products(product_id)

# example:

cursor.execute("""
create table order_items (
    order_item_id integer primary key,
    order_id integer,
    product_id integer,
    quantity integer,
    foreign key (order_id) references orders(order_id),
    foreign key (product_id) references products(product_id)
)
""")


# ============================================================
# 11. insert one row
# ============================================================

# concept:
# insert into adds new data to a table.
# ? placeholders safely receive python values.

# formula:
# insert into table_name (column1, column2)
# values (?, ?)

# example:

cursor.execute("""
insert into customers (customer_id, customer_name, city, signup_date)
values (?, ?, ?, ?)
""", (1, "Sara Ahmed", "New York", "2024-01-10"))


# ============================================================
# 12. insert multiple rows
# ============================================================

# concept:
# executemany inserts many rows at once.

# formula:
# cursor.executemany(sql_command, list_of_rows)

# example:

customers = [
    (2, "John Smith", "Boston", "2024-01-15"),
    (3, "Mina Lee", "Chicago", "2024-02-01"),
    (4, "David Kim", "New York", "2024-02-20"),
    (5, "Elena Garcia", "Austin", "2024-03-05"),
    (6, "Omar Khan", "Boston", "2024-03-18"),
    (7, "Nina Patel", "Seattle", "2024-04-02"),
    (8, "Alex NoCity", None, "2024-04-10")
]

cursor.executemany("""
insert into customers (customer_id, customer_name, city, signup_date)
values (?, ?, ?, ?)
""", customers)


# ============================================================
# 13. insert product data
# ============================================================

products = [
    (101, "Laptop", "Electronics", 1200.00),
    (102, "Headphones", "Electronics", 150.00),
    (103, "Office Chair", "Furniture", 300.00),
    (104, "Desk Lamp", "Furniture", 45.00),
    (105, "Notebook", "Stationery", 5.00),
    (106, "Pen Set", "Stationery", 12.00),
    (107, "Monitor", "Electronics", 250.00)
]

cursor.executemany("""
insert into products (product_id, product_name, category, unit_price)
values (?, ?, ?, ?)
""", products)


# ============================================================
# 14. insert order data
# ============================================================

# concept:
# orders must use customer_id values that already exist in customers.

orders = [
    (1001, 1, "2024-01-20", "completed"),
    (1002, 2, "2024-01-22", "completed"),
    (1003, 1, "2024-02-05", "completed"),
    (1004, 3, "2024-02-10", "cancelled"),
    (1005, 4, "2024-02-18", "completed"),
    (1006, 5, "2024-03-12", "completed"),
    (1007, 2, "2024-03-15", "completed"),
    (1008, 6, "2024-04-01", "completed"),
    (1009, 3, "2024-04-10", "completed")
]

cursor.executemany("""
insert into orders (order_id, customer_id, order_date, status)
values (?, ?, ?, ?)
""", orders)


# ============================================================
# 15. insert order item data
# ============================================================

# concept:
# order_items must use real order_id values and real product_id values.

# example row:
# (1, 1001, 101, 1)

# meaning:
# order_item_id = 1
# order_id = 1001
# product_id = 101
# quantity = 1

order_items = [
    (1, 1001, 101, 1),
    (2, 1001, 102, 2),
    (3, 1002, 105, 10),
    (4, 1002, 106, 5),
    (5, 1003, 107, 1),
    (6, 1003, 104, 2),
    (7, 1004, 103, 1),
    (8, 1005, 103, 2),
    (9, 1005, 104, 1),
    (10, 1006, 102, 1),
    (11, 1006, 105, 20),
    (12, 1007, 101, 1),
    (13, 1008, 107, 2),
    (14, 1008, 106, 3),
    (15, 1009, 104, 4),
    (16, 1009, 105, 15)
]

cursor.executemany("""
insert into order_items (order_item_id, order_id, product_id, quantity)
values (?, ?, ?, ?)
""", order_items)


# ============================================================
# 16. commit
# ============================================================

# concept:
# commit saves changes permanently.

# formula:
# connection.commit()

# example:

conn.commit()


# ============================================================
# 17. select all rows
# ============================================================

# concept:
# select reads data.
# * means all columns.

# formula:
# select *
# from table_name

# example:

cursor.execute("""
select *
from customers
""")

rows = cursor.fetchall()

print("\nall customers")

for row in rows:
    print(row)


# ============================================================
# 18. select specific columns
# ============================================================

# concept:
# usually we do not need every column.
# select only the columns needed.

# formula:
# select column1, column2
# from table_name

# example:

cursor.execute("""
select customer_name, city
from customers
""")

rows = cursor.fetchall()

print("\ncustomer names and cities")

for row in rows:
    print(row)


# ============================================================
# 19. where
# ============================================================

# concept:
# where filters rows.

# formula:
# select columns
# from table_name
# where condition

# example:

cursor.execute("""
select *
from customers
where city = ?
""", ("New York",))

rows = cursor.fetchall()

print("\ncustomers from new york")

for row in rows:
    print(row)


# ============================================================
# 20. order by
# ============================================================

# concept:
# order by sorts rows.
# asc means low to high.
# desc means high to low.

# formula:
# select columns
# from table_name
# order by column_name desc

# example:

cursor.execute("""
select product_name, unit_price
from products
order by unit_price desc
""")

rows = cursor.fetchall()

print("\nproducts from most expensive to cheapest")

for row in rows:
    print(row)


# ============================================================
# 21. limit
# ============================================================

# concept:
# limit restricts the number of rows returned.

# formula:
# select columns
# from table_name
# limit number

# example:

cursor.execute("""
select product_name, unit_price
from products
order by unit_price desc
limit 3
""")

rows = cursor.fetchall()

print("\ntop 3 expensive products")

for row in rows:
    print(row)


# ============================================================
# 22. count
# ============================================================

# concept:
# count counts rows.

# formula:
# select count(*)
# from table_name

# example:

cursor.execute("""
select count(*)
from customers
""")

total_customers = cursor.fetchone()[0]

print("\ntotal customers")
print(total_customers)


# ============================================================
# 23. sum and avg
# ============================================================

# concept:
# sum adds numbers.
# avg calculates average.

# formulas:
# select sum(column_name) from table_name
# select avg(column_name) from table_name

# example:

cursor.execute("""
select sum(quantity)
from order_items
""")

total_items = cursor.fetchone()[0]

print("\ntotal items ordered")
print(total_items)

cursor.execute("""
select avg(unit_price)
from products
""")

average_price = cursor.fetchone()[0]

print("\naverage product price")
print(average_price)


# ============================================================
# 24. group by
# ============================================================

# concept:
# group by summarizes rows with the same value.

# formula:
# select group_column, aggregate_function(column)
# from table_name
# group by group_column

# example:

cursor.execute("""
select city, count(*) as customer_count
from customers
group by city
""")

rows = cursor.fetchall()

print("\ncustomer count by city")

for row in rows:
    print(row)


# ============================================================
# 25. having
# ============================================================

# concept:
# where filters rows before grouping.
# having filters groups after grouping.

# formula:
# select group_column, count(*)
# from table_name
# group by group_column
# having count(*) condition

# example:

cursor.execute("""
select city, count(*) as customer_count
from customers
group by city
having count(*) >= 2
""")

rows = cursor.fetchall()

print("\ncities with at least 2 customers")

for row in rows:
    print(row)


# ============================================================
# 26. null and coalesce
# ============================================================

# concept:
# null means missing value.
# use is null, not = null.
# coalesce replaces null with another value.

# formulas:
# where column_name is null
# coalesce(column_name, replacement_value)

# example:

cursor.execute("""
select customer_name, city
from customers
where city is null
""")

rows = cursor.fetchall()

print("\ncustomers with missing city")

for row in rows:
    print(row)

cursor.execute("""
select customer_name,
       coalesce(city, 'Unknown') as cleaned_city
from customers
""")

rows = cursor.fetchall()

print("\ncustomers with cleaned city")

for row in rows:
    print(row)


# ============================================================
# 27. case when
# ============================================================

# concept:
# case when creates conditional labels.

# formula:
# case
#     when condition then result
#     else result
# end as new_column

# example:

cursor.execute("""
select product_name,
       unit_price,
       case
           when unit_price >= 500 then 'High'
           when unit_price >= 100 then 'Medium'
           else 'Low'
       end as price_level
from products
""")

rows = cursor.fetchall()

print("\nproduct price levels")

for row in rows:
    print(row)


# ============================================================
# 28. inner join
# ============================================================

# concept:
# join combines matching rows from two tables.

# formula:
# select columns
# from table1
# join table2
# on table1.column = table2.column

# example:
# orders.customer_id matches customers.customer_id.

cursor.execute("""
select orders.order_id,
       customers.customer_name,
       orders.order_date,
       orders.status
from orders
join customers
on orders.customer_id = customers.customer_id
""")

rows = cursor.fetchall()

print("\norders with customer names")

for row in rows:
    print(row)


# ============================================================
# 29. left join
# ============================================================

# concept:
# left join keeps all rows from the left table.
# if there is no match, the right table columns become null.

# formula:
# select columns
# from left_table
# left join right_table
# on left_table.column = right_table.column

# example:

cursor.execute("""
select customers.customer_name,
       orders.order_id
from customers
left join orders
on customers.customer_id = orders.customer_id
""")

rows = cursor.fetchall()

print("\nall customers with possible orders")

for row in rows:
    print(row)


# ============================================================
# 30. find rows with no match
# ============================================================

# concept:
# left join plus is null finds missing matches.

# formula:
# select columns
# from left_table
# left join right_table
# on left_table.id = right_table.id
# where right_table.id is null

# example:
# find customers with no orders.

cursor.execute("""
select customers.customer_id,
       customers.customer_name
from customers
left join orders
on customers.customer_id = orders.customer_id
where orders.order_id is null
""")

rows = cursor.fetchall()

print("\ncustomers with no orders")

for row in rows:
    print(row)


# ============================================================
# 31. calculated field
# ============================================================

# concept:
# sql can create calculated columns.
# revenue = quantity * unit_price.

# formula:
# select column1 * column2 as new_column
# from table_name

# example:

cursor.execute("""
select order_items.order_id,
       products.product_name,
       order_items.quantity,
       products.unit_price,
       order_items.quantity * products.unit_price as revenue
from order_items
join products
on order_items.product_id = products.product_id
""")

rows = cursor.fetchall()

print("\nline item revenue")

for row in rows:
    print(row)


# ============================================================
# 32. total revenue from completed orders
# ============================================================

# concept:
# cancelled orders should not count as real revenue.

# formula:
# select sum(quantity * price)
# from joined_tables
# where status = 'completed'

# example:

cursor.execute("""
select sum(order_items.quantity * products.unit_price)
from orders
join order_items
on orders.order_id = order_items.order_id
join products
on order_items.product_id = products.product_id
where orders.status = 'completed'
""")

total_revenue = cursor.fetchone()[0]

print("\ntotal revenue from completed orders")
print(total_revenue)


# ============================================================
# 33. revenue by category
# ============================================================

# concept:
# this combines join, sum, group by, and order by.

# formula:
# select category, sum(quantity * price)
# from joined_tables
# where condition
# group by category
# order by revenue desc

# example:

cursor.execute("""
select products.category,
       sum(order_items.quantity * products.unit_price) as revenue
from orders
join order_items
on orders.order_id = order_items.order_id
join products
on order_items.product_id = products.product_id
where orders.status = 'completed'
group by products.category
order by revenue desc
""")

rows = cursor.fetchall()

print("\nrevenue by category")

for row in rows:
    print(row)


# ============================================================
# 34. revenue by customer
# ============================================================

# concept:
# to find customer spending, connect:
# customers -> orders -> order_items -> products

# formula:
# select customer, sum(quantity * price)
# from customers
# join orders
# join order_items
# join products
# group by customer

# example:

cursor.execute("""
select customers.customer_id,
       customers.customer_name,
       sum(order_items.quantity * products.unit_price) as total_spent
from customers
join orders
on customers.customer_id = orders.customer_id
join order_items
on orders.order_id = order_items.order_id
join products
on order_items.product_id = products.product_id
where orders.status = 'completed'
group by customers.customer_id,
         customers.customer_name
order by total_spent desc
""")

rows = cursor.fetchall()

print("\nrevenue by customer")

for row in rows:
    print(row)


# ============================================================
# 35. common table expression
# ============================================================

# concept:
# a cte is a temporary named query.
# it makes a complex query easier to read.

# formula:
# with cte_name as (
#     select ...
# )
# select *
# from cte_name

# example:

cursor.execute("""
with customer_revenue as (
    select customers.customer_id,
           customers.customer_name,
           sum(order_items.quantity * products.unit_price) as total_spent
    from customers
    join orders
    on customers.customer_id = orders.customer_id
    join order_items
    on orders.order_id = order_items.order_id
    join products
    on order_items.product_id = products.product_id
    where orders.status = 'completed'
    group by customers.customer_id,
             customers.customer_name
)
select *
from customer_revenue
where total_spent > 500
""")

rows = cursor.fetchall()

print("\ncustomers who spent more than 500")

for row in rows:
    print(row)


# ============================================================
# 36. window function
# ============================================================

# concept:
# a window function calculates across rows without removing rows.
# rank gives a ranking.

# formula:
# rank() over (order by column_name desc)

# example:
# rank customers by total spending.

cursor.execute("""
with customer_revenue as (
    select customers.customer_id,
           customers.customer_name,
           sum(order_items.quantity * products.unit_price) as total_spent
    from customers
    join orders
    on customers.customer_id = orders.customer_id
    join order_items
    on orders.order_id = order_items.order_id
    join products
    on order_items.product_id = products.product_id
    where orders.status = 'completed'
    group by customers.customer_id,
             customers.customer_name
)
select customer_id,
       customer_name,
       total_spent,
       rank() over (order by total_spent desc) as spending_rank
from customer_revenue
""")

rows = cursor.fetchall()

print("\ncustomer spending rank")

for row in rows:
    print(row)


# ============================================================
# 37. date analysis
# ============================================================

# concept:
# sqlite uses strftime to extract parts of a date.
# '%Y-%m' means year and month.

# formula:
# strftime('%Y-%m', date_column)

# example:
# monthly revenue.

cursor.execute("""
select strftime('%Y-%m', orders.order_date) as order_month,
       sum(order_items.quantity * products.unit_price) as monthly_revenue
from orders
join order_items
on orders.order_id = order_items.order_id
join products
on order_items.product_id = products.product_id
where orders.status = 'completed'
group by strftime('%Y-%m', orders.order_date)
order by order_month
""")

rows = cursor.fetchall()

print("\nmonthly revenue")

for row in rows:
    print(row)


# ============================================================
# 38. final customer summary query
# ============================================================

# concept:
# this is the main project query.
# it creates one summary row per customer.

# it uses:
# left join
# count distinct
# sum
# min
# max
# coalesce
# cte
# rank

# formula:
# with summary as (
#     select customer fields and metrics
#     from customers
#     left join other tables
#     group by customer fields
# )
# select summary fields,
#        rank() over (order by metric desc)
# from summary

# example:

cursor.execute("""
with customer_summary as (
    select customers.customer_id,
           customers.customer_name,
           coalesce(customers.city, 'Unknown') as city,
           count(distinct orders.order_id) as completed_orders,
           coalesce(sum(order_items.quantity * products.unit_price), 0) as total_spent,
           min(orders.order_date) as first_order_date,
           max(orders.order_date) as latest_order_date
    from customers
    left join orders
    on customers.customer_id = orders.customer_id
       and orders.status = 'completed'
    left join order_items
    on orders.order_id = order_items.order_id
    left join products
    on order_items.product_id = products.product_id
    group by customers.customer_id,
             customers.customer_name,
             customers.city
)
select customer_id,
       customer_name,
       city,
       completed_orders,
       total_spent,
       first_order_date,
       latest_order_date,
       rank() over (order by total_spent desc) as customer_rank
from customer_summary
order by customer_rank
""")

rows = cursor.fetchall()

print("\nfinal customer summary")

for row in rows:
    print(row)


# ============================================================
# 39. update
# ============================================================

# concept:
# update changes existing rows.

# formula:
# update table_name
# set column_name = new_value
# where condition

# example:

cursor.execute("""
update products
set unit_price = ?
where product_name = ?
""", (155.00, "Headphones"))

conn.commit()


# ============================================================
# 40. delete
# ============================================================

# concept:
# delete removes rows.
# always use where unless you want to delete everything.

# formula:
# delete from table_name
# where condition

# example:
# this deletes nothing because the product does not exist.

cursor.execute("""
delete from products
where product_name = ?
""", ("Temporary Product",))

conn.commit()


# ============================================================
# 41. project tasks
# ============================================================

# solve these yourself.

# task 1:
# show all customers.

# task 2:
# show all products ordered by price from highest to lowest.

# task 3:
# count customers by city.

# task 4:
# count completed orders.

# task 5:
# calculate total revenue from completed orders.

# task 6:
# calculate revenue by category.

# task 7:
# calculate revenue by product.

# task 8:
# find top 3 customers by total spending.

# task 9:
# find customers with no completed orders.

# task 10:
# calculate monthly revenue.

# task 11:
# rank customers by spending.

# task 12:
# write the final customer summary query.


# ============================================================
# 42. summary
# ============================================================

# connect          -> connect python to database
# cursor           -> send sql commands to database
# execute          -> run one sql command
# executemany      -> run one insert command many times
# commit           -> save changes
# table            -> stores rows and columns
# column           -> one type of information
# row              -> one record
# primary key      -> unique id for each row
# foreign key      -> column pointing to another table
# insert into      -> add data
# select           -> read data
# where            -> filter rows
# order by         -> sort rows
# limit            -> restrict rows
# count            -> count rows
# sum              -> add numbers
# avg              -> average
# group by         -> summarize by group
# having           -> filter grouped results
# null             -> missing value
# coalesce         -> replace missing value
# case when        -> create labels
# join             -> combine matching rows
# left join        -> keep all rows from left table
# cte              -> temporary named query
# window function  -> rank or number rows
# strftime         -> date analysis
# update           -> modify rows
# delete           -> remove rows
# close            -> close database


# ============================================================
# 43. close database
# ============================================================

# concept:
# close the database connection when finished.

# formula:
# connection.close()

# example:

conn.close()
