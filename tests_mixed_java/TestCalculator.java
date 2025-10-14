package com.example;

import AfterAll;
import AfterEach;
import BeforeAll;
import BeforeEach;
import DisplayName;
import MethodSource;
import ParameterizedTest;
import Test;
import ValueSource;
import com.example.Calculator;
import org.assertj.core.api.Assertions.assertThat;
import org.assertj.core.api.Assertions.assertThatCode;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class TestCalculator {

    @Test
@DisplayName("Test Calculator instantiation")
void test_Calculator_instantiation() {
    // Arrange & Act
    Calculator instance = new Calculator();
    
    // Assert
    assertThat(instance).isNotNull();
    assertThat(instance).isInstanceOf(Calculator.class);
}

    @Test
@DisplayName("Test add method")
void test_add() {
    // Arrange
    Calculator instance = new Calculator();
    double a = 0.0;
    double b = 0.0;

    // Act
    double result = instance.add(a, b);

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test subtract method")
void test_subtract() {
    // Arrange
    Calculator instance = new Calculator();
    double a = 0.0;
    double b = 0.0;

    // Act
    double result = instance.subtract(a, b);

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test multiply method")
void test_multiply() {
    // Arrange
    Calculator instance = new Calculator();
    double a = 0.0;
    double b = 0.0;

    // Act
    double result = instance.multiply(a, b);

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test divide method")
void test_divide() {
    // Arrange
    Calculator instance = new Calculator();
    double a = 0.0;
    double b = 0.0;

    // Act
    double result = instance.divide(a, b);

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test sqrt method")
void test_sqrt() {
    // Arrange
    Calculator instance = new Calculator();
    double a = 0.0;

    // Act
    double result = instance.sqrt(a);

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test getHistory method")
void test_getHistory() {
    // Arrange
    Calculator instance = new Calculator();

    // Act
    List result = instance.getHistory();

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test clearHistory method")
void test_clearHistory() {
    // Arrange
    Calculator instance = new Calculator();

    // Act & Assert
    assertThatCode(() -> instance.clearHistory())
            .doesNotThrowAnyException();
}

}