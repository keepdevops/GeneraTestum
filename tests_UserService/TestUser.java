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
import com.example.User;
import com.example.service.User;
import org.assertj.core.api.Assertions.assertThat;
import org.assertj.core.api.Assertions.assertThatCode;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class TestUser {

    @Test
@DisplayName("Test User instantiation")
void test_User_instantiation() {
    // Arrange & Act
    User instance = new User();
    
    // Assert
    assertThat(instance).isNotNull();
    assertThat(instance).isInstanceOf(User.class);
}

    @Test
@DisplayName("Test getId method")
void test_getId() {
    // Arrange
    User instance = new User();

    // Act
    Long result = instance.getId();

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test getUsername method")
void test_getUsername() {
    // Arrange
    User instance = new User();

    // Act
    String result = instance.getUsername();

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test setUsername method")
void test_setUsername() {
    // Arrange
    User instance = new User();
    String username = "test";

    // Act & Assert
    assertThatCode(() -> instance.setUsername(username))
            .doesNotThrowAnyException();
}

    @Test
@DisplayName("Test getEmail method")
void test_getEmail() {
    // Arrange
    User instance = new User();

    // Act
    String result = instance.getEmail();

    // Assert
    assertThat(result).isNotNull();
}

    @Test
@DisplayName("Test setEmail method")
void test_setEmail() {
    // Arrange
    User instance = new User();
    String email = "test";

    // Act & Assert
    assertThatCode(() -> instance.setEmail(email))
            .doesNotThrowAnyException();
}

    @Test
@DisplayName("Test getCreatedAt method")
void test_getCreatedAt() {
    // Arrange
    User instance = new User();

    // Act
    Date result = instance.getCreatedAt();

    // Assert
    assertThat(result).isNotNull();
}

}