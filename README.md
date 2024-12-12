# Library Catalog Application

## Project Overview
This is a simple library catalog application built using Flask and SQLAlchemy. The application allows users to manage books in a library by adding, searching, borrowing, and returning books. The data is stored in an SQLite database.

## Features
1. **Home Page**
   - Displays a list of all books in the library.

2. **Add Book**
   - Add new books to the library with details like title, author, ISBN, publication year, and number of copies.

3. **Search Books**
   - Search books by title, author, or ISBN.

4. **Borrow Book**
   - Borrow a book by decreasing its available copies.

5. **Return Book**
   - Return a borrowed book by increasing its available copies.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd inventory_tracking
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Usage
1. Run the Flask application:
   ```bash
   python app.py
   ```
