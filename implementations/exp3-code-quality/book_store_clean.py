"""
book_store_clean.py - Online Book Store AFTER code quality fixes.

Experiment 3: Code Quality Analysis - CLEAN VERSION
This file shows the code AFTER fixing all Pylint/Flake8 issues.

Run Pylint: pylint book_store_clean.py
Run Flake8: flake8 book_store_clean.py
"""

import sys
from typing import List, Optional

# Constants instead of magic numbers
CHEAP_THRESHOLD = 200
MEDIUM_THRESHOLD = 500
PREMIUM_DISCOUNT_BONUS = 5
COUPON_DISCOUNT_RATE = 0.9


class Book:
    """Represents a book in the online book store."""

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        price: float,
        stock: int
    ):
        """Initialize a Book instance.

        Args:
            book_id: Unique identifier for the book.
            title: Title of the book.
            author: Author's name.
            price: Price in rupees.
            stock: Available stock quantity.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    def get_info(self) -> str:
        """Return formatted book information.

        Returns:
            A string with book ID and title.
        """
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}"

    def __repr__(self) -> str:
        """Return string representation of Book."""
        return (
            f"Book(id={self.book_id}, title='{self.title}', "
            f"author='{self.author}', price={self.price})"
        )


class BookStore:
    """Online Book Store management system.

    Manages a collection of books and user accounts.
    """

    def __init__(self):
        """Initialize empty book store."""
        self.books: List[Book] = []
        self.users: dict = {}

    def add_book(self, book: Book) -> bool:
        """Add a book to the store.

        Args:
            book: Book instance to add.

        Returns:
            True if book was added, False otherwise.
        """
        if book is None:
            return False
        self.books.append(book)
        return True

    def search(self, keyword: str) -> List[Book]:
        """Search books by keyword in title.

        Args:
            keyword: Search term.

        Returns:
            List of matching books.
        """
        if not keyword or not keyword.strip():
            return []

        keyword_lower = keyword.lower()
        return [
            book for book in self.books
            if keyword_lower in book.title.lower()
        ]

    def get_total_value(self) -> float:
        """Calculate total value of all books in store.

        Returns:
            Sum of prices of all books.
        """
        return sum(book.price for book in self.books)

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Find a book by its ID.

        Args:
            book_id: Book identifier.

        Returns:
            Book instance or None if not found.
        """
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None


def calculate_discount(
    price: float,
    discount_percent: float,
    tax_rate: float,
    minimum_order_value: float,
    is_premium_member: bool,
    has_coupon: bool
) -> float:
    """Calculate final price with discount and tax.

    Args:
        price: Original price.
        discount_percent: Base discount percentage.
        tax_rate: Tax rate percentage.
        minimum_order_value: Minimum order for discount eligibility.
        is_premium_member: Whether user is premium member.
        has_coupon: Whether user has a coupon code.

    Returns:
        Final calculated price.
    """
    if price < minimum_order_value:
        return price * (1 + tax_rate / 100)

    effective_discount = discount_percent
    if is_premium_member:
        effective_discount += PREMIUM_DISCOUNT_BONUS

    discount_amount = price * (effective_discount / 100)
    discounted_price = price - discount_amount

    if has_coupon:
        discounted_price *= COUPON_DISCOUNT_RATE

    return discounted_price * (1 + tax_rate / 100)


def get_price_category(price: float) -> str:
    """Categorize book price.

    Args:
        price: Book price in rupees.

    Returns:
        Category: 'cheap', 'medium', or 'expensive'.
    """
    if price < CHEAP_THRESHOLD:
        return "cheap"
    if price < MEDIUM_THRESHOLD:
        return "medium"
    return "expensive"


def verify_admin_access(provided_password: str, stored_hash: str) -> bool:
    """Verify admin access using hash comparison (not hardcoded password).

    Args:
        provided_password: Password to verify.
        stored_hash: Stored hash to compare against.

    Returns:
        True if password matches hash.
    """
    import hashlib
    provided_hash = hashlib.sha256(provided_password.encode()).hexdigest()
    return provided_hash == stored_hash


if __name__ == "__main__":
    # Demo usage
    store = BookStore()
    store.add_book(Book(1, "Clean Code", "Robert C. Martin", 450.0, 10))
    store.add_book(Book(2, "Effective Java", "Joshua Bloch", 600.0, 5))

    print("=== Clean Code Demo ===")
    for book in store.books:
        print(book.get_info())

    print("\nSearch results for 'code':")
    results = store.search("code")
    for book in results:
        print(f"  - {book.title}")

    print(f"\nTotal store value: ₹{store.get_total_value():.2f}")
    print(f"'Clean Code' category: {get_price_category(450.0)}")

    final_price = calculate_discount(
        price=600.0,
        discount_percent=10,
        tax_rate=18,
        minimum_order_value=200,
        is_premium_member=True,
        has_coupon=False
    )
    print(f"Final price with 10% discount (premium): ₹{final_price:.2f}")
