package com.example.service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Service class for user management operations.
 */
public class UserService {
    private Map<Long, User> users;
    private Long nextId;
    
    public UserService() {
        this.users = new HashMap<>();
        this.nextId = 1L;
    }
    
    /**
     * Creates a new user.
     */
    public User createUser(String username, String email) {
        if (username == null || username.trim().isEmpty()) {
            throw new IllegalArgumentException("Username cannot be null or empty");
        }
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email format");
        }
        
        User user = new User(nextId++, username, email);
        users.put(user.getId(), user);
        return user;
    }
    
    /**
     * Retrieves a user by ID.
     */
    public User getUserById(Long id) {
        return users.get(id);
    }
    
    /**
     * Retrieves all users.
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(users.values());
    }
    
    /**
     * Updates a user's information.
     */
    public User updateUser(Long id, String username, String email) {
        User user = users.get(id);
        if (user == null) {
            throw new IllegalArgumentException("User not found");
        }
        
        if (username != null && !username.trim().isEmpty()) {
            user.setUsername(username);
        }
        if (email != null && email.contains("@")) {
            user.setEmail(email);
        }
        
        return user;
    }
    
    /**
     * Deletes a user.
     */
    public boolean deleteUser(Long id) {
        return users.remove(id) != null;
    }
    
    /**
     * Finds users by username pattern.
     */
    public List<User> findUsersByUsername(String pattern) {
        return users.values().stream()
                .filter(user -> user.getUsername().toLowerCase().contains(pattern.toLowerCase()))
                .collect(Collectors.toList());
    }
}

/**
 * Simple User model class.
 */
class User {
    private Long id;
    private String username;
    private String email;
    private Date createdAt;
    
    public User(Long id, String username, String email) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.createdAt = new Date();
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public Date getCreatedAt() { return createdAt; }
}
