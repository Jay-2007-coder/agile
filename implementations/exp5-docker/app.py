"""
app.py - Online Book Store Flask REST API
Experiment 5: Docker Containerization

Endpoints:
  GET  /health       - Health check
  GET  /books        - Get all books
  GET  /books/<id>   - Get book by ID
  POST /books        - Add new book
  GET  /books/search?q=<query> - Search books
  POST /users/register - Register user
  POST /users/login    - Login user
"""

from flask import Flask, jsonify, request, abort
from typing import List, Optional, Dict
import uuid

app = Flask(__name__)

# ============================================================
# In-memory database (simulates a real database for demo)
# ============================================================
books_db: List[Dict] = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "genre": "Programming", "price": 450.0, "stock": 10},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "David Thomas", "genre": "Programming", "price": 550.0, "stock": 5},
    {"id": 3, "title": "Design Patterns", "author": "Gang of Four", "genre": "Programming", "price": 700.0, "stock": 3},
    {"id": 4, "title": "Introduction to Algorithms", "author": "CLRS", "genre": "Computer Science", "price": 1200.0, "stock": 8},
    {"id": 5, "title": "Effective Java", "author": "Joshua Bloch", "genre": "Java", "price": 600.0, "stock": 12},
]
users_db: Dict[str, str] = {}  # username -> password
next_book_id = 6


# ============================================================
# Health Check (Required for Docker HEALTHCHECK)
# ============================================================
@app.route('/health', methods=['GET'])
def health_check():
    """Docker health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Online Book Store API",
        "version": "1.0.0"
    }), 200


# ============================================================
# Books Endpoints
# ============================================================
@app.route('/books', methods=['GET'])
def get_all_books():
    """OBS-03: Get all books."""
    return jsonify({
        "books": books_db,
        "total": len(books_db)
    }), 200


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID."""
    book = next((b for b in books_db if b['id'] == book_id), None)
    if not book:
        abort(404, description=f"Book with ID {book_id} not found")
    return jsonify(book), 200


@app.route('/books/search', methods=['GET'])
def search_books():
    """OBS-04: Search books by title or author."""
    query = request.args.get('q', '').strip()
    author = request.args.get('author', '').strip()
    genre = request.args.get('genre', '').strip()

    results = books_db

    if query:
        results = [b for b in results if query.lower() in b['title'].lower()]
    if author:
        results = [b for b in results if author.lower() in b['author'].lower()]
    if genre:
        results = [b for b in results if b['genre'].lower() == genre.lower()]

    return jsonify({
        "query": query,
        "results": results,
        "total": len(results)
    }), 200


@app.route('/books', methods=['POST'])
def add_book():
    """OBS-05: Add a new book."""
    global next_book_id
    data = request.get_json()

    if not data:
        abort(400, description="Request body is required")

    required_fields = ['title', 'author', 'genre', 'price']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Field '{field}' is required")

    if not data['title'].strip():
        abort(400, description="Title cannot be empty")

    if data['price'] < 0:
        abort(400, description="Price cannot be negative")

    new_book = {
        "id": next_book_id,
        "title": data['title'],
        "author": data['author'],
        "genre": data['genre'],
        "price": float(data['price']),
        "stock": int(data.get('stock', 0))
    }
    books_db.append(new_book)
    next_book_id += 1

    return jsonify({
        "message": "Book added successfully",
        "book": new_book
    }), 201


# ============================================================
# Users Endpoints
# ============================================================
@app.route('/users/register', methods=['POST'])
def register():
    """OBS-01: Register a new user."""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        abort(400, description="username and password are required")

    username = data['username'].strip()
    password = data['password']

    if not username:
        abort(400, description="Username cannot be empty")

    if username in users_db:
        abort(409, description="Username already exists")

    users_db[username] = password
    return jsonify({
        "message": f"User '{username}' registered successfully"
    }), 201


@app.route('/users/login', methods=['POST'])
def login():
    """OBS-02: Login user and get session token."""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        abort(400, description="username and password are required")

    username = data['username']
    password = data['password']

    stored = users_db.get(username)
    if not stored or stored != password:
        abort(401, description="Invalid credentials")

    token = str(uuid.uuid4())
    return jsonify({
        "message": "Login successful",
        "token": token,
        "username": username
    }), 200


# ============================================================
# Error handlers
# ============================================================
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e.description)}), 400


@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"error": "Unauthorized", "message": str(e.description)}), 401


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": str(e.description)}), 404


@app.errorhandler(409)
def conflict(e):
    return jsonify({"error": "Conflict", "message": str(e.description)}), 409


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
