"""
book_store_for_testing.py - Production code to be tested in Experiment 4.

This module is the implementation that test_book_store.py tests.
"""

import uuid
from typing import List, Optional, Dict, Tuple


class Book:
    """Represents a book in the online book store."""

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        genre: str,
        price: float,
        stock: int
    ):
        if not title or not title.strip():
            raise ValueError("Book title cannot be empty")
        if price < 0:
            raise ValueError("Book price cannot be negative")
        if stock < 0:
            raise ValueError("Book stock cannot be negative")

        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.stock = stock

    def __repr__(self) -> str:
        return (
            f"Book(id={self.book_id}, title='{self.title}', "
            f"author='{self.author}', price={self.price})"
        )

    def __str__(self) -> str:
        return f"[{self.book_id}] '{self.title}' by {self.author} - ₹{self.price}"


class BookService:
    """Manages book database operations."""

    def __init__(self):
        self._books: List[Book] = []

    def add_book(self, book: Optional[Book]) -> bool:
        """Add book to store."""
        if book is None:
            return False
        self._books.append(book)
        return True

    def get_all_books(self) -> List[Book]:
        """Return all books."""
        return list(self._books)

    def get_total_books(self) -> int:
        """Return count of books."""
        return len(self._books)

    def search_by_title(self, keyword: Optional[str]) -> List[Book]:
        """Search books by title keyword (case-insensitive)."""
        if not keyword or not keyword.strip():
            return []
        kw = keyword.lower()
        return [b for b in self._books if kw in b.title.lower()]

    def search_by_author(self, author: Optional[str]) -> List[Book]:
        """Search books by author name (case-insensitive)."""
        if not author or not author.strip():
            return []
        a = author.lower()
        return [b for b in self._books if a in b.author.lower()]

    def search_by_genre(self, genre: Optional[str]) -> List[Book]:
        """Search books by genre (case-insensitive exact match)."""
        if not genre or not genre.strip():
            return []
        return [b for b in self._books if b.genre.lower() == genre.lower()]

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Get book by its ID."""
        for b in self._books:
            if b.book_id == book_id:
                return b
        return None


class UserService:
    """Manages user authentication."""

    def __init__(self):
        self._users: Dict[str, str] = {}  # username -> password

    def register(self, username: Optional[str], password: Optional[str]) -> bool:
        """Register new user."""
        if not username or not username.strip():
            return False
        if not password:
            return False
        if username in self._users:
            return False
        self._users[username] = password
        return True

    def login(self, username: Optional[str], password: Optional[str]) -> Optional[str]:
        """Login user, return session token or None."""
        if not username or not password:
            return None
        stored = self._users.get(username)
        if stored and stored == password:
            return str(uuid.uuid4())
        return None

    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        return username in self._users


class ShoppingCart:
    """Manages a user's shopping cart."""

    def __init__(self):
        # book_id -> (Book, quantity)
        self._items: Dict[int, Tuple[Book, int]] = {}

    def add_item(self, book: Book, quantity: int = 1) -> None:
        """Add book to cart or increase quantity."""
        if book.book_id in self._items:
            existing_book, existing_qty = self._items[book.book_id]
            self._items[book.book_id] = (existing_book, existing_qty + quantity)
        else:
            self._items[book.book_id] = (book, quantity)

    def remove_item(self, book_id: int) -> bool:
        """Remove item from cart."""
        if book_id not in self._items:
            return False
        del self._items[book_id]
        return True

    def get_item_count(self) -> int:
        """Get number of unique items in cart."""
        return len(self._items)

    def get_total(self) -> float:
        """Calculate total cost of cart."""
        total = 0.0
        for book, qty in self._items.values():
            total += book.price * qty
        return total

    def clear(self) -> None:
        """Clear all items from cart."""
        self._items.clear()
