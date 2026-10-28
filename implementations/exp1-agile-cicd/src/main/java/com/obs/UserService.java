package com.obs;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * UserService - Handles user authentication.
 * Implements user stories:
 * OBS-01: User Registration
 * OBS-02: User Login
 */
public class UserService {

    private final Map<String, String> userDatabase; // username -> password

    public UserService() {
        this.userDatabase = new HashMap<>();
    }

    /**
     * OBS-01: Register a new user
     * @return true if registration successful, false if username already exists
     */
    public boolean register(String username, String password) {
        if (username == null || username.trim().isEmpty() ||
            password == null || password.trim().isEmpty()) {
            return false;
        }
        if (userDatabase.containsKey(username)) {
            return false; // Username already taken
        }
        userDatabase.put(username, password);
        return true;
    }

    /**
     * OBS-02: Login existing user
     * @return token if login successful, null if invalid credentials
     */
    public String login(String username, String password) {
        if (username == null || password == null) {
            return null;
        }
        String storedPassword = userDatabase.get(username);
        if (storedPassword != null && storedPassword.equals(password)) {
            // Generate simple session token
            return UUID.randomUUID().toString();
        }
        return null;
    }

    /**
     * Check if a user exists
     */
    public boolean userExists(String username) {
        return userDatabase.containsKey(username);
    }

    /**
     * Get total number of registered users
     */
    public int getTotalUsers() {
        return userDatabase.size();
    }
}
