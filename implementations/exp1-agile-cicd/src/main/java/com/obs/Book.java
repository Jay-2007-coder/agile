package com.obs;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Book entity representing a book in the Online Book Store.
 * OBS-01: User Registration & OBS-03: View Books features
 */
public class Book {
    private int id;
    private String title;
    private String author;
    private String genre;
    private double price;
    private int stock;

    public Book(int id, String title, String author, String genre, double price, int stock) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.genre = genre;
        this.price = price;
        this.stock = stock;
    }

    public int getId() { return id; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public String getGenre() { return genre; }
    public double getPrice() { return price; }
    public int getStock() { return stock; }

    public void setStock(int stock) { this.stock = stock; }

    @Override
    public String toString() {
        return String.format("Book{id=%d, title='%s', author='%s', genre='%s', price=%.2f, stock=%d}",
                id, title, author, genre, price, stock);
    }
}
