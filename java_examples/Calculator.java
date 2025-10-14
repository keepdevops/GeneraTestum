package com.example;

import java.util.ArrayList;
import java.util.List;

/**
 * A simple calculator class for demonstrating Java test generation.
 */
public class Calculator {
    private List<String> history;
    
    public Calculator() {
        this.history = new ArrayList<>();
    }
    
    /**
     * Adds two numbers and records the operation.
     */
    public double add(double a, double b) {
        double result = a + b;
        history.add(String.format("%.2f + %.2f = %.2f", a, b, result));
        return result;
    }
    
    /**
     * Subtracts two numbers and records the operation.
     */
    public double subtract(double a, double b) {
        double result = a - b;
        history.add(String.format("%.2f - %.2f = %.2f", a, b, result));
        return result;
    }
    
    /**
     * Multiplies two numbers and records the operation.
     */
    public double multiply(double a, double b) {
        double result = a * b;
        history.add(String.format("%.2f * %.2f = %.2f", a, b, result));
        return result;
    }
    
    /**
     * Divides two numbers and records the operation.
     * @throws IllegalArgumentException if dividing by zero
     */
    public double divide(double a, double b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        double result = a / b;
        history.add(String.format("%.2f / %.2f = %.2f", a, b, result));
        return result;
    }
    
    /**
     * Calculates the square root of a number.
     * @throws IllegalArgumentException for negative numbers
     */
    public double sqrt(double a) {
        if (a < 0) {
            throw new IllegalArgumentException("Cannot calculate square root of negative number");
        }
        double result = Math.sqrt(a);
        history.add(String.format("sqrt(%.2f) = %.2f", a, result));
        return result;
    }
    
    /**
     * Gets the calculation history.
     */
    public List<String> getHistory() {
        return new ArrayList<>(history);
    }
    
    /**
     * Clears the calculation history.
     */
    public void clearHistory() {
        history.clear();
    }
}
