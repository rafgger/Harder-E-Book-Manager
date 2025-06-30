# E-Book Manager Frontend Test Suite

This directory contains the complete frontend test suite for the E-Book Manager application.

## Test Files Overview

### 🔧 Unit Tests (No Backend Required)
- **`form-tests.html`** - Comprehensive frontend form testing without backend dependency
  - Tests: Session handling, form validation, book object construction, UI state management
  - Coverage: 12 comprehensive test cases
  - Usage: Open in browser, tests run automatically

- **`test-runner.html`** - Professional Mocha/Chai test framework
  - Tests: Book rendering, login/logout flow, session management
  - Framework: Uses Mocha and Chai from CDN
  - Usage: Open in browser for structured test reporting

### 🔗 Integration Tests (Backend Required)
- **`real-backend-test.html`** - Complete backend integration testing
  - Tests: HTTP Basic Auth, Bearer tokens, form submission, CORS
  - Requirements: Backend server running at localhost:8000
  - Usage: Primary integration test suite

- **`add-book-test.html`** - Focused book addition functionality testing
  - Tests: Authentication flow, book validation, database persistence
  - Requirements: Backend server running
  - Usage: Specific book addition workflow testing

- **`server-status-check.html`** - Backend connectivity and health check
  - Tests: Server availability, API endpoints, response times
  - Requirements: Backend server running
  - Usage: Quick connectivity verification

### 🐛 Debug & Diagnostic Tools
- **`debug-form-test.html`** - Advanced form submission debugging
  - Tools: Token validation, request/response logging, error diagnosis
  - Requirements: Backend server running
  - Usage: Troubleshooting form submission issues

### 📚 Documentation & Legacy
- **`index.html`** - Legacy test index (original simple interface)
- **`app.test.js`** - JavaScript test utilities and helper functions
- **`README.html`** - Interactive test suite dashboard (recommended entry point)

## Quick Start

### 1. Unit Testing (No Backend)
```bash
# Open any of these in your browser:
frontend/test/form-tests.html      # Main unit tests
frontend/test/test-runner.html     # Mocha test framework
```

### 2. Integration Testing (Backend Required)
```bash
# First, start the backend:
cd backend
uvicorn main:app --reload

# Then open these in your browser:
frontend/test/real-backend-test.html    # Main integration tests
frontend/test/add-book-test.html        # Book addition tests
frontend/test/server-status-check.html  # Quick connectivity check
```

### 3. Debug & Troubleshooting
```bash
# If you encounter issues:
frontend/test/debug-form-test.html      # Advanced debugging tools
```

## Test Suite Dashboard

**Recommended:** Open `frontend/test/README.html` in your browser for an interactive test suite dashboard with organized access to all tests.

## Test Categories Explained

### Unit Tests
- Run entirely in the browser
- No backend connectivity required
- Test frontend logic, form handling, UI components
- Ideal for development and CI/CD pipelines

### Integration Tests
- Require live backend server at localhost:8000
- Test complete workflows from frontend to database
- Verify authentication, API communication, data persistence
- Essential for pre-deployment validation

### Debug Tools
- Advanced troubleshooting utilities
- Token validation and session debugging
- Request/response logging and analysis
- Used when investigating specific issues

## Prerequisites

### For Unit Tests
- Modern web browser with JavaScript enabled
- No additional setup required

### For Integration Tests
- Backend server running: `uvicorn main:app --reload`
- PostgreSQL database configured and running
- Default credentials: username=`user`, password=`123`

### For All Tests
- Files must be served from the correct directory structure
- Some tests may require local server for CORS compatibility

## Test Data Management

- Tests create books with ISBNs like `test-*`, `frontend-*`, `debug-*`
- Test data persists in the database
- Manually clean test data if needed
- Session tokens are managed automatically

## Troubleshooting

### Common Issues
- **CORS Errors**: Serve files from a local server instead of file:// protocol
- **Backend Connection Failed**: Ensure backend is running at localhost:8000
- **Authentication Errors**: Verify credentials in backend/config.py
- **Test Data Conflicts**: Use unique ISBNs or clean test data

### Debug Process
1. Run `server-status-check.html` to verify backend connectivity
2. Run `form-tests.html` to verify frontend functionality
3. Run `real-backend-test.html` for complete integration testing
4. Use `debug-form-test.html` for specific issue investigation

## Coverage Matrix

| Feature Area | Unit Tests | Integration Tests | Debug Tools |
|--------------|------------|-------------------|-------------|
| Authentication | ✅ Mock tests | ✅ Real HTTP Basic Auth | ✅ Token validation |
| Form Handling | ✅ Complete validation | ✅ Real submissions | ✅ Request logging |
| Book Operations | ✅ Object construction | ✅ Database persistence | ✅ Error diagnosis |
| UI Components | ✅ State management | ✅ Visual feedback | ✅ Debug interfaces |
| Error Handling | ✅ Mock scenarios | ✅ Real error responses | ✅ Troubleshooting |

## Maintenance

### Adding New Tests
1. Create test file in `frontend/test/`
2. Follow naming convention: `*-test.html` or `test-*.html`
3. Update `README.html` dashboard if needed
4. Document test purpose and requirements

### Test Organization
- Keep unit tests separate from integration tests
- Use clear naming conventions
- Maintain comprehensive documentation
- Ensure tests are self-contained and repeatable
