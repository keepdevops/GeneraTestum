# API Documentation

## 📋 Overview

This document provides comprehensive API documentation for the test suite.

## 🔗 Endpoints

### Base URL

```
http://localhost:5000
```

### Authentication

No authentication required for test endpoints.

## 📚 API Reference

### Test Endpoints

#### GET /tests
Get all available tests.

**Response:**
```json
{
  "tests": [
    {
      "id": "test_calculator_add",
      "name": "test_calculator_add",
      "description": "Test calculator addition functionality",
      "status": "pass",
      "duration": 0.001
    }
  ],
  "total": 1,
  "passed": 1,
  "failed": 0
}
```

#### POST /tests/run
Run specific tests.

**Request Body:**
```json
{
  "test_ids": ["test_calculator_add"],
  "options": {
    "verbose": true,
    "coverage": true
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "test_calculator_add",
      "status": "pass",
      "duration": 0.001,
      "output": "Test passed successfully"
    }
  ],
  "summary": {
    "total": 1,
    "passed": 1,
    "failed": 0,
    "duration": 0.001
  }
}
```

#### GET /coverage
Get test coverage information.

**Response:**
```json
{
  "coverage_percentage": 85.5,
  "files": [
    {
      "file": "src/calculator.py",
      "coverage": 90.0,
      "lines_covered": 18,
      "lines_total": 20
    }
  ],
  "summary": {
    "lines_covered": 180,
    "lines_total": 200,
    "branches_covered": 45,
    "branches_total": 50
  }
}
```

#### GET /security
Get security test results.

**Response:**
```json
{
  "vulnerabilities": [
    {
      "type": "sql_injection",
      "severity": "high",
      "description": "Potential SQL injection vulnerability",
      "file": "src/database.py",
      "line": 25
    }
  ],
  "summary": {
    "total": 1,
    "critical": 0,
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
```

#### GET /performance
Get performance test results.

**Response:**
```json
{
  "performance_tests": [
    {
      "function": "calculate_fibonacci",
      "execution_time": 0.001,
      "max_time": 0.1,
      "status": "pass",
      "memory_usage": 1024
    }
  ],
  "summary": {
    "total": 1,
    "passed": 1,
    "failed": 0,
    "average_time": 0.001
  }
}
```

## 🔧 Configuration

### Test Configuration

```json
{
  "test_framework": "pytest",
  "mock_level": "comprehensive",
  "coverage_threshold": 80,
  "include_performance_tests": true,
  "include_security_tests": true,
  "include_integration_tests": true,
  "timeout": 300,
  "parallel": true,
  "workers": 4
}
```

### API Configuration

```json
{
  "base_url": "http://localhost:5000",
  "timeout": 30,
  "retries": 3,
  "headers": {
    "Content-Type": "application/json",
    "User-Agent": "pytest-gen/1.0.0"
  }
}
```

## 📊 Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request |
| 401  | Unauthorized |
| 403  | Forbidden |
| 404  | Not Found |
| 500  | Internal Server Error |

## 🧪 Testing the API

### Using curl

```bash
# Get all tests
curl -X GET http://localhost:5000/tests

# Run specific test
curl -X POST http://localhost:5000/tests/run \
  -H "Content-Type: application/json" \
  -d '{"test_ids": ["test_calculator_add"]}'

# Get coverage
curl -X GET http://localhost:5000/coverage
```

### Using Python requests

```python
import requests

# Get all tests
response = requests.get('http://localhost:5000/tests')
tests = response.json()

# Run specific test
response = requests.post('http://localhost:5000/tests/run', 
                        json={'test_ids': ['test_calculator_add']})
result = response.json()

# Get coverage
response = requests.get('http://localhost:5000/coverage')
coverage = response.json()
```

## 📈 Monitoring

### Health Check

```bash
curl -X GET http://localhost:5000/health
```

### Metrics

```bash
curl -X GET http://localhost:5000/metrics
```

---

**Last Updated**: 2025-10-14 16:44:09
