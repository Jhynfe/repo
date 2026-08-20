import sqlite3
#create db connection
conn = sqlite3.connect("books.sqlite")
#create the db cursor object
cursor = conn.cursor()
#create sql table creation query
sql_query = """ CREATE TABLE books (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	author TEXT NOT NULL,
	genre TEXT NOT NULL,
	year TEXT
)"""

cursor.execute(sql_query)
