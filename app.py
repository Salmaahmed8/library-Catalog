import json
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

#json file path
JSON_FILE = 'library.json'

#load books from json file
def load_books():
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return []

#save books to the JSON file
def save_books(books):
    with open(JSON_FILE, 'w') as file:
        json.dump(books, file, indent=4)

@app.route('/')
def index():
    books = load_books()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        books = load_books()
        new_book = {
            "id": len(books) + 1,
            "title": request.form.get('title'),
            "author": request.form.get('author'),
            "isbn": request.form.get('isbn'),
            "publication_year": request.form.get('publication_year'),
            "total_copies": int(request.form.get('total_copies', 1)),
            "available_copies": int(request.form.get('total_copies', 1))
        }
        books.append(new_book)
        save_books(books)
        return redirect(url_for('index'))

    return render_template('add_book.html')

@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '').lower()
    search_type = request.args.get('search_type', 'title').lower()

    books = load_books()
    results = []

    for book in books:
        if search_type == 'title' and query in book['title'].lower():
            results.append(book)
        elif search_type == 'author' and query in book['author'].lower():
            results.append(book)
        elif search_type == 'isbn' and query == book['isbn']:
            results.append(book)

    return render_template('search_results.html', books=results, query=query)

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    books = load_books()
    for book in books:
        if book['id'] == book_id and book['available_copies'] > 0:
            book['available_copies'] -= 1
            save_books(books)
            return redirect(url_for('index'))
    return "Book not available", 400

@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    books = load_books()
    for book in books:
        if book['id'] == book_id and book['available_copies'] < book['total_copies']:
            book['available_copies'] += 1
            save_books(books)
            return redirect(url_for('index'))
    return "Cannot return more books", 400

if __name__ == '__main__':
    app.run(debug=True)
