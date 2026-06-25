# ============================================================
# all sql and sqlite data analysis notes
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

# connect to a database file.
# if the file does not exist, sqlite creates it.

conn = sqlite3.connect("ecommerce.db")

# create a cursor.
# the cursor sends sql commands to sqlite.

cursor = conn.cursor()


# ============================================================
# 2. create tables
# ============================================================

# this project uses four tables:
# customers    -> one row per customer
# products     -> one row per product
# orders       -> one row per order
# order_items  -> one row per product inside an order

cursor.execute("""
create table if not exists customers (
    customer_id integer primary key,
    customer_name text,
    city text,
    signup_date text
)
""")

cursor.execute("""
create table if not exists products (
    product_id integer primary key,
    product_name text,
    category text,
    unit_price real
)
""")

cursor.execute("""
create table if not exists orders (
    order_id integer primary key,
    customer_id integer,
    order_date text,
    status text,
    foreign key (customer_id) references customers(customer_id)
)
""")

cursor.execute("""
create table if not exists order_items (
    order_item_id integer primary key,
    order_id integer,
    product_id integer,
    quantity integer,
    foreign key (order_id) references orders(order_id),
    foreign key (product_id) references products(product_id)
)
""")


# ============================================================
# 3. clear old data
# ============================================================

# this prevents duplicate data when the script is run many times.

cursor.execute("delete from order_items")
cursor.execute("delete from orders")
cursor.execute("delete from products")
cursor.execute("delete from customers")

conn.commit()


# ============================================================
# 4. insert customer data
# ============================================================

customers = [
    (1, "Sara Ahmed", "New York", "2024-01-10"),
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
# 5. insert product data
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
# 6. insert order data
# ============================================================

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
# 7. insert order item data
# ============================================================

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

conn.commit()


# ============================================================
# 8. helper function for printing results
# ============================================================

# this function prints a title and all rows returned by a query.

def show(title, rows):
    print("\n" + title)
    for row in rows:
        print(row)


# ============================================================
# 9. select all rows
# ============================================================

# select reads data.
# * means all columns.

cursor.execute("""
select *
from customers
""")

rows = cursor.fetchall()

show("all customers", rows)


# ============================================================
# 10. select specific columns
# ============================================================

cursor.execute("""
select customer_name, city
from customers
""")

rows = cursor.fetchall()

show("customer names and cities", rows)


# ============================================================
# 11. column aliases
# ============================================================

# as renames columns in the output.

cursor.execute("""
select customer_name as name,
       city as customer_city
from customers
""")

rows = cursor.fetchall()

show("column alias example", rows)


# ============================================================
# 12. where
# ============================================================

# where filters rows.

cursor.execute("""
select *
from customers
where city = ?
""", ("New York",))

rows = cursor.fetchall()

show("customers from new york", rows)


# ============================================================
# 13. comparison operators
# ============================================================

# common comparison operators:
# = equal
# <> not equal
# > greater than
# < less than
# >= greater than or equal
# <= less than or equal

cursor.execute("""
select product_name, unit_price
from products
where unit_price > ?
""", (100,))

rows = cursor.fetchall()

show("products more expensive than 100", rows)


# ============================================================
# 14. and
# ============================================================

# and requires both conditions to be true.

cursor.execute("""
select product_name, category, unit_price
from products
where category = ?
  and unit_price > ?
""", ("Electronics", 200))

rows = cursor.fetchall()

show("electronics products over 200", rows)


# ============================================================
# 15. or
# ============================================================

# or requires at least one condition to be true.

cursor.execute("""
select customer_name, city
from customers
where city = ?
   or city = ?
""", ("New York", "Boston"))

rows = cursor.fetchall()

show("customers from new york or boston", rows)


# ============================================================
# 16. in
# ============================================================

# in is a cleaner way to check multiple possible values.

cursor.execute("""
select customer_name, city
from customers
where city in (?, ?)
""", ("New York", "Boston"))

rows = cursor.fetchall()

show("customers from selected cities", rows)


# ============================================================
# 17. like
# ============================================================

# like searches text patterns.
# % means any characters.

cursor.execute("""
select product_name
from products
where product_name like ?
""", ("%Pen%",))

rows = cursor.fetchall()

show("products containing pen", rows)


# ============================================================
# 18. date filtering
# ============================================================

# sqlite stores dates as text when using yyyy-mm-dd format.
# this format still sorts correctly.

cursor.execute("""
select order_id, order_date, status
from orders
where order_date >= ?
""", ("2024-03-01",))

rows = cursor.fetchall()

show("orders from march 2024 or later", rows)


# ============================================================
# 19. between
# ============================================================

# between filters values inside a range.

cursor.execute("""
select order_id, order_date
from orders
where order_date between ? and ?
""", ("2024-01-01", "2024-01-31"))

rows = cursor.fetchall()

show("orders in january", rows)


# ============================================================
# 20. order by
# ============================================================

# order by sorts rows.
# desc sorts from highest to lowest.

cursor.execute("""
select product_name, unit_price
from products
order by unit_price desc
""")

rows = cursor.fetchall()

show("products from most expensive to cheapest", rows)


# ============================================================
# 21. limit
# ============================================================

# limit restricts the number of rows returned.

cursor.execute("""
select product_name, unit_price
from products
order by unit_price desc
limit 3
""")

rows = cursor.fetchall()

show("top 3 most expensive products", rows)


# ============================================================
# 22. count
# ============================================================

# count(*) counts rows.

cursor.execute("""
select count(*)
from customers
""")

total_customers = cursor.fetchone()[0]

print("\ntotal customers")
print(total_customers)


# ============================================================
# 23. count completed orders
# ============================================================

cursor.execute("""
select count(*)
from orders
where status = ?
""", ("completed",))

completed_orders = cursor.fetchone()[0]

print("\ncompleted orders")
print(completed_orders)


# ============================================================
# 24. sum
# ============================================================

# sum adds values.

cursor.execute("""
select sum(quantity)
from order_items
""")

total_items = cursor.fetchone()[0]

print("\ntotal items ordered")
print(total_items)


# ============================================================
# 25. avg
# ============================================================

# avg computes the average.

cursor.execute("""
select avg(unit_price)
from products
""")

average_price = cursor.fetchone()[0]

print("\naverage product price")
print(average_price)


# ============================================================
# 26. min and max
# ============================================================

# min finds the smallest value.
# max finds the largest value.

cursor.execute("""
select min(unit_price), max(unit_price)
from products
""")

lowest_price, highest_price = cursor.fetchone()

print("\nlowest and highest product price")
print(lowest_price, highest_price)


# ============================================================
# 27. distinct
# ============================================================

# distinct removes duplicate values.

cursor.execute("""
select distinct city
from customers
""")

rows = cursor.fetchall()

show("unique customer cities", rows)


# ============================================================
# 28. group by
# ============================================================

# group by summarizes rows with the same value.

cursor.execute("""
select city, count(*) as customer_count
from customers
group by city
""")

rows = cursor.fetchall()

show("number of customers by city", rows)


# ============================================================
# 29. having
# ============================================================

# where filters rows before grouping.
# having filters groups after grouping.

cursor.execute("""
select city, count(*) as customer_count
from customers
group by city
having count(*) >= 2
""")

rows = cursor.fetchall()

show("cities with at least 2 customers", rows)


# ============================================================
# 30. null values
# ============================================================

# null means missing or unknown.
# use is null, not = null.

cursor.execute("""
select customer_name, city
from customers
where city is null
""")

rows = cursor.fetchall()

show("customers with missing city", rows)


# ============================================================
# 31. coalesce
# ============================================================

# coalesce replaces null with a chosen value.

cursor.execute("""
select customer_name,
       coalesce(city, 'Unknown') as cleaned_city
from customers
""")

rows = cursor.fetchall()

show("customers with cleaned city", rows)


# ============================================================
# 32. case when
# ============================================================

# case when creates conditional logic.

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
# 33. inner join
# ============================================================

# join combines rows from two tables.
# inner join returns only matching rows.

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
# 34. left join
# ============================================================

# left join keeps all rows from the left table.
# it is useful when looking for missing matches.

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
# 35. find customers with no orders
# ============================================================

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
# 36. calculated fields
# ============================================================

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
# 37. total revenue from completed orders
# ============================================================

# cancelled orders should usually be excluded from revenue analysis.

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
# 38. revenue by category
# ============================================================

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
# 39. revenue by product
# ============================================================

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
# 40. total spending by customer
# ============================================================

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
# 41. average order value
# ============================================================

# first calculate revenue per order.
# then average those order totals.

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
# 42. subquery
# ============================================================

# a subquery is a query inside another query.
# this finds products priced above the average product price.

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
# 43. common table expression
# ============================================================

# a cte creates a temporary named result.
# ctes make complex queries easier to read.

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
# 44. window function: rank
# ============================================================

# window functions calculate across rows without collapsing them.
# rank gives the same rank to ties.

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
# 45. window function: row_number
# ============================================================

# row_number numbers rows inside each group.
# partition by means restart numbering for each customer.

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
# 46. date analysis with strftime
# ============================================================

# sqlite uses strftime for date grouping.
# '%Y-%m' extracts year and month.

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
# 47. monthly completed orders
# ============================================================

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
# 48. first and latest order date per customer
# ============================================================

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
# 49. customers with more than one completed order
# ============================================================

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
# 50. rank products by revenue inside each category
# ============================================================

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
# 51. revenue by price level
# ============================================================

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
# 52. final customer summary query
# ============================================================

# this is the most important query in the tutorial.
# it combines joins, aggregation, ctes, null handling, and ranking.

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
# 53. update example
# ============================================================

# update modifies existing rows.
# this example changes a product price.

cursor.execute("""
update products
set unit_price = ?
where product_name = ?
""", (155.00, "Headphones"))

conn.commit()


# ============================================================
# 54. delete example
# ============================================================

# delete removes rows.
# be careful with delete in real databases.
# always use where unless you truly want to delete everything.

cursor.execute("""
delete from products
where product_name = ?
""", ("Temporary Product",))

conn.commit()


# ============================================================
# 55. sql execution order
# ============================================================

# sql is written like this:
# select
# from
# join
# where
# group by
# having
# order by
# limit

# sql logically runs like this:
# from and join
# where
# group by
# having
# select
# order by
# limit


# ============================================================
# 56. project tasks
# ============================================================

# if you can write these queries without looking at the answers,
# you have a solid beginner data analysis sql foundation.

# task 1: show all customers.
# task 2: show products from most expensive to cheapest.
# task 3: count customers by city.
# task 4: count completed orders.
# task 5: calculate total revenue from completed orders.
# task 6: calculate revenue by category.
# task 7: calculate revenue by product.
# task 8: find the top 3 products by revenue.
# task 9: calculate total spending by each customer.
# task 10: find customers with no completed orders.
# task 11: find each customer's first completed order date.
# task 12: calculate monthly revenue.
# task 13: calculate average order value.
# task 14: rank customers by total spending.
# task 15: create the final customer summary query.


# ============================================================
# 57. summary
# ============================================================

# create table       -> create a table
# insert into        -> add rows
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
# join               -> combine matching rows
# left join          -> keep unmatched rows from left table
# is null            -> find missing values
# coalesce           -> replace missing values
# case when          -> create conditional columns
# subquery           -> query inside another query
# cte                -> temporary named query
# window function    -> rank or compare rows without collapsing them
# strftime           -> analyze dates in sqlite
# commit             -> save changes
# close              -> close database


# ============================================================
# 58. close database
# ============================================================

# always close the connection when finished.

conn.close()
