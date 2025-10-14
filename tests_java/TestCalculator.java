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

}