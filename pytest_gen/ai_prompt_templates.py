"""
AI prompt template definitions.
"""


class PromptTemplates:
    """Template definitions for AI prompts."""
    
    @staticmethod
    def system_prompt() -> str:
        """System prompt defining the AI assistant's role."""
        return """You are an expert testing assistant specializing in pytest and test automation. Your role is to help developers write better tests by providing intelligent guidance, recommendations, and explanations.

Key capabilities:
- Analyze code and suggest comprehensive test strategies
- Recommend appropriate mocking approaches
- Identify test coverage gaps
- Explain testing best practices
- Help with pytest configuration and setup
- Debug test generation issues
- Provide educational content about testing concepts

Guidelines:
- Always be helpful, accurate, and practical
- Provide specific, actionable recommendations
- Include code examples when relevant
- Explain the reasoning behind suggestions
- Consider different testing scenarios (unit, integration, e2e)
- Stay focused on testing and pytest topics
- If unsure about something, say so and suggest how to find out
- Be concise but thorough in explanations"""
    
    @staticmethod
    def test_strategy_prompt() -> str:
        """Template for test strategy recommendations."""
        return """Analyze the following code and recommend a comprehensive test strategy:

Code Type: {code_type}
Framework: {framework}
Code:
```python
{code}
```

Please provide:
1. **Test Categories**: What types of tests should be written (unit, integration, etc.)
2. **Key Test Cases**: Specific scenarios to test
3. **Mocking Strategy**: What should be mocked and why
4. **Edge Cases**: Boundary conditions and error scenarios
5. **Fixtures**: Recommended pytest fixtures
6. **Parametrization**: Opportunities for parametrized tests

Focus on practical, actionable recommendations that will improve test coverage and reliability."""
    
    @staticmethod
    def coverage_analysis_prompt() -> str:
        """Template for coverage analysis."""
        return """Analyze the test coverage for the following code:

Source Code:
```python
{source_code}
```

Existing Tests:
```python
{existing_tests}
```

Please identify:
1. **Missing Test Cases**: What's not being tested
2. **Coverage Gaps**: Areas with insufficient coverage
3. **Test Quality**: Issues with existing tests
4. **Improvement Suggestions**: How to enhance the tests
5. **Edge Cases**: Missing boundary conditions
6. **Error Scenarios**: Unhandled error cases

Provide specific, actionable recommendations for improving test coverage."""
    
    @staticmethod
    def mock_recommendation_prompt() -> str:
        """Template for mocking recommendations."""
        return """Analyze the dependencies in this code and recommend a mocking strategy:

Code:
```python
{code}
```

Dependencies: {dependencies}

Please recommend:
1. **What to Mock**: Which dependencies should be mocked
2. **Mocking Level**: How extensively to mock (shallow vs deep)
3. **Mock Types**: Pytest fixtures, unittest.mock, or external libraries
4. **Mock Configuration**: How to set up the mocks
5. **Test Isolation**: Ensuring tests don't interfere with each other
6. **Integration Points**: Where to test real integrations vs mocks

Focus on practical mocking that improves test reliability and speed."""
    
    @staticmethod
    def configuration_help_prompt() -> str:
        """Template for configuration assistance."""
        return """Help configure the test generator for this codebase:

Requirements: {requirements}
Code Type: {code_type}
Framework: {framework}

Please recommend:
1. **Mock Level**: Appropriate mocking strategy
2. **Coverage Type**: Test coverage approach
3. **Configuration Settings**: Optimal generator settings
4. **File Organization**: How to structure test files
5. **Dependencies**: What external dependencies to handle
6. **Performance**: Settings for test generation speed vs quality

Provide specific configuration values and explain the reasoning behind each recommendation."""
    
    @staticmethod
    def error_resolution_prompt() -> str:
        """Template for error resolution."""
        return """Help resolve this test generation error:

Error: {error_message}
Code: {code}
Configuration: {config}

Please provide:
1. **Error Analysis**: What's causing the error
2. **Solution Steps**: How to fix the issue
3. **Prevention**: How to avoid this error in the future
4. **Alternative Approaches**: Other ways to achieve the goal
5. **Debugging Tips**: How to troubleshoot similar issues

Be specific and actionable in your recommendations."""
    
    @staticmethod
    def code_explanation_prompt() -> str:
        """Template for code explanation."""
        return """Explain what tests will be generated for this code:

Code:
```python
{code}
```

Configuration: {config}

Please explain:
1. **Generated Tests**: What test files and functions will be created
2. **Test Structure**: How the tests will be organized
3. **Mocking**: What will be mocked and how
4. **Fixtures**: What fixtures will be generated
5. **Parametrization**: What parametrized tests will be created
6. **Coverage**: What scenarios will be tested

Provide a clear, detailed explanation that helps the user understand the test generation process."""
    
    @staticmethod
    def best_practices_prompt() -> str:
        """Template for best practices guidance."""
        return """Provide testing best practices for:

Topic: {topic}
Context: {context}

Please cover:
1. **Core Principles**: Fundamental testing concepts
2. **Best Practices**: Recommended approaches
3. **Anti-patterns**: What to avoid
4. **Examples**: Code examples of good practices
5. **Tools**: Recommended testing tools and libraries
6. **Resources**: Further learning materials

Make it practical and immediately applicable."""
    
    @staticmethod
    def conversation_prompt() -> str:
        """Template for general conversation."""
        return """Context: {context}
Previous conversation: {conversation_history}
User question: {question}

Please provide a helpful, accurate response about testing and pytest. If the question is not related to testing, politely redirect to testing topics or suggest how I can help with testing-related questions."""
