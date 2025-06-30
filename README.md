# E-Book Manager

A minimalist web application for managing e-books with a FastAPI backend and a modern, responsive frontend featuring session-based authentication and real-time notifications.

## Features
- **Session-based authentication** with Bearer token support
- **Add new books** with comprehensive validation and duplicate checking (includes genre, price, and rating)
- **Import books** from a `books.json` file with progress feedback
- **Enhanced book display** showing cover, title, author, year, genre, price, and rating
- **Real-time notifications** via snackbar alerts for all user actions
- **Responsive, minimalist UI** (plain JavaScript, CSS)
- **PostgreSQL database integration** with full CRUD operations
- **Comprehensive test suite** for both frontend and backend
- **CORS support** for cross-origin requests
- **Robust error handling** with user-friendly messages

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Node.js (optional, for SASS compilation)

### Backend
1. **Create and activate virtual environment:**
   ```sh
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```sh
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure database:**
   - Ensure PostgreSQL is running and a database named `Books` exists with a `books` table:
     - Columns: `isbn` (PK), `title`, `author`, `year`, `publisher`, `img_m`, `genre`, `price`, `rating`
   - Example SQL to create the table:
     ```sql
     CREATE TABLE books (
         isbn VARCHAR(20) PRIMARY KEY,
         title VARCHAR(500),
         author VARCHAR(200),
         year INTEGER,
         publisher VARCHAR(200),
         img_m VARCHAR(500),
         genre VARCHAR(50),
         price VARCHAR(10),
         rating VARCHAR(5)
     );
     ```

4. **Set password:**
   - Edit `backend/config.py` and set your desired password:
     ```python
     PASSWORD = "123"
     ```

5. **Run the backend:**
   ```sh
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000` with interactive API docs at `http://localhost:8000/docs`

### Frontend
1. **Open the application:**
   - Open `frontend/index.html` in your browser
   - Or serve it from a local server for better CORS handling

2. **Login credentials:**
   - Username: `user`
   - Password: `123` (or whatever you set in `backend/config.py`)

### SASS/CSS
- Edit styles in `src/style.scss` and compile to `frontend/style.css` as needed.

## Usage
- **Login:** Use username `user` and the password set in `backend/config.py`
- **Add Book:** Click the `+` button, fill out the form (all fields required), and submit
- **Import Books:** Click "Import Books" to load books from `books.json`
- **Visual Feedback:** Green snackbars for success, red for errors
- **Session Management:** Automatic logout on token expiration with clear notifications

## API Endpoints
- `POST /login` - Authenticate with HTTP Basic Auth
- `GET /books` - Get all books (requires Bearer token)
- `GET /books/{isbn}` - Get specific book (requires Bearer token)
- `POST /add-book` - Add new book (requires Bearer token)
- `POST /import-books` - Import books from JSON (requires Bearer token)

## Testing
- **Backend:**
  ```sh
  cd backend
  
  # Use the test runner (recommended)
  python run_tests.py list                    # List all available tests
  python run_tests.py all                     # Run key tests
  python run_tests.py test_new_fields         # Run specific test
  
  # Or run tests directly from tests/ directory
  python tests/test_auth_flow.py              # Test authentication flow
  python tests/end_to_end_test.py             # Test complete API flow
  python tests/complete_test.py               # Complete flow with proper field handling
  ```
- **Frontend:**
  - Open `frontend/test/form-tests.html` for comprehensive form tests
  - Open `frontend/debug-form-test.html` for real backend testing

## Available Tests

### Backend Test Suite (Located in `backend/tests/`)

#### Core Testing Scripts
##### `tests/test_auth_flow.py`
- **Purpose:** Tests the complete authentication and book addition workflow
- **Functionality:**
  - Validates HTTP Basic Auth login process
  - Tests Bearer token authentication for protected endpoints
  - Verifies book addition with proper authorization
  - Confirms database persistence of added books
- **Usage:** `python tests/test_auth_flow.py`

##### `tests/end_to_end_test.py`
- **Purpose:** Comprehensive API testing suite
- **Functionality:**
  - Tests server connectivity and availability
  - Validates login endpoint with various scenarios
  - Tests book addition with different data formats
  - Verifies book retrieval functionality
  - Tests error handling and validation
- **Usage:** `python tests/end_to_end_test.py`

##### `tests/complete_test.py`
- **Purpose:** Full flow testing using Python's urllib (no external dependencies)
- **Functionality:**
  - Tests login flow identical to frontend implementation
  - Validates book addition with pure Python HTTP requests
  - Demonstrates backend compatibility with different HTTP libraries
- **Usage:** `python tests/complete_test.py`

#### Authentication & Token Testing
##### `tests/token_test.py`
- **Purpose:** Specific token validation testing
- **Functionality:**
  - Tests problematic tokens from frontend logs
  - Compares fresh vs. expired token behavior
  - Diagnoses authentication issues
- **Usage:** `python tests/token_test.py`

##### `tests/test_auth_fix.py`
- **Purpose:** Validates authentication system fixes
- **Functionality:**
  - Tests Bearer token authentication after system updates
  - Verifies proper handling of authorization headers
  - Confirms book addition with authenticated requests
- **Usage:** `python tests/test_auth_fix.py`

#### Specialized Testing Scripts
##### `tests/test_add_book.py`
- **Purpose:** Focused book addition testing
- **Functionality:**
  - Tests manual book addition workflow
  - Validates book data persistence
  - Tests authorization headers formatting
- **Usage:** `python tests/test_add_book.py` (update password variable first)

##### `tests/simple_test.py`
- **Purpose:** Basic connectivity and functionality testing
- **Functionality:**
  - Tests server connection and availability
  - Basic login functionality testing
  - Simple book addition testing
- **Usage:** `python tests/simple_test.py`

##### `tests/quick_test.py`, `tests/manual_test.py`
- **Purpose:** Quick debugging and manual testing utilities
- **Functionality:** Minimal test scripts for rapid debugging
- **Usage:** `python tests/[script_name].py`

### Frontend Test Suite

#### Comprehensive Testing Pages
##### `frontend/test/form-tests.html`
- **Purpose:** Comprehensive frontend form testing without backend dependency
- **Functionality:**
  - Session token retrieval and validation
  - Book object construction from form data
  - Authorization header formatting
  - Book list rendering simulation
  - UI state management testing
  - Form prefill and cancellation logic
  - Mock backend interaction testing
  - Real form submission event simulation
  - Error handling for various scenarios
- **Coverage:** 12 comprehensive test cases
- **Usage:** Open in browser, tests run automatically

##### `frontend/test/test-runner.html`
- **Purpose:** Mocha-based testing framework setup
- **Functionality:**
  - Professional test runner using Mocha and Chai
  - Book rendering and display testing
  - Login/logout flow validation
  - Session token management verification
  - Form input validation testing
- **Usage:** Open in browser (requires Mocha/Chai from CDN)

#### Real Backend Integration Tests
##### `frontend/debug-form-test.html`
- **Purpose:** Real-time testing with actual backend
- **Functionality:**
  - Backend connectivity verification
  - Live HTTP Basic Auth login testing
  - Bearer token validation with real tokens
  - Actual form submission to backend
  - Real-time error diagnosis
  - CORS and network issue detection
- **Usage:** Open in browser (requires running backend)

##### `frontend/test/real-backend-test.html`
- **Purpose:** Cross-origin request testing
- **Functionality:**
  - Tests form submission from file:// protocol
  - CORS compatibility verification
  - Network error identification
  - Same-origin vs. cross-origin behavior comparison
- **Usage:** Open in browser (requires running backend)

#### Test Utilities
##### `frontend/test/app.test.js`
- **Purpose:** JavaScript unit test utilities
- **Functionality:**
  - Reusable test functions for frontend components
  - Mock data and helper functions
  - Integration with test HTML pages
- **Usage:** Included in test HTML pages

### Test Coverage Matrix

| Test Area | Backend Tests | Frontend Tests | Coverage Level |
|-----------|---------------|----------------|----------------|
| **Authentication** | ✅ `test_auth_flow.py`<br>✅ `test_auth_fix.py`<br>✅ `token_test.py` | ✅ `debug-form-test.html`<br>✅ `form-tests.html` | Complete |
| **Authorization** | ✅ Bearer token validation<br>✅ Session management | ✅ Token handling<br>✅ Header formatting | Complete |
| **Database Operations** | ✅ Book CRUD operations<br>✅ Persistence validation<br>✅ Duplicate checking | ✅ Mock database tests<br>✅ Real backend integration | Complete |
| **Form Handling** | ✅ Data validation<br>✅ Error responses | ✅ Form validation<br>✅ Submission logic<br>✅ Error handling | Complete |
| **UI Interactions** | N/A | ✅ State management<br>✅ Visual feedback<br>✅ Snackbar notifications | Complete |
| **Network Communications** | ✅ HTTP request/response<br>✅ Error codes | ✅ CORS handling<br>✅ Network errors<br>✅ Cross-origin requests | Complete |
| **Error Scenarios** | ✅ Invalid auth<br>✅ Database errors<br>✅ Validation failures | ✅ Network failures<br>✅ Invalid tokens<br>✅ Form errors | Complete |
| **User Experience** | ✅ API response times<br>✅ Error messages | ✅ Notifications<br>✅ Form prefilling<br>✅ Visual feedback | Complete |

### Running Test Suites

#### Backend Test Execution
```bash
cd backend

# Use the test runner (recommended)
python run_tests.py all                    # Run all key tests
python run_tests.py list                   # List available tests  
python run_tests.py test_new_fields        # Run specific test

# Or run tests directly from tests/ directory
python tests/test_auth_flow.py             # Core authentication test
python tests/end_to_end_test.py            # Comprehensive API test
python tests/complete_test.py              # Complete flow test

# Run specialized tests
python tests/test_auth_fix.py              # Authentication fixes
python tests/token_test.py                 # Token validation
python tests/test_add_book.py              # Book addition test

# Quick connectivity tests  
python tests/simple_test.py               # Basic connectivity
python tests/diagnose_500_error.py        # Database diagnostics
```

#### Frontend Test Execution
1. **Automated Unit Tests:**
   - Open `frontend/test/form-tests.html` in browser
   - Tests run automatically on page load
   - View results in browser console and on page
   - **Coverage:** 12 comprehensive test cases including session management, form handling, network requests, and error scenarios

2. **Professional Test Runner:**
   - Open `frontend/test/test-runner.html` in browser
   - Uses Mocha/Chai framework for structured testing
   - Interactive test results display

3. **Real Backend Integration:**
   - Start backend server: `uvicorn main:app --reload`
   - Open `frontend/debug-form-test.html` in browser
   - Performs live API testing with real server

4. **CORS and Cross-Origin Testing:**
   - Ensure backend is running
   - Open `frontend/test/real-backend-test.html` in browser
   - Tests file:// protocol compatibility

#### Complete Test Run
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Run backend tests
cd backend
python run_tests.py all                     # Run all key tests with test runner
python run_tests.py list                    # List all available tests
python run_tests.py comprehensive_test      # Run comprehensive functionality test

# OR run individual tests:
python tests/test_auth_flow.py && python tests/end_to_end_test.py && python tests/complete_test.py

# For debugging server issues:
python tests/diagnose_500_error.py          # Database diagnostics
python tests/isolated_add_test.py          # Isolated add-book testing

# Browser: Open frontend test files
# 1. frontend/test/form-tests.html
# 2. frontend/debug-form-test.html
# 3. frontend/test/real-backend-test.html
```

### Test Debugging and Reporting

#### Backend Test Output
- **Success Indicators:** HTTP 200 status codes, "Test passed" messages
- **Failure Indicators:** HTTP 4xx/5xx status codes, exception tracebacks
- **Debug Information:** Token values, request/response data, database states

#### Frontend Test Output
- **Browser Console:** Detailed test results and error messages
- **Visual Indicators:** Green checkmarks for passed tests, red X for failures
- **Interactive Results:** Click on test results for detailed information

#### Common Test Issues and Solutions
- **Backend Connection Failed:** Ensure `uvicorn main:app --reload` is running
- **401 Unauthorized:** Check password in `config.py` matches test scripts
- **CORS Errors:** Use a local server instead of opening HTML files directly
- **Database Errors:** Verify PostgreSQL is running and `Books` database exists
- **Token Validation Failed:** Check for expired sessions, restart backend if needed

#### Test Data Management
- **Test Books:** Tests create books with ISBNs like `test-*`, `auth-test-*`, `manual-*`
- **Cleanup:** Test books persist in database - manually remove if needed
- **Sessions:** Backend maintains session tokens in `sessions.pkl` file

## Project Structure
## Project Structure
```
backend/                    # FastAPI backend
├── main.py                # Main application with all endpoints
├── config.py              # Configuration (password)
├── requirements.txt       # Python dependencies
├── sessions.pkl           # Session token storage
├── run_tests.py           # Test runner script
└── tests/                 # Test files directory
    ├── __init__.py        # Python package initialization
    ├── test_auth_flow.py  # Authentication testing
    ├── end_to_end_test.py # Complete API testing
    ├── complete_test.py   # Full flow testing
    ├── test_new_fields.py # New fields testing
    ├── diagnose_500_error.py # Database diagnostics
    └── *.py               # Various other test scripts

frontend/                   # Frontend application
├── index.html             # Main application page
├── app.js                 # JavaScript application logic
├── style.css              # Compiled CSS styles
├── debug-form-test.html   # Real backend testing page
└── test/                  # Test files
    ├── form-tests.html    # Comprehensive form tests
    └── *.js               # Test utilities

src/                       # SASS source files
├── style.scss             # Main SASS source

books.json                 # Example books data for import
Books.csv                  # Sample data in CSV format
README.md                  # This file
```

## Recent Improvements
- ✅ **Fixed authentication system** - Proper Bearer token handling
- ✅ **Added real database persistence** - Books are actually saved to PostgreSQL
- ✅ **Implemented snackbar notifications** - Visual feedback for all actions
- ✅ **Enhanced error handling** - User-friendly error messages
- ✅ **Comprehensive testing** - Frontend and backend test suites
- ✅ **Session management** - Robust token validation and cleanup
- ✅ **CORS support** - Cross-origin request handling
- ✅ **Fixed field consistency** - Updated all tests to use "gender" field consistently
- ✅ **Organized test structure** - All backend tests moved to dedicated `tests/` directory
- ✅ **Added test runner** - Convenient `run_tests.py` script for easy test execution
- ✅ **Database diagnostics** - Tools to troubleshoot database issues and field mapping

## Troubleshooting
- **401 Unauthorized errors:** Ensure you're logged in and have a valid session token
- **Database connection issues:** Verify PostgreSQL is running and the database exists
- **Import failures:** Check that `books.json` exists and has the correct format
- **CORS errors:** Serve the frontend from a local server instead of opening directly
- **500 Internal Server Errors when adding books:** The server may need to be restarted if it becomes unresponsive. Stop the server (Ctrl+C) and restart with `uvicorn main:app --reload`
- **Field mapping issues:** The database has both 'gender' and 'genre' columns - the Book model uses 'gender' column for data storage
- **Test book duplicates:** Test books persist in the database. Use unique ISBNs or manually clean test data if needed

## License
MIT

Used adjusted data set:
J. Schler, M. Koppel, S. Argamon and J. Pennebaker (2006). Effects of Age and Gender on Blogging in Proceedings of 2006 AAAI Spring Symposium on Computational Approaches for Analyzing Weblogs. URL: http://www.cs.biu.ac.il/~schlerj/schler_springsymp06.pdf
