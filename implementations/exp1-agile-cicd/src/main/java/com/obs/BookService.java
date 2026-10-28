package com.obs;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * BookService - Core business logic for Online Book Store.
 * Implements user stories:
 * OBS-03: View Books
 * OBS-04: Search Books
 * OBS-05: Add Book to DB
 */
public class BookService {

    private final List<Book> bookDatabase;

    public BookService() {
        this.bookDatabase = new ArrayList<>();
        initializeSampleData();
    }

    private void initializeSampleData() {
        bookDatabase.add(new Book(1, "Clean Code", "Robert C. Martin", "Programming", 450.00, 10));
        bookDatabase.add(new Book(2, "The Pragmatic Programmer", "David Thomas", "Programming", 550.00, 5));
        bookDatabase.add(new Book(3, "Design Patterns", "Gang of Four", "Programming", 700.00, 3));
        bookDatabase.add(new Book(4, "Introduction to Algorithms", "CLRS", "Computer Science", 1200.00, 8));
        bookDatabase.add(new Book(5, "Effective Java", "Joshua Bloch", "Java", 600.00, 12));
    }

    /**
     * OBS-03: View all available books
     */
    public List<Book> getAllBooks() {
        return new ArrayList<>(bookDatabase);
    }

    /**
     * OBS-04: Search books by title
     */
    public List<Book> searchByTitle(String keyword) {
        if (keyword == null || keyword.trim().isEmpty()) {
            return new ArrayList<>();
        }
        return bookDatabase.stream()
                .filter(b -> b.getTitle().toLowerCase().contains(keyword.toLowerCase()))
                .collect(Collectors.toList());
    }

    /**
     * OBS-04: Search books by author
     */
    public List<Book> searchByAuthor(String author) {
        if (author == null || author.trim().isEmpty()) {
            return new ArrayList<>();
        }
        return bookDatabase.stream()
                .filter(b -> b.getAuthor().toLowerCase().contains(author.toLowerCase()))
                .collect(Collectors.toList());
    }

    /**
     * OBS-04: Search books by genre
     */
    public List<Book> searchByGenre(String genre) {
        if (genre == null || genre.trim().isEmpty()) {
            return new ArrayList<>();
        }
        return bookDatabase.stream()
                .filter(b -> b.getGenre().equalsIgnoreCase(genre))
                .collect(Collectors.toList());
    }

    /**
     * OBS-05: Add book to database
     */
    public boolean addBook(Book book) {
        if (book == null || book.getTitle() == null || book.getTitle().isEmpty()) {
            return false;
        }
        bookDatabase.add(book);
        return true;
    }

    /**
     * OBS-05: Get book by ID
     */
    public Optional<Book> getBookById(int id) {
        return bookDatabase.stream()
                .filter(b -> b.getId() == id)
                .findFirst();
    }

    /**
     * Get total number of books
     */
    public int getTotalBooks() {
        return bookDatabase.size();
    }
}
