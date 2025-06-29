# E-Book Manager

A minimalist web application for managing e-books with a FastAPI backend and a modern, responsive frontend.

## Features
- Simple authentication (password stored in `backend/config.py`)
- Add new books with validation
- Import books from a `books.json` file
- Responsive, minimalist UI (plain JavaScript, SASS)
- PostgreSQL database integration
- Mocha/Chai frontend tests

## Installation & Setup

### Backend
1. **Install dependencies:**
   ```sh
   cd backend
   pip install -r requirements.txt
   ```
2. **Configure database:**
   - Ensure PostgreSQL is running and a database named `Books` exists with a `books` table:
     - Columns: `isbn` (PK), `title`, `author`, `year`, `publisher`, `img_m`
3. **Set password:**
   - Edit `backend/config.py` and set your desired password:
     ```python
     PASSWORD = "yourpassword"
     ```
4. **Run the backend:**
   ```sh
   uvicorn main:app --reload
   ```

### Frontend
1. Open `frontend/index.html` in your browser.
2. For tests, open `frontend/test/index.html` to view Mocha/Chai test results.

### SASS/CSS
- Edit styles in `src/style.scss` and compile to `frontend/style.css` as needed.

## Usage
- **Login:** Use the password set in `backend/config.py`.
- **Add Book:** Fill out the form and submit. All fields are required.
- **Import Books:** Click the import button to load books from `books.json`.

## Testing
- **Backend:**
  ```sh
  cd backend
  pytest
  ```
- **Frontend:**
  Open `frontend/test/index.html` in your browser.

## Project Structure
```
backend/        # FastAPI backend
frontend/       # Frontend (HTML, JS, CSS, tests)
src/            # SASS source
books.json      # Example books data
README.md       # This file
```

## License
MIT
