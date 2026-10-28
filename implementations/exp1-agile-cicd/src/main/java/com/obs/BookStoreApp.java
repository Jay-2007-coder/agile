package com.obs;

import java.util.List;

/**
 * BookStoreApp - Main application entry point for Online Book Store.
 * Demonstrates all user stories from Sprint 1.
 *
 * User Stories covered:
 *   OBS-01: User Registration
 *   OBS-02: User Login
 *   OBS-03: View Books
 *   OBS-04: Search Books
 *   OBS-05: Add Book to Database
 *   OBS-06: Bug Fix - Empty Search Handling
 */
public class BookStoreApp {

    public static void main(String[] args) {
        System.out.println("======================================");
        System.out.println("   Online Book Store - Sprint Demo   ");
        System.out.println("======================================");

        // Initialize services
        UserService userService = new UserService();
        BookService bookService = new BookService();

        // --- OBS-01: User Registration ---
        System.out.println("\n[OBS-01] User Registration:");
        boolean reg1 = userService.register("jay_student", "password123");
        boolean reg2 = userService.register("john_doe", "secure456");
        boolean reg3 = userService.register("jay_student", "duplicate"); // Should fail
        System.out.println("  Registered 'jay_student': " + reg1);
        System.out.println("  Registered 'john_doe': " + reg2);
        System.out.println("  Re-registered 'jay_student' (should fail): " + reg3);
        System.out.println("  Total users: " + userService.getTotalUsers());

        // --- OBS-02: User Login ---
        System.out.println("\n[OBS-02] User Login:");
        String token = userService.login("jay_student", "password123");
        String badToken = userService.login("jay_student", "wrongpass");
        System.out.println("  Login with correct password: " + (token != null ? "SUCCESS (token=" + token.substring(0, 8) + "...)" : "FAILED"));
        System.out.println("  Login with wrong password: " + (badToken != null ? "SUCCESS" : "FAILED (expected)"));

        // --- OBS-03: View Books ---
        System.out.println("\n[OBS-03] View All Books:");
        List<Book> books = bookService.getAllBooks();
        books.forEach(b -> System.out.println("  " + b));
        System.out.println("  Total books: " + bookService.getTotalBooks());

        // --- OBS-04: Search Books ---
        System.out.println("\n[OBS-04] Search Books:");
        System.out.println("  Search by title 'java':");
        bookService.searchByTitle("java").forEach(b -> System.out.println("    " + b.getTitle()));

        System.out.println("  Search by author 'Martin':");
        bookService.searchByAuthor("Martin").forEach(b -> System.out.println("    " + b.getTitle()));

        System.out.println("  Search by genre 'Programming':");
        bookService.searchByGenre("Programming").forEach(b -> System.out.println("    " + b.getTitle()));

        // --- OBS-05: Add Book ---
        System.out.println("\n[OBS-05] Add Book to Database:");
        Book newBook = new Book(6, "Spring Boot in Action", "Craig Walls", "Java", 800.00, 7);
        boolean added = bookService.addBook(newBook);
        System.out.println("  Added 'Spring Boot in Action': " + added);
        System.out.println("  Total books now: " + bookService.getTotalBooks());

        // --- OBS-06: Bug Fix - Empty Search ---
        System.out.println("\n[OBS-06] Bug Fix - Empty Search Handling:");
        List<Book> emptySearch = bookService.searchByTitle("");
        List<Book> nullSearch = bookService.searchByTitle(null);
        System.out.println("  Empty string search returns empty list: " + emptySearch.isEmpty());
        System.out.println("  Null search returns empty list: " + nullSearch.isEmpty());

        System.out.println("\n======================================");
        System.out.println("   Sprint 1 Demo Complete!           ");
        System.out.println("======================================");
    }
}
