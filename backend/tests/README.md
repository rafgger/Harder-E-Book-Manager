# E-Book Manager Backend Tests

This directory contains the essential test suite for the E-Book Manager backend application. The tests have been refactored to remove duplicates and focus on core functionality.

## Test Files Overview

### Core Functionality Tests

#### `comprehensive_test.py` ⭐ **Main Integration Test**
- **Purpose**: Complete end-to-end testing of all system functionality
- **Coverage**: 
  - Server connectivity and availability
  - User authentication (login/logout)
  - Book addition with all fields (genre, price, rating)
  - Book retrieval and validation
  - Database persistence verification
  - Error handling and edge cases
- **Usage**: `python comprehensive_test.py`
- **When to use**: Primary test for system verification

#### `test_new_fields.py` ⭐ **New Features Test**
- **Purpose**: Specific testing of enhanced book model features
- **Coverage**:
  - Genre/Gender field mapping (API uses "genre", DB uses "gender")
  - Price field handling (string to numeric conversion)
  - Rating field handling (string to numeric conversion)
  - Data validation and type conversion
- **Usage**: `python test_new_fields.py`
- **When to use**: After changes to book model or field handling

#### `test_auth_flow.py` ⭐ **Authentication Test**
- **Purpose**: Complete authentication workflow testing
- **Coverage**:
  - HTTP Basic Auth login
  - Bearer token generation and validation
  - Protected endpoint access
  - Session management and persistence
- **Usage**: `python test_auth_flow.py`
- **When to use**: After changes to authentication system

### Database Tests

#### `check_database.py` ⭐ **Database Health Check**
- **Purpose**: Database connectivity and structure verification
- **Coverage**:
  - PostgreSQL connection and authentication
  - Books table existence and schema validation
  - Column types and constraints
  - Sample data operations
- **Usage**: `python check_database.py`
- **When to use**: Database setup verification or troubleshooting

#### `test_database.py` **Database Operations Test**
- **Purpose**: Database CRUD operations testing
- **Coverage**: Book creation, reading, updating, deletion
- **Usage**: `python test_database.py`
- **When to use**: After database schema changes

### Diagnostic Tests

#### `diagnose_500_error.py` ⭐ **Error Diagnostic**
- **Purpose**: Troubleshoot 500 Internal Server Errors
- **Coverage**:
  - Database connection issues
  - SQL execution problems
  - Data type conversion errors
  - Field mapping problems
- **Usage**: `python diagnose_500_error.py`
- **When to use**: When encountering server errors

### Utility Scripts

#### `clean_sessions.py` **Session Management**
- **Purpose**: Clean up and test session handling
- **Coverage**: Session file cleanup, token validation
- **Usage**: `python clean_sessions.py`
- **When to use**: Session corruption or authentication issues

#### `add_token.py` **Token Management**
- **Purpose**: Manual token addition for testing
- **Usage**: `python add_token.py`
- **When to use**: Manual session management

#### `read_sessions.py` **Session Inspection**
- **Purpose**: View current session state
- **Usage**: `python read_sessions.py`
- **When to use**: Debugging session issues

## Running Tests

### Using the Test Runner (Recommended)
```bash
cd backend

# List all available tests
python run_tests.py list

# Run all key tests
python run_tests.py all

# Run specific test
python run_tests.py comprehensive_test
python run_tests.py test_new_fields
python run_tests.py test_auth_flow
```

### Running Tests Directly
```bash
cd backend/tests

# Core functionality tests
python comprehensive_test.py      # Complete system test
python test_new_fields.py         # New fields testing
python test_auth_flow.py           # Authentication testing

# Database tests
python check_database.py          # Database health check
python test_database.py           # Database operations

# Diagnostic tests
python diagnose_500_error.py      # Error troubleshooting

# Utility scripts
python clean_sessions.py          # Session cleanup
python read_sessions.py           # Session inspection
```

## Test Categories

### ⭐ Essential Tests (Run First)
1. `comprehensive_test.py` - Complete system verification
2. `test_new_fields.py` - New features validation
3. `test_auth_flow.py` - Authentication verification
4. `check_database.py` - Database health check

### 🔧 Diagnostic Tests (Run When Issues Occur)
1. `diagnose_500_error.py` - Server error troubleshooting
2. `clean_sessions.py` - Session issues
3. `read_sessions.py` - Session inspection

### 📊 Database Tests (Run After DB Changes)
1. `test_database.py` - Database operations
2. `check_database.py` - Schema validation

## Prerequisites

### Backend Server
- Ensure the backend server is running: `uvicorn main:app --reload`
- Server should be accessible at `http://localhost:8000`

### Database
- PostgreSQL server running
- Database "Books" exists with proper schema
- Connection credentials configured in `config.py`

### Authentication
- Default credentials: username="user", password="123"
- Modify password in `config.py` if needed

## Test Results Interpretation

### Success Indicators
- ✅ HTTP 200 status codes
- ✅ "Test passed" messages
- ✅ Successful database operations
- ✅ Valid token generation and validation

### Failure Indicators
- ❌ HTTP 4xx/5xx status codes
- ❌ Exception tracebacks
- ❌ Database connection errors
- ❌ Authentication failures

### Common Issues and Solutions
- **Connection refused**: Start the backend server
- **401 Unauthorized**: Check password in `config.py`
- **500 Internal Server Error**: Run `diagnose_500_error.py`
- **Database errors**: Run `check_database.py`

## Maintenance

### Adding New Tests
1. Create test file in `backend/tests/`
2. Follow naming convention: `test_*.py` or `*_test.py`
3. Add documentation header with purpose and usage
4. Update this README if needed

### Removing Tests
1. Remove test file from `backend/tests/`
2. Update `run_tests.py` if it was in the key_tests list
3. Update this README

### Test Data Cleanup
- Test books persist in database with ISBNs like `test-*`, `comprehensive-*`
- Manually remove test data if needed
- Sessions are stored in `backend/sessions.pkl`

## Refactoring Notes

This test suite was refactored from 30+ files to 9 essential files:
- **Removed**: Duplicate debug scripts, overlapping functionality tests
- **Kept**: Core functionality, authentication, database, and diagnostic tests
- **Improved**: Clear documentation, focused test purposes, reduced maintenance overhead
