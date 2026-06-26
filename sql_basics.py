# ============================================================
# SQL + SQLITE STUDY NOTES
# students and majors database
# ============================================================

# SQL = Structured Query Language.
# SQL is used to create, read, update, delete, join, and analyze data.

# SQLite = lightweight database system.
# Python talks to SQLite using the sqlite3 module.

import sqlite3


# ============================================================
# 1. CONNECT TO DATABASE
# ============================================================

# Concept:
# A connection links Python to the database file.
# If the file does not exist, SQLite creates it.

# General structure:
# connection = sqlite3.connect("database_name.db")

conn = sqlite3.connect("school.db")


# ============================================================
# 2. CREATE CURSOR
# ============================================================

# Concept:
# A cursor is the object that sends SQL commands to the database.
# Python does not run SQL directly.
# Python uses cursor.execute(...) to run SQL.

# General structure:
# cursor = connection.cursor()

cursor = conn.cursor()


# ============================================================
# 3. TURN ON FOREIGN KEYS
# ============================================================

# Concept:
# A foreign key connects one table to another table.
# SQLite checks foreign keys only if we turn them on.

cursor.execute("PRAGMA foreign_keys = ON")


# ============================================================
# 4. RESET OLD TABLES
# ============================================================

# Concept:
# DROP TABLE removes a table.
# IF EXISTS avoids an error if the table does not exist.

cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS majors")

# Concept:
# commit saves changes permanently.

conn.commit()


# ============================================================
# 5. CREATE TABLES
# ============================================================

# Concept:
# Table = stores rows and columns.
# Column = one type of information.
# Row = one full record.
# Primary key = unique ID for each row.
# Foreign key = column that points to another table.

cursor.execute("""
CREATE TABLE majors (
    major_id INTEGER PRIMARY KEY,
    major_name TEXT
)
""")

cursor.execute("""
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    major_id INTEGER,
    gpa REAL,
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
)
""")

conn.commit()


# ============================================================
# 6. INSERT DATA
# ============================================================

# Concept:
# INSERT INTO adds new rows.
# ? placeholders safely receive Python values.

# execute = runs one SQL command.
# executemany = runs one SQL command many times.

majors = [
    (10, "Computer Science"),
    (20, "Business"),
    (40, "Biology")
]

students = [
    (1, "Ana", 10, 3.8),
    (2, "Ben", 20, 3.1),
    (3, "Cara", 10, 3.5),
    (4, "Dan", None, 2.9),
    (5, "Eva", 40, 3.9),
    (6, "Omar", 20, 3.7)
]

cursor.executemany("""
INSERT INTO majors (major_id, major_name)
VALUES (?, ?)
""", majors)

cursor.executemany("""
INSERT INTO students (student_id, name, major_id, gpa)
VALUES (?, ?, ?, ?)
""", students)

conn.commit()


# ============================================================
# 7. FETCHING RESULTS
# ============================================================

# Concept:
# After SELECT, the result stays inside the cursor.
# fetchall() gets all result rows.
# fetchone() gets one result row.

cursor.execute("""
SELECT *
FROM students
""")

rows = cursor.fetchall()

print("\nAll students:")
for row in rows:
    print(row)


# ============================================================
# 8. GENERAL SQL ORDER
# ============================================================

# SELECT      -> what to show
# FROM        -> main table
# JOIN        -> connect another table
# ON          -> join condition
# WHERE       -> filter rows before grouping
# GROUP BY    -> group rows
# HAVING      -> filter groups after grouping
# ORDER BY    -> sort final result
# LIMIT       -> restrict number of rows

# General structure:

"""
SELECT column_name, aggregate_function(column_name)
FROM table1
JOIN table2
ON table1.common_column = table2.common_column
WHERE row_condition
GROUP BY column_name
HAVING group_condition
ORDER BY column_name ASC/DESC
LIMIT number;
"""


# ============================================================
# 9. WHERE + ORDER BY
# ============================================================

# WHERE filters rows.
# ORDER BY sorts rows.
# DESC means high to low.
# ASC means low to high.

cursor.execute("""
SELECT name, gpa
FROM students
WHERE gpa > 3.5
ORDER BY gpa DESC
""")

print("\nStudents with GPA greater than 3.5:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 10. AGGREGATE FUNCTIONS
# ============================================================

# COUNT(*) = count rows.
# AVG(column) = average.
# MIN(column) = lowest value.
# MAX(column) = highest value.
# SUM(column) = total.

cursor.execute("""
SELECT COUNT(*)
FROM students
""")

total_students = cursor.fetchone()[0]

print("\nTotal students:")
print(total_students)


# ============================================================
# 11. GROUP BY
# ============================================================

# GROUP BY summarizes rows with the same value.

cursor.execute("""
SELECT major_id, AVG(gpa) AS average_gpa
FROM students
GROUP BY major_id
""")

print("\nAverage GPA by major_id:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 12. HAVING
# ============================================================

# WHERE filters rows before grouping.
# HAVING filters groups after grouping.

cursor.execute("""
SELECT major_id, AVG(gpa) AS average_gpa
FROM students
GROUP BY major_id
HAVING AVG(gpa) > 3.4
""")

print("\nMajor groups with average GPA greater than 3.4:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 13. JOIN TYPES
# ============================================================

# JOIN / INNER JOIN = only matching rows.
# LEFT JOIN         = all left table rows; right side may be NULL.
# RIGHT JOIN        = all right table rows; left side may be NULL.
# FULL OUTER JOIN   = all rows from both tables; either side may be NULL.
# SELF JOIN         = table joined to itself.

# General join structure:

"""
SELECT table1.column_name, table2.column_name
FROM table1
JOIN table2
ON table1.common_column = table2.common_column;
"""


# ============================================================
# 14. INNER JOIN
# ============================================================

# Concept:
# INNER JOIN shows only rows with matching values in both tables.

cursor.execute("""
SELECT s.name, m.major_name, s.gpa
FROM students s
JOIN majors m
ON s.major_id = m.major_id
""")

print("\nStudents with matching majors:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 15. LEFT JOIN
# ============================================================

# Concept:
# LEFT JOIN keeps every row from the left table.
# If there is no match, right table columns become NULL.

cursor.execute("""
SELECT s.name, m.major_name, s.gpa
FROM students s
LEFT JOIN majors m
ON s.major_id = m.major_id
""")

print("\nAll students with possible major names:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 16. COALESCE
# ============================================================

# Concept:
# COALESCE replaces NULL with another value.

# General structure:
# COALESCE(column_name, replacement_value)

cursor.execute("""
SELECT s.name,
       COALESCE(m.major_name, 'Undeclared') AS major_name,
       s.gpa
FROM students s
LEFT JOIN majors m
ON s.major_id = m.major_id
ORDER BY s.gpa DESC
""")

print("\nStudents with cleaned major names:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 17. CTE
# ============================================================

# Concept:
# CTE = Common Table Expression.
# It is a temporary named result inside one query.
# It makes long queries easier to read.

# General structure:

"""
WITH cte_name AS (
    SELECT ...
    FROM ...
)
SELECT *
FROM cte_name;
"""

cursor.execute("""
WITH strong_students AS (
    SELECT name, major_id, gpa
    FROM students
    WHERE gpa > 3.3
)
SELECT *
FROM strong_students
ORDER BY gpa DESC
""")

print("\nStrong students:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 18. RANK
# ============================================================

# Concept:
# RANK gives position.
# If two rows tie, they get the same rank.
# The next rank skips a number.

# General structure:
# RANK() OVER (ORDER BY column_name DESC)

cursor.execute("""
SELECT name,
       gpa,
       RANK() OVER (ORDER BY gpa DESC) AS gpa_rank
FROM students
ORDER BY gpa_rank
""")

print("\nStudents ranked by GPA:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 19. UPDATE
# ============================================================

# Concept:
# UPDATE changes existing rows.
# Always use WHERE unless you want to update every row.

# General structure:
# UPDATE table_name
# SET column_name = new_value
# WHERE condition;

cursor.execute("""
UPDATE students
SET gpa = 3.2
WHERE name = 'Ben'
""")

conn.commit()


# ============================================================
# 20. DELETE
# ============================================================

# Concept:
# DELETE removes rows.
# Always use WHERE unless you want to delete every row.

# General structure:
# DELETE FROM table_name
# WHERE condition;

cursor.execute("""
DELETE FROM students
WHERE name = 'Temporary Student'
""")

conn.commit()


# ============================================================
# 21. PRACTICE QUESTION 1
# ============================================================

# Question:
# Show each major name and its average GPA.
# Only include students with GPA greater than 3.0.
# Show only majors where average GPA is greater than 3.4.
# Sort from highest average GPA to lowest.

# Answer:

cursor.execute("""
SELECT m.major_name,
       AVG(s.gpa) AS average_gpa
FROM students s
JOIN majors m
ON s.major_id = m.major_id
WHERE s.gpa > 3.0
GROUP BY m.major_name
HAVING AVG(s.gpa) > 3.4
ORDER BY average_gpa DESC
""")

print("\nPractice Question 1 Answer:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 22. PRACTICE QUESTION 2
# ============================================================

# Question:
# Show students with GPA greater than 3.0.
# Show student name, major name, GPA, and GPA rank.
# If the student has no major, show 'Undeclared'.
# First organize the joined result as a temporary named result.
# Then select from it and rank students by GPA.

# Answer:

cursor.execute("""
WITH student_major AS (
    SELECT s.name,
           COALESCE(m.major_name, 'Undeclared') AS major_name,
           s.gpa
    FROM students s
    LEFT JOIN majors m
    ON s.major_id = m.major_id
    WHERE s.gpa > 3.0
)
SELECT name,
       major_name,
       gpa,
       RANK() OVER (ORDER BY gpa DESC) AS gpa_rank
FROM student_major
ORDER BY gpa_rank
""")

print("\nPractice Question 2 Answer:")
for row in cursor.fetchall():
    print(row)


# ============================================================
# 23. SHORT SUMMARY
# ============================================================

# connection       -> links Python to database
# cursor           -> sends SQL commands to database
# execute          -> runs one SQL command
# executemany      -> runs one SQL command many times
# commit           -> saves changes
# fetchall         -> gets all result rows
# fetchone         -> gets one result row
# close            -> closes database connection

# SELECT           -> read data
# FROM             -> choose table
# WHERE            -> filter rows
# ORDER BY         -> sort rows
# LIMIT            -> restrict rows
# COUNT            -> count rows
# SUM              -> add numbers
# AVG              -> average
# MIN              -> lowest value
# MAX              -> highest value
# GROUP BY         -> summarize by group
# HAVING           -> filter grouped results
# JOIN             -> combine matching rows
# LEFT JOIN        -> keep all left rows
# COALESCE         -> replace NULL
# CTE              -> temporary named result
# RANK             -> ranking position
# UPDATE           -> change rows
# DELETE           -> remove rows


# ============================================================
# 24. CLOSE DATABASE
# ============================================================

# Concept:
# close ends the database connection.

conn.close()
