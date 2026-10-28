package com.obs;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Test suite for Online Book Store - Sprint 1
 * Covers all user stories: OBS-01 through OBS-06
 */
@DisplayName("Online Book Store - Sprint 1 Tests")
public class BookStoreTest {

    private UserService userService;
    private BookService bookService;

    @BeforeEach
    void setUp() {
        userService = new UserService();
        bookService = new BookService();
    }

    // ================================================================
    // OBS-01: User Registration Tests
    // ================================================================
    @Nested
    @DisplayName("OBS-01: User Registration")
    class UserRegistrationTest {

        @Test
        @DisplayName("Should successfully register a new user")
        void testRegisterNewUser() {
            boolean result = userService.register("testUser", "password123");
            assertTrue(result, "Registration should succeed for a new user");
            assertTrue(userService.userExists("testUser"));
        }

        @Test
        @DisplayName("Should fail registration for duplicate username")
        void testRegisterDuplicateUser() {
            userService.register("testUser", "pass1");
            boolean result = userService.register("testUser", "pass2");
            assertFalse(result, "Registration should fail for duplicate username");
        }

        @Test
        @DisplayName("Should fail registration with empty username")
        void testRegisterEmptyUsername() {
            boolean result = userService.register("", "password123");
            assertFalse(result, "Registration should fail for empty username");
        }

        @Test
        @DisplayName("Should fail registration with null password")
        void testRegisterNullPassword() {
            boolean result = userService.register("testUser", null);
            assertFalse(result, "Registration should fail for null password");
        }
    }

    // ================================================================
    // OBS-02: User Login Tests
    // ================================================================
    @Nested
    @DisplayName("OBS-02: User Login")
    class UserLoginTest {

        @BeforeEach
        void registerTestUser() {
            userService.register("testUser", "password123");
        }

        @Test
        @DisplayName("Should return token on successful login")
        void testSuccessfulLogin() {
            String token = userService.login("testUser", "password123");
            assertNotNull(token, "Token should not be null on successful login");
            assertFalse(token.isEmpty(), "Token should not be empty");
        }

        @Test
        @DisplayName("Should return null for wrong password")
        void testWrongPasswordLogin() {
            String token = userService.login("testUser", "wrongPassword");
            assertNull(token, "Token should be null for wrong password");
        }

        @Test
        @DisplayName("Should return null for non-existent user")
        void testNonExistentUserLogin() {
            String token = userService.login("unknownUser", "password");
            assertNull(token, "Token should be null for non-existent user");
        }
    }

    // ================================================================
    // OBS-03: View Books Tests
    // ================================================================
    @Nested
    @DisplayName("OBS-03: View All Books")
    class ViewBooksTest {

        @Test
        @DisplayName("Should return all books from database")
        void testGetAllBooks() {
            List<Book> books = bookService.getAllBooks();
            assertNotNull(books);
            assertFalse(books.isEmpty(), "Book list should not be empty");
            assertEquals(5, books.size(), "Should have 5 initial books");
        }

        @Test
        @DisplayName("Book should have all required fields")
        void testBookFields() {
            Book book = bookService.getAllBooks().get(0);
            assertNotNull(book.getTitle());
            assertNotNull(book.getAuthor());
            assertNotNull(book.getGenre());
            assertTrue(book.getPrice() > 0);
            assertTrue(book.getStock() >= 0);
        }
    }

    // ================================================================
    // OBS-04: Search Books Tests
    // ================================================================
    @Nested
    @DisplayName("OBS-04: Search Books")
    class SearchBooksTest {

        @Test
        @DisplayName("Should find book by title keyword")
        void testSearchByTitle() {
            List<Book> results = bookService.searchByTitle("java");
            assertFalse(results.isEmpty(), "Should find books with 'java' in title");
            assertTrue(results.stream().anyMatch(b -> b.getTitle().toLowerCase().contains("java")));
        }

        @Test
        @DisplayName("Should find book by author")
        void testSearchByAuthor() {
            List<Book> results = bookService.searchByAuthor("Martin");
            assertFalse(results.isEmpty(), "Should find books by Martin");
        }

        @Test
        @DisplayName("Should find books by genre")
        void testSearchByGenre() {
            List<Book> results = bookService.searchByGenre("Programming");
            assertFalse(results.isEmpty(), "Should find programming books");
        }

        @Test
        @DisplayName("Should return empty list for non-existent title")
        void testSearchByNonExistentTitle() {
            List<Book> results = bookService.searchByTitle("XYZ_NonExistent_Book");
            assertTrue(results.isEmpty(), "Should return empty list for non-existent book");
        }
    }

    // ================================================================
    // OBS-05: Add Book Tests
    // ================================================================
    @Nested
    @DisplayName("OBS-05: Add Book to Database")
    class AddBookTest {

        @Test
        @DisplayName("Should successfully add a new book")
        void testAddNewBook() {
            int initialCount = bookService.getTotalBooks();
            Book newBook = new Book(10, "New Book", "Author", "Genre", 300.0, 5);
            boolean result = bookService.addBook(newBook);
            assertTrue(result, "Book should be added successfully");
            assertEquals(initialCount + 1, bookService.getTotalBooks());
        }

        @Test
        @DisplayName("Should fail to add null book")
        void testAddNullBook() {
            boolean result = bookService.addBook(null);
            assertFalse(result, "Should fail to add null book");
        }

        @Test
        @DisplayName("Should retrieve added book by ID")
        void testRetrieveAddedBook() {
            Book newBook = new Book(100, "Test Book", "Test Author", "Test", 100.0, 1);
            bookService.addBook(newBook);
            assertTrue(bookService.getBookById(100).isPresent(), "Should find book by ID");
            assertEquals("Test Book", bookService.getBookById(100).get().getTitle());
        }
    }

    // ================================================================
    // OBS-06: Bug Fix - Empty Search Tests
    // ================================================================
    @Nested
    @DisplayName("OBS-06: Bug Fix - Empty Search Handling")
    class EmptySearchBugFixTest {

        @Test
        @DisplayName("Empty string search should return empty list, not all books")
        void testEmptyStringSearch() {
            List<Book> results = bookService.searchByTitle("");
            assertTrue(results.isEmpty(), "Empty search should return empty list (bug fix)");
        }

        @Test
        @DisplayName("Null search should return empty list without exception")
        void testNullSearch() {
            assertDoesNotThrow(() -> {
                List<Book> results = bookService.searchByTitle(null);
                assertTrue(results.isEmpty(), "Null search should return empty list");
            });
        }

        @Test
        @DisplayName("Whitespace search should return empty list")
        void testWhitespaceSearch() {
            List<Book> results = bookService.searchByTitle("   ");
            assertTrue(results.isEmpty(), "Whitespace search should return empty list");
        }
    }
}
