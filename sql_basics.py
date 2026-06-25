# ============================================================
# sql and sqlite data analysis tutorial
# ============================================================

# this file teaches sql for data analysis using python and sqlite.
# every topic follows this structure:
# 1. concept explanation
# 2. general formula
# 3. working example

# sql means structured query language.
# sql is used to create, read, update, delete, clean, join, and analyze data.

# sqlite is a small database system.
# it stores data in a local file such as ecommerce.db.

# python communicates with sqlite using the sqlite3 module.

import sqlite3


# ============================================================
# 1. connect to a database
# ============================================================

# concept:
# before using a database, python must connect to it.
# if the database file does not exist, sqlite creates it.

# general formula:
# connection = sqlite3.connect("database_name.db")
# cursor = connection.cursor()

# example:

conn = sqlite3.connect("ecommerce.db")

cursor = conn.cursor()

# foreign keys are disabled by default in sqlite.
# this turns them on.

cursor.execute("pragma foreign_keys = on")


# ============================================================
# 2. helper function
# ============================================================

# concept:
# many select queries return rows.
# this helper prints the result nicely.

# general formula:
# def function_name(title, rows):
#     print title
#     loop through rows
#     print each row

# example:

def show(title, rows):
    print("\n" + title)
    print("-" * len(title))
    for row in rows:
        print(row)


# ============================================================
# 3. database concepts
# ============================================================

# concept:
# a database contains tables.
# a table contains rows and columns.

# example:
# customers table
#
# customer_id | customer_name | city
# 1           | Sara Ahmed    | New York
# 2           | John Smith    | Boston

# column:
# a column is one type of information.
# example: customer_name

# row:
# a row is one record.
# example: one customer

# data type:
# a data type tells sqlite what kind of data is stored.

# common sqlite data types:
# integer -> whole number
# real    -> decimal number
# text    -> words or dates stored as text
# null    -> missing value

# primary key:
# a primary key uniquely identifies each row.

# foreign key:
# a foreign key is a column in one table that points to a primary key in another table.

# general foreign key formula:
# foreign key (column_in_this_table)
# references other_table(column_in_other_table)

# simple foreign key meaning:
# child_table.foreign_key_column -> parent_table.primary_key_column

# example:
# orders.customer_id -> customers.customer_id

# this means:
# every customer_id inside orders must already exist inside customers.


# ============================================================
# 4. table grain
# ============================================================

# concept:
# table grain means what one row represents.
# always know the grain before writing joins.

# in this project:
# customers   -> one row per customer
# products    -> one row per product
# orders      -> one row per order
# order_items -> one row per product inside an order

# example:
# one order can contain many products.
# so one order can have many rows in order_items.


# ============================================================
# 5. delete old tables
# ============================================================

# concept:
# this makes the script restart cleanly.
# child tables must be dropped before parent tables.

# general formula:
# drop table if exists table_name

# example:

cursor.execute("drop table if exists order_items")
cursor.execute("drop table if exists orders")
cursor.execute("drop table if exists products")
cursor.execute("drop table if exists customers")

conn.commit()


# ============================================================
# 6. create table
# ============================================================

# concept:
# create table makes a new table.

# general formula:
# create table table_name (
#     column_name data_type constraint,
#     column_name data_type constraint
# )

# example:
# create a customers table.

cursor.execute("""
create table customers (
    customer_id integer primary key,
    customer_name text,
    city text,
    signup_date text
)
""")


# ============================================================
# 7. primary key
# ============================================================

# concept:
# primary key uniquely identifies each row.
# no two rows should have the same primary key.

# general formula:
# column_name integer primary key

# example:
# customer_id integer primary key

# meaning:
# each customer has a unique customer_id.


# ============================================================
# 8. create products table
# ============================================================

# concept:
# products stores product information.

# general formula:
# create table products (
#     product_id integer primary key,
#     product_name text,
#     category text,
#     unit_price real
# )

# example:

cursor.execute("""
create table products (
    product_id integer primary key,
    product_name text,
    category text,
    unit_price real
)
""")


# ============================================================
# 9. create orders table with foreign key
# ============================================================

# concept:
# orders belong to customers.
# therefore, orders needs customer_id.

# parent table:
# customers

# child table:
# orders

# general foreign key formula:
# foreign key (column_in_child_table)
# references parent_table(primary_key_column)

# example:
# foreign key (customer_id) references customers(customer_id)

# meaning:
# orders.customer_id must match a real customers.customer_id.

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
# 10. create order_items table with foreign keys
# ============================================================

# concept:
# order_items connects orders and products.
# each row says:
# this order included this product with this quantity.

# parent table 1:
# orders

# parent table 2:
# products

# child table:
# order_items

# general formula:
# foreign key (child_column)
# references parent_table(parent_column)

# examples:
# foreign key (order_id) references orders(order_id)
# foreign key (product_id) references products(product_id)

# meaning:
# order_items.order_id must exist in orders.order_id.
# order_items.product_id must exist in products.product_id.

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
# insert into adds data to a table.

# general formula:
# insert into table_name (column1, column2)
# values (?, ?)

# ? is a placeholder.
# placeholders safely receive python values.

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

# general formula:
# cursor.executemany("""
# insert into table_name (column1, column2)
# values (?, ?)
# """, list_of_tuples)

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
# each order belongs to one customer.
# customer_id is the foreign key.

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
# each row in order_items is one product inside one order.

# example:
# (1, 1001, 101, 1)
# means:
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
# commit permanently saves changes.

# general formula:
# connection.commit()

# example:

conn.commit()


# ============================================================
# 17. select all columns
# ============================================================

# concept:
# select reads data from a table.
# * means all columns.

# general formula:
# select *
# from table_name

# example:

cursor.execute("""
select *
from customers
""")

rows = cursor.fetchall()

show("all customers", rows)


# ============================================================
# 18. select specific columns
# ============================================================

# concept:
# usually analysts do not need all columns.
# select only the columns you need.

# general formula:
# select column1, column2
# from table_name

# example:

cursor.execute("""
select customer_name, city
from customers
""")

rows = cursor.fetchall()

show("customer names and cities", rows)


# ============================================================
# 19. column alias
# ============================================================

# concept:
# alias means temporary output name.
# it does not rename the real database column.

# general formula:
# select column_name as new_name
# from table_name

# example:

cursor.execute("""
select customer_name as name,
       city as customer_city
from customers
""")

rows = cursor.fetchall()

show("column alias example", rows)


# ============================================================
# 20. where
# ============================================================

# concept:
# where filters rows.

# general formula:
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

show("customers from new york", rows)


# ============================================================
# 21. comparison operators
# ============================================================

# concept:
# comparison operators compare values.

# general formula:
# where column operator value

# operators:
# =   equal
# <>  not equal
# >   greater than
# <   less than
# >=  greater than or equal
# <=  less than or equal

# example:

cursor.execute("""
select product_name, unit_price
from products
where unit_price > ?
""", (100,))

rows = cursor.fetchall()

show("products more expensive than 100", rows)


# ============================================================
# 22. and
# ============================================================

# concept:
# and means both conditions must be true.

# general formula:
# where condition1
#   and condition2

# example:

cursor.execute("""
select product_name, category, unit_price
from products
where category = ?
  and unit_price > ?
""", ("Electronics", 200))

rows = cursor.fetchall()

show("electronics products over 200", rows)


# ============================================================
# 23. or
# ============================================================

# concept:
# or means at least one condition must be true.

# general formula:
# where condition1
#    or condition2

# example:

cursor.execute("""
select customer_name, city
from customers
where city = ?
   or city = ?
""", ("New York", "Boston"))

rows = cursor.fetchall()

show("customers from new york or boston", rows)


# ============================================================
# 24. in
# ============================================================

# concept:
# in checks whether a value is inside a list.

# general formula:
# where column_name in (value1, value2, value3)

# example:

cursor.execute("""
select customer_name, city
from customers
where city in (?, ?)
""", ("New York", "Boston"))

rows = cursor.fetchall()

show("customers from selected cities", rows)


# ============================================================
# 25. like
# ============================================================

# concept:
# like searches text patterns.
# % means any characters.

# general formula:
# where column_name like pattern

# examples:
# 'Pen%'  -> starts with Pen
# '%Pen'  -> ends with Pen
# '%Pen%' -> contains Pen

# working example:

cursor.execute("""
select product_name
from products
where product_name like ?
""", ("%Pen%",))

rows = cursor.fetchall()

show("products containing pen", rows)


# ============================================================
# 26. date filtering
# ============================================================

# concept:
# sqlite can store dates as text in yyyy-mm-dd format.
# this format sorts correctly.

# general formula:
# where date_column >= 'yyyy-mm-dd'

# example:

cursor.execute("""
select order_id, order_date, status
from orders
where order_date >= ?
""", ("2024-03-01",))

rows = cursor.fetchall()

show("orders from march 2024 or later", rows)


# ============================================================
# 27. between
# ============================================================

# concept:
# between filters values inside a range.

# general formula:
# where column_name between low_value and high_value

# example:

cursor.execute("""
select order_id, order_date
from orders
where order_date between ? and ?
""", ("2024-01-01", "2024-01-31"))

rows = cursor.fetchall()

show("orders in january", rows)


# ============================================================
# 28. order by
# ============================================================

# concept:
# order by sorts results.

# general formula:
# order by column_name asc
# order by column_name desc

# asc means low to high.
# desc means high to low.

# example:

cursor.execute("""
select product_name, unit_price
from products
order by unit_price desc
""")

rows = cursor.fetchall()

show("products from most expensive to cheapest", rows)


# ============================================================
# 29. limit
# ============================================================

# concept:
# limit restricts how many rows come back.

# general formula:
# limit number_of_rows

# example:

cursor.execute("""
select product_name, unit_price
from products
order by unit_price desc
limit 3
""")

rows = cursor.fetchall()

show("top 3 most expensive products", rows)


# ============================================================
# 30. count
# ============================================================

# concept:
# count counts rows.

# general formula:
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
# 31. count with where
# ============================================================

# concept:
# combine count with where to count only selected rows.

# general formula:
# select count(*)
# from table_name
# where condition

# example:

cursor.execute("""
select count(*)
from orders
where status = ?
""", ("completed",))

completed_orders = cursor.fetchone()[0]

print("\ncompleted orders")
print(completed_orders)


# ============================================================
# 32. sum
# ============================================================

# concept:
# sum adds numeric values.

# general formula:
# select sum(column_name)
# from table_name

# example:

cursor.execute("""
select sum(quantity)
from order_items
""")

total_items = cursor.fetchone()[0]

print("\ntotal items ordered")
print(total_items)


# ============================================================
# 33. avg
# ============================================================

# concept:
# avg calculates the average.

# general formula:
# select avg(column_name)
# from table_name

# example:

cursor.execute("""
select avg(unit_price)
from products
""")

average_price = cursor.fetchone()[0]

print("\naverage product price")
print(average_price)


# ============================================================
# 34. min and max
# ============================================================

# concept:
# min finds the smallest value.
# max finds the largest value.

# general formula:
# select min(column_name), max(column_name)
# from table_name

# example:

cursor.execute("""
select min(unit_price), max(unit_price)
from products
""")

lowest_price, highest_price = cursor.fetchone()

print("\nlowest and highest product price")
print(lowest_price, highest_price)


# ============================================================
# 35. distinct
# ============================================================

# concept:
# distinct removes duplicates.

# general formula:
# select distinct column_name
# from table_name

# example:

cursor.execute("""
select distinct city
from customers
""")

rows = cursor.fetchall()

show("unique customer cities", rows)


# ============================================================
# 36. group by
# ============================================================

# concept:
# group by summarizes rows with the same value.

# general formula:
# select group_column, aggregate_function(column)
# from table_name
# group by group_column

# example:

cursor.execute("""
select city,
       count(*) as customer_count
from customers
group by city
""")

rows = cursor.fetchall()

show("number of customers by city", rows)


# ============================================================
# 37. having
# ============================================================

# concept:
# where filters rows before grouping.
# having filters groups after grouping.

# general formula:
# select group_column, aggregate_function(column)
# from table_name
# group by group_column
# having aggregate_condition

# example:

cursor.execute("""
select city,
       count(*) as customer_count
from customers
group by city
having count(*) >= 2
""")

rows = cursor.fetchall()

show("cities with at least 2 customers", rows)


# ============================================================
# 38. null
# ============================================================

# concept:
# null means missing value.
# do not use = null.
# use is null or is not null.

# general formula:
# where column_name is null
# where column_name is not null

# example:

cursor.execute("""
select customer_name, city
from customers
where city is null
""")

rows = cursor.fetchall()

show("customers with missing city", rows)


# ============================================================
# 39. coalesce
# ============================================================

# concept:
# coalesce replaces null with another value.

# general formula:
# coalesce(column_name, replacement_value)

# example:

cursor.execute("""
select customer_name,
       coalesce(city, 'Unknown') as cleaned_city
from customers
""")

rows = cursor.fetchall()

show("customers with cleaned city", rows)


# ============================================================
# 40. case when
# ============================================================

# concept:
# case when creates conditional labels.

# general formula:
# case
#     when condition1 then result1
#     when condition2 then result2
#     else result3
# end as new_column_name

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

show("product price levels", rows)


# ============================================================
# 41. inner join
# ============================================================

# concept:
# join combines matching rows from two tables.
# inner join only keeps rows that match in both tables.

# general formula:
# select columns
# from table1
# join table2
# on table1.common_column = table2.common_column

# example:
# orders.customer_id connects to customers.customer_id.

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

show("orders with customer names", rows)


# ============================================================
# 42. left join
# ============================================================

# concept:
# left join keeps all rows from the left table.
# if no match exists, sqlite returns null for the right table.

# general formula:
# select columns
# from left_table
# left join right_table
# on left_table.column = right_table.column

# example:
# keep all customers, even customers with no orders.

cursor.execute("""
select customers.customer_name,
       orders.order_id
from customers
left join orders
on customers.customer_id = orders.customer_id
""")

rows = cursor.fetchall()

show("all customers with possible orders", rows)


# ============================================================
# 43. find rows with no match
# ============================================================

# concept:
# left join plus is null finds missing matches.

# general formula:
# select columns
# from left_table
# left join right_table
# on left_table.id = right_table.id
# where right_table.id is null

# example:
# find customers who never placed any order.

cursor.execute("""
select customers.customer_id,
       customers.customer_name
from customers
left join orders
on customers.customer_id = orders.customer_id
where orders.order_id is null
""")

rows = cursor.fetchall()

show("customers with no orders", rows)


# ============================================================
# 44. calculated fields
# ============================================================

# concept:
# sql can calculate new columns.

# general formula:
# select column1,
#        column2,
#        column1 * column2 as new_column
# from table_name

# example:
# revenue = quantity * unit_price.

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

show("line item revenue", rows)


# ============================================================
# 45. total revenue from completed orders
# ============================================================

# concept:
# real sales analysis should ignore cancelled orders.
# revenue comes from completed orders only.

# general formula:
# select sum(quantity * price)
# from joined_tables
# where status = 'completed'

# example:

cursor.execute("""
select sum(order_items.quantity * products.unit_price) as total_revenue
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
# 46. revenue by category
# ============================================================

# concept:
# combine join, sum, group by, and order by.

# general formula:
# select category,
#        sum(quantity * price) as revenue
# from joined_tables
# where condition
# group by category
# order by revenue desc

# example:

cursor.execute("""
select products.category,
       sum(order_items.quantity * products.unit_price) as category_revenue
from orders
join order_items
on orders.order_id = order_items.order_id
join products
on order_items.product_id = products.product_id
where orders.status = 'completed'
group by products.category
order by category_revenue desc
""")

rows = cursor.fetchall()

show("revenue by category", rows)


# ============================================================
# 47. revenue by product
# ============================================================

# concept:
# this shows which products generated the most money.

# general formula:
# select product_name,
#        sum(quantity * price) as revenue
# from joined_tables
# group by product_name
# order by revenue desc

# example:

cursor.execute("""
select products.product_name,
       sum(order_items.quantity * products.unit_price) as product_revenue
from orders
join order_items
on orders.order_id = order_items.order_id
join products
on order_items.product_id = products.product_id
where orders.status = 'completed'
group by products.product_name
order by product_revenue desc
""")

rows = cursor.fetchall()

show("revenue by product", rows)


# ============================================================
# 48. total spending by customer
# ============================================================

# concept:
# customer spending needs four tables:
# customers -> orders -> order_items -> products

# general formula:
# select customer,
#        sum(quantity * price) as total_spent
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

show("total spending by customer", rows)


# ============================================================
# 49. subquery
# ============================================================

# concept:
# a subquery is a query inside another query.

# general formula:
# select columns
# from table_name
# where column > (
#     select aggregate_function(column)
#     from table_name
# )

# example:
# find products more expensive than the average product price.

cursor.execute("""
select product_name, unit_price
from products
where unit_price > (
    select avg(unit_price)
    from products
)
order by unit_price desc
""")

rows = cursor.fetchall()

show("products above average price", rows)


# ============================================================
# 50. common table expression
# ============================================================

# concept:
# a cte is a temporary named result.
# it makes complex queries easier to read.

# general formula:
# with cte_name as (
#     select ...
# )
# select *
# from cte_name

# example:
# first calculate customer revenue.
# then filter customers who spent more than 500.

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
order by total_spent desc
""")

rows = cursor.fetchall()

show("customers who spent more than 500", rows)


# ============================================================
# 51. average order value
# ============================================================

# concept:
# average order value means average revenue per order.
# first calculate revenue per order.
# then average those order totals.

# general formula:
# with order_totals as (
#     select order_id,
#            sum(quantity * price) as order_total
#     from joined_tables
#     group by order_id
# )
# select avg(order_total)
# from order_totals

# example:

cursor.execute("""
with order_totals as (
    select orders.order_id,
           sum(order_items.quantity * products.unit_price) as order_total
    from orders
    join order_items
    on orders.order_id = order_items.order_id
    join products
    on order_items.product_id = products.product_id
    where orders.status = 'completed'
    group by orders.order_id
)
select avg(order_total)
from order_totals
""")

average_order_value = cursor.fetchone()[0]

print("\naverage order value")
print(average_order_value)


# ============================================================
# 52. window function: rank
# ============================================================

# concept:
# window functions calculate across rows without collapsing rows.
# rank gives a ranking based on a value.

# general formula:
# rank() over (
#     order by column_name desc
# ) as rank_column

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

show("customer spending rank", rows)


# ============================================================
# 53. window function: row_number
# ============================================================

# concept:
# row_number gives each row a number.
# partition by restarts numbering for each group.

# general formula:
# row_number() over (
#     partition by group_column
#     order by sort_column
# ) as row_number_column

# example:
# number each customer's completed orders.

cursor.execute("""
select order_id,
       customer_id,
       order_date,
       row_number() over (
           partition by customer_id
           order by order_date
       ) as order_number_for_customer
from orders
where status = 'completed'
""")

rows = cursor.fetchall()

show("order number per customer", rows)


# ============================================================
# 54. date analysis with strftime
# ============================================================

# concept:
# sqlite uses strftime to extract parts of a date.
# '%Y-%m' extracts year and month.

# general formula:
# strftime('%Y-%m', date_column)

# example:
# calculate monthly revenue.

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

show("monthly revenue", rows)


# ============================================================
# 55. monthly completed orders
# ============================================================

# concept:
# count completed orders by month.

# general formula:
# select month,
#        count(*) as order_count
# from orders
# where status = 'completed'
# group by month

# example:

cursor.execute("""
select strftime('%Y-%m', order_date) as order_month,
       count(*) as completed_orders
from orders
where status = 'completed'
group by strftime('%Y-%m', order_date)
order by order_month
""")

rows = cursor.fetchall()

show("monthly completed orders", rows)


# ============================================================
# 56. first and latest order date
# ============================================================

# concept:
# min(date) gives the first date.
# max(date) gives the latest date.

# general formula:
# select group_column,
#        min(date_column),
#        max(date_column)
# from table_name
# group by group_column

# example:

cursor.execute("""
select customers.customer_name,
       min(orders.order_date) as first_order_date,
       max(orders.order_date) as latest_order_date
from customers
join orders
on customers.customer_id = orders.customer_id
where orders.status = 'completed'
group by customers.customer_name
""")

rows = cursor.fetchall()

show("first and latest completed order per customer", rows)


# ============================================================
# 57. customers with more than one completed order
# ============================================================

# concept:
# use group by plus having to filter customers after counting.

# general formula:
# select customer,
#        count(order_id)
# from orders
# group by customer
# having count(order_id) > 1

# example:

cursor.execute("""
select customers.customer_id,
       customers.customer_name,
       count(orders.order_id) as completed_order_count
from customers
join orders
on customers.customer_id = orders.customer_id
where orders.status = 'completed'
group by customers.customer_id,
         customers.customer_name
having count(orders.order_id) > 1
""")

rows = cursor.fetchall()

show("customers with more than one completed order", rows)


# ============================================================
# 58. rank products inside each category
# ============================================================

# concept:
# partition by ranks separately inside each group.
# here, each category gets its own ranking.

# general formula:
# rank() over (
#     partition by group_column
#     order by value_column desc
# )

# example:

cursor.execute("""
with product_revenue as (
    select products.category,
           products.product_name,
           sum(order_items.quantity * products.unit_price) as revenue
    from orders
    join order_items
    on orders.order_id = order_items.order_id
    join products
    on order_items.product_id = products.product_id
    where orders.status = 'completed'
    group by products.category,
             products.product_name
)
select category,
       product_name,
       revenue,
       rank() over (
           partition by category
           order by revenue desc
       ) as rank_inside_category
from product_revenue
order by category, rank_inside_category
""")

rows = cursor.fetchall()

show("products ranked by revenue inside each category", rows)


# ============================================================
# 59. revenue by price level
# ============================================================

# concept:
# combine case when with revenue analysis.

# general formula:
# select case when ... end as group_name,
#        sum(metric) as total_metric
# from tables
# group by group_name

# example:

cursor.execute("""
select case
           when products.unit_price >= 500 then 'High'
           when products.unit_price >= 100 then 'Medium'
           else 'Low'
       end as price_level,
       sum(order_items.quantity * products.unit_price) as revenue
from orders
join order_items
on orders.order_id = order_items.order_id
join products
on order_items.product_id = products.product_id
where orders.status = 'completed'
group by price_level
order by revenue desc
""")

rows = cursor.fetchall()

show("revenue by price level", rows)


# ============================================================
# 60. final customer summary query
# ============================================================

# concept:
# this is the main project-style query.
# it combines:
# left join
# aggregation
# count distinct
# sum
# min
# max
# coalesce
# cte
# rank window function

# goal:
# create one summary row per customer.

# general formula:
# with summary as (
#     select customer fields,
#            aggregate metrics
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
           count(distinct orders.order_id) as number_of_completed_orders,
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
       number_of_completed_orders,
       total_spent,
       first_order_date,
       latest_order_date,
       rank() over (order by total_spent desc) as customer_rank_by_spending
from customer_summary
order by customer_rank_by_spending
""")

rows = cursor.fetchall()

show("final customer summary", rows)


# ============================================================
# 61. update
# ============================================================

# concept:
# update changes existing rows.

# general formula:
# update table_name
# set column_name = new_value
# where condition

# warning:
# always use where unless you want to update every row.

# example:

cursor.execute("""
update products
set unit_price = ?
where product_name = ?
""", (155.00, "Headphones"))

conn.commit()

cursor.execute("""
select product_name, unit_price
from products
where product_name = ?
""", ("Headphones",))

rows = cursor.fetchall()

show("updated headphones price", rows)


# ============================================================
# 62. delete
# ============================================================

# concept:
# delete removes rows.

# general formula:
# delete from table_name
# where condition

# warning:
# without where, delete removes all rows from the table.

# example:
# this example deletes nothing because Temporary Product does not exist.
# it is safe.

cursor.execute("""
delete from products
where product_name = ?
""", ("Temporary Product",))

conn.commit()


# ============================================================
# 63. sql execution order
# ============================================================

# concept:
# sql is written in one order but logically runs in another order.

# written order:
# select
# from
# join
# where
# group by
# having
# order by
# limit

# logical execution order:
# from and join
# where
# group by
# having
# select
# order by
# limit

# why this matters:
# where filters raw rows.
# having filters grouped results.


# ============================================================
# 64. project tasks
# ============================================================

# solve these without looking at the examples above.

# task 1:
# show all customers.

# task 2:
# show products from most expensive to cheapest.

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
# find the top 3 products by revenue.

# task 9:
# calculate total spending by each customer.

# task 10:
# find customers with no completed orders.

# task 11:
# find each customer's first completed order date.

# task 12:
# calculate monthly revenue.

# task 13:
# calculate average order value.

# task 14:
# rank customers by total spending.

# task 15:
# create the final customer summary query.


# ============================================================
# 65. final summary
# ============================================================

# create table       -> create a table
# primary key        -> unique id for each row
# foreign key        -> column pointing to another table's primary key
# insert into        -> add rows
# executemany        -> add many rows
# commit             -> save changes
# select             -> read data
# where              -> filter rows
# and / or           -> combine conditions
# in                 -> match multiple values
# like               -> search text
# between            -> filter ranges
# order by           -> sort rows
# limit              -> restrict rows
# count              -> count rows
# sum                -> add values
# avg                -> compute average
# min / max          -> find smallest / largest values
# distinct           -> remove duplicates
# group by           -> summarize rows
# having             -> filter grouped results
# is null            -> find missing values
# coalesce           -> replace missing values
# case when          -> create conditional labels
# join               -> combine matching rows
# left join          -> keep unmatched left-table rows
# calculated field   -> create new value from existing columns
# subquery           -> query inside another query
# cte                -> temporary named query
# window function    -> rank or number rows without collapsing them
# strftime           -> analyze dates in sqlite
# update             -> modify rows
# delete             -> remove rows
# close              -> close database connection


# ============================================================
# 66. close database
# ============================================================

# concept:
# close the connection when finished.

# general formula:
# connection.close()

# example:

conn.close()
