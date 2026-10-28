"""
Experiment 4: Software Testing
=================================
AIM: To understand and implement unit testing and integration
     testing using Python's unittest/pytest framework.

Tests for:
  - Unit Testing: Test individual components in isolation
  - Integration Testing: Test component interactions
  - Edge cases, boundary values, parameterized tests
"""

import unittest
from typing import List, Optional
from book_store_for_testing import Book, BookService, UserService, ShoppingCart


class TestBookUnit(unittest.TestCase):
    """UNIT TESTS for Book class - OBS-03"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.book = Book(1, "Clean Code", "Robert C. Martin", "Programming", 450.0, 10)

    def test_book_creation_valid(self):
        """Test creating a valid book."""
        self.assertEqual(self.book.book_id, 1)
        self.assertEqual(self.book.title, "Clean Code")
        self.assertEqual(self.book.author, "Robert C. Martin")
        self.assertEqual(self.book.price, 450.0)
        self.assertEqual(self.book.stock, 10)

    def test_book_str_representation(self):
        """Test string representation of book."""
        result = str(self.book)
        self.assertIn("Clean Code", result)
        self.assertIn("Robert C. Martin", result)

    def test_book_price_must_be_positive(self):
        """Test that negative price raises ValueError."""
        with self.assertRaises(ValueError):
            Book(2, "Bad Book", "Author", "Genre", -100.0, 5)

    def test_book_stock_cannot_be_negative(self):
        """Test that negative stock raises ValueError."""
        with self.assertRaises(ValueError):
            Book(3, "Stock Book", "Author", "Genre", 100.0, -1)

    def test_book_title_cannot_be_empty(self):
        """Test that empty title raises ValueError."""
        with self.assertRaises(ValueError):
            Book(4, "", "Author", "Genre", 100.0, 5)


class TestBookServiceUnit(unittest.TestCase):
    """UNIT TESTS for BookService - OBS-03, OBS-04, OBS-05"""

    def setUp(self):
        self.service = BookService()
        # Add test books
        self.book1 = Book(1, "Python Programming", "Guido", "Programming", 500.0, 10)
        self.book2 = Book(2, "Java Fundamentals", "James Gosling", "Programming", 600.0, 5)
        self.book3 = Book(3, "Machine Learning", "Andrew Ng", "ML", 800.0, 3)
        self.service.add_book(self.book1)
        self.service.add_book(self.book2)
        self.service.add_book(self.book3)

    def test_get_all_books_returns_all(self):
        """OBS-03: All books should be returned."""
        books = self.service.get_all_books()
        self.assertEqual(len(books), 3)

    def test_search_by_title_found(self):
        """OBS-04: Search by title should find matching books."""
        results = self.service.search_by_title("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Programming")

    def test_search_by_title_case_insensitive(self):
        """OBS-04: Search should be case-insensitive."""
        results = self.service.search_by_title("PYTHON")
        self.assertEqual(len(results), 1)

    def test_search_by_title_not_found(self):
        """OBS-04: Search for non-existent title returns empty list."""
        results = self.service.search_by_title("NonExistentXYZ")
        self.assertEqual(len(results), 0)

    def test_search_by_title_empty_string_returns_empty(self):
        """OBS-06 Bug Fix: Empty search returns empty, not all books."""
        results = self.service.search_by_title("")
        self.assertEqual(len(results), 0)

    def test_search_by_title_none_returns_empty(self):
        """OBS-06 Bug Fix: None search returns empty list."""
        results = self.service.search_by_title(None)
        self.assertEqual(len(results), 0)

    def test_add_book_valid(self):
        """OBS-05: Adding a valid book increases count."""
        initial_count = self.service.get_total_books()
        new_book = Book(4, "New Book", "Author", "Genre", 300.0, 1)
        result = self.service.add_book(new_book)
        self.assertTrue(result)
        self.assertEqual(self.service.get_total_books(), initial_count + 1)

    def test_add_book_none_fails(self):
        """OBS-05: Adding None book should fail."""
        result = self.service.add_book(None)
        self.assertFalse(result)

    def test_search_by_author(self):
        """OBS-04: Search by author name."""
        results = self.service.search_by_author("Guido")
        self.assertEqual(len(results), 1)

    def test_search_by_genre(self):
        """OBS-04: Search by genre returns correct books."""
        results = self.service.search_by_genre("ML")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Machine Learning")


class TestUserServiceUnit(unittest.TestCase):
    """UNIT TESTS for UserService - OBS-01, OBS-02"""

    def setUp(self):
        self.user_service = UserService()

    def test_register_new_user_succeeds(self):
        """OBS-01: New user registration should succeed."""
        result = self.user_service.register("alice", "pass123")
        self.assertTrue(result)

    def test_register_duplicate_user_fails(self):
        """OBS-01: Registering same username twice should fail."""
        self.user_service.register("alice", "pass123")
        result = self.user_service.register("alice", "different")
        self.assertFalse(result)

    def test_register_empty_username_fails(self):
        """OBS-01: Empty username should be rejected."""
        result = self.user_service.register("", "password")
        self.assertFalse(result)

    def test_register_none_password_fails(self):
        """OBS-01: None password should be rejected."""
        result = self.user_service.register("bob", None)
        self.assertFalse(result)

    def test_login_valid_credentials_returns_token(self):
        """OBS-02: Valid credentials should return a token."""
        self.user_service.register("alice", "pass123")
        token = self.user_service.login("alice", "pass123")
        self.assertIsNotNone(token)
        self.assertGreater(len(token), 0)

    def test_login_wrong_password_returns_none(self):
        """OBS-02: Wrong password returns None."""
        self.user_service.register("alice", "pass123")
        token = self.user_service.login("alice", "wrongpass")
        self.assertIsNone(token)

    def test_login_nonexistent_user_returns_none(self):
        """OBS-02: Non-existent user login returns None."""
        token = self.user_service.login("unknown", "pass")
        self.assertIsNone(token)

    def test_multiple_logins_give_different_tokens(self):
        """OBS-02: Each login should give a unique token."""
        self.user_service.register("alice", "pass")
        token1 = self.user_service.login("alice", "pass")
        token2 = self.user_service.login("alice", "pass")
        self.assertNotEqual(token1, token2)


class TestShoppingCartUnit(unittest.TestCase):
    """UNIT TESTS for ShoppingCart"""

    def setUp(self):
        self.cart = ShoppingCart()
        self.book1 = Book(1, "Book One", "Author A", "Genre", 100.0, 10)
        self.book2 = Book(2, "Book Two", "Author B", "Genre", 200.0, 5)

    def test_add_item_to_cart(self):
        """Adding item should increase cart size."""
        self.cart.add_item(self.book1, quantity=2)
        self.assertEqual(self.cart.get_item_count(), 1)  # 1 unique item

    def test_cart_total_calculation(self):
        """Total should be sum of (price * quantity)."""
        self.cart.add_item(self.book1, quantity=2)  # 100 * 2 = 200
        self.cart.add_item(self.book2, quantity=1)  # 200 * 1 = 200
        self.assertAlmostEqual(self.cart.get_total(), 400.0)

    def test_remove_item_from_cart(self):
        """Removing item should decrease cart."""
        self.cart.add_item(self.book1, quantity=1)
        result = self.cart.remove_item(self.book1.book_id)
        self.assertTrue(result)
        self.assertEqual(self.cart.get_item_count(), 0)

    def test_empty_cart_total_is_zero(self):
        """Empty cart should have zero total."""
        self.assertAlmostEqual(self.cart.get_total(), 0.0)

    def test_remove_nonexistent_item_fails(self):
        """Removing non-existent item returns False."""
        result = self.cart.remove_item(999)
        self.assertFalse(result)


# ================================================================
# INTEGRATION TESTS - Testing component interactions
# ================================================================
class TestBookStoreIntegration(unittest.TestCase):
    """
    INTEGRATION TESTS - Test full user flows across components.
    Integration tests verify that BookService + UserService + ShoppingCart
    work correctly together (not in isolation).
    """

    def setUp(self):
        self.user_service = UserService()
        self.book_service = BookService()
        self.cart = ShoppingCart()

        # Pre-populate books
        self.book_service.add_book(Book(1, "Python", "Guido", "Prog", 500.0, 10))
        self.book_service.add_book(Book(2, "Java", "Gosling", "Prog", 600.0, 5))

    def test_full_purchase_flow(self):
        """Integration: Register -> Login -> Search -> Add to Cart -> Checkout."""
        # Step 1: Register user
        self.assertTrue(self.user_service.register("jay", "password"))

        # Step 2: Login
        token = self.user_service.login("jay", "password")
        self.assertIsNotNone(token)

        # Step 3: Search for book
        results = self.book_service.search_by_title("python")
        self.assertFalse(len(results) == 0, "Should find Python book")

        # Step 4: Add to cart
        selected_book = results[0]
        self.cart.add_item(selected_book, quantity=1)

        # Step 5: Verify cart total
        self.assertAlmostEqual(self.cart.get_total(), 500.0)

    def test_user_must_be_registered_to_purchase(self):
        """Integration: Unregistered user cannot login."""
        token = self.user_service.login("unregistered", "password")
        self.assertIsNone(token, "Unregistered user cannot login")

    def test_add_book_then_search_finds_it(self):
        """Integration: Book added to service should be findable."""
        new_book = Book(10, "New Science Book", "Dr. Smith", "Science", 400.0, 3)
        added = self.book_service.add_book(new_book)
        self.assertTrue(added)

        found = self.book_service.search_by_title("Science")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].title, "New Science Book")


if __name__ == "__main__":
    # Run with verbose output
    unittest.main(verbosity=2)
