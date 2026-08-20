from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

#instead of a list, we connect to a database where we store books
def db_connection():
	conn = None
	try:
		conn = sqlite3.connect('books.sqlite')
	except sqlite3.error as e:
		print(e)
	return conn

@app.route("/books", methods=["GET", "POST"])
def books():
	#access the db connection
	conn = db_connection()
	#access the cursor object
	cursor = conn.cursor()

#creating our GET request for all books
	if request.method == "GET":
		cursor = conn.execute("SELECT * FROM books")
		books = [
		  dict(id=row[0], title=row[1], author=row[2], genre=row[3], year=row[4])
		  for row in cursor.fetchall()
		]

		if books is not None:
			return jsonify(books)
#creating our POST request for a book
	if request.method == "POST":
		title = request.form["title"]
		author = request.form["author"]
		genre = request.form["genre"]
		year = request.form["year"]
		#SQL query to INSERT a book INTO our database
		sql = """INSERT INTO books (title, author, genre, year)
				 VALUES (?, ?, ?, ?) """

		cursor = cursor.execute(sql, (title, author, genre, year))
		conn.commit()
		return f"Book with id: {cursor.lastrowid} created successfully"

#a route with all the necessary request methods for a single book
@app.route('/book/<int:id>', methods=["GET", "PUT", "DELETE"])
def book(id):
	conn = db_connection()
	cursor = conn.cursor()
	book = None

#creating our GET request for a book
	if request.method == "GET":
		cursor.execute("SELECT * FROM books WHERE id=?", (id,))
		rows = cursor.fetchall()
		for row in rows:
			book = row
		if book is not None:
			return jsonify(book), 200
		else:
			return "Something went wrong", 404

#creating our PUT request for a book
	if request.method == "PUT":
		sql = """ UPDATE books SET title = ?, author = ?, genre = ?, year = ?
				  WHERE id = ? """

		title = request.form["title"]
		author = request.form["author"]
		genre = request.form["genre"]
		year = request.form["year"]

		updated_book = {
			"id": id,
			"title": title,
			"author": author,
			"genre": genre,
			"year": year
		}

		conn.execute(sql, (title, author, genre, year, id))
		conn.commit()
		return jsonify(updated_book)

#creating our DELETE request for a book
	if request.method == "DELETE":
		sql = """ DELETE FROM books WHERE id=? """
		conn.execute(sql, (id,))
		conn.commit()

		return "The Book with id: {} has been deleted.".format(id), 200

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000, debug=False)
