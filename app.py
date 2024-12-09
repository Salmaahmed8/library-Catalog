from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    publication_year = db.Column(db.Integer)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # add book to database
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            isbn=request.form['isbn'],
            publication_year=int(request.form['publication_year']),
            total_copies=int(request.form['total_copies']),
            available_copies=int(request.form['total_copies'])
        )
        
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return f"Error adding book: {str(e)}", 400

    return render_template('add_book.html')

@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    search_type = request.args.get('search_type', 'title')

    if search_type == 'title':
        books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    elif search_type == 'author':
        books = Book.query.filter(Book.author.ilike(f'%{query}%')).all()
    elif search_type == 'isbn':
        books = Book.query.filter(Book.isbn == query).all()
    else:
        books = []

    return render_template('search_results.html', books=books, query=query)

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_copies > 0:
        book.available_copies -= 1
        db.session.commit()
        return redirect(url_for('index'))
    return "Book not available", 400

@app.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_copies < book.total_copies:
        book.available_copies += 1
        db.session.commit()
        return redirect(url_for('index'))
    return "Cannot return more books", 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)