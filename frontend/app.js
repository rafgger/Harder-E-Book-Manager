const API_URL = "http://localhost:8000/books";

// Snackbar functionality
function showSnackbar(message, type = 'success') {
    // Remove any existing snackbar
    const existingSnackbar = document.querySelector('.snackbar');
    if (existingSnackbar) {
        existingSnackbar.remove();
    }
    
    // Create new snackbar
    const snackbar = document.createElement('div');
    snackbar.className = `snackbar ${type}`;
    snackbar.textContent = message;
    
    // Add to document
    document.body.appendChild(snackbar);
    
    // Show with animation
    setTimeout(() => {
        snackbar.classList.add('show');
    }, 100);
    
    // Hide after 4 seconds
    setTimeout(() => {
        snackbar.classList.remove('show');
        setTimeout(() => {
            if (snackbar.parentNode) {
                snackbar.parentNode.removeChild(snackbar);
            }
        }, 300);
    }, 4000);
}

const bookList = document.getElementById("book-list");
const bookDetail = document.getElementById("book-detail");
const backBtn = document.getElementById("back-btn");
const logoutBtn = document.getElementById("logout-btn");
const loginContainer = document.getElementById("login-container");
const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const appContainer = document.getElementById("app");
const importBtn = document.getElementById("import-btn");
const addBtn = document.getElementById("add-btn");
const addFormContainer = document.getElementById("add-form-container");
const addForm = document.getElementById("add-form");
const cancelAdd = document.getElementById("cancel-add");
const addError = document.getElementById("add-error");

function showOverview() {
    if (bookList) bookList.classList.remove("hidden");
    if (bookDetail) bookDetail.classList.add("hidden");
    if (backBtn) backBtn.classList.add("hidden");
}

function showDetail() {
    if (bookList) bookList.classList.add("hidden");
    if (bookDetail) bookDetail.classList.remove("hidden");
    if (backBtn) backBtn.classList.remove("hidden");
}

function renderBooks(books) {
    if (!bookList) return;
    bookList.innerHTML = books.map(book => `
        <div class="book-card" data-isbn="${book.ISBN}">
            <img class="book-cover" src="${book.cover}" alt="${book.title}">
            <div class="book-title">${book.title}</div>
            <div class="book-author">${book.author}</div>
            <div class="book-year">${book.year}</div>
            <div class="book-genre">${book.genre || 'Unknown'}</div>
            <div class="book-price">$${book.price || 'N/A'}</div>
            <div class="book-rating">★ ${book.rating || 'N/A'}</div>
        </div>
    `).join("");
}

function renderBookDetail(book) {
    if (!bookDetail) return;
    bookDetail.innerHTML = `
        <img src="${book.cover}" alt="${book.title}">
        <h2>${book.title}</h2>
        <div class="meta"><strong>Author:</strong> ${book.author}</div>
        <div class="meta"><strong>Year:</strong> ${book.year}</div>
        <div class="meta"><strong>Publisher:</strong> ${book.publisher}</div>
        <div class="meta"><strong>ISBN:</strong> ${book.ISBN}</div>
        <div class="meta"><strong>Genre:</strong> ${book.genre || 'Unknown'}</div>
        <div class="meta"><strong>Price:</strong> $${book.price || 'N/A'}</div>
        <div class="meta"><strong>Rating:</strong> ★ ${book.rating || 'N/A'}/5</div>
    `;
}

function getSessionToken() {
    // Always get the latest token from localStorage
    const token = localStorage.getItem("sessionToken");
    if (!token || token === "null" || token.length < 10) return null;
    return token;
}

async function fetchBooks() {
    const token = getSessionToken();
    const headers = token ? { "Authorization": "Bearer " + token } : {};
    const res = await fetch(API_URL, { headers });
    const books = await res.json();
    renderBooks(books);
}

async function fetchBookDetail(isbn) {
    const token = getSessionToken();
    const headers = token ? { "Authorization": "Bearer " + token } : {};
    const res = await fetch(`${API_URL}/${isbn}`, { headers });
    const book = await res.json();
    renderBookDetail(book);
    showDetail();
}

function forceRepaint(element) {
    if (element) {
        element.style.display = "none";
        element.offsetHeight; // Trigger reflow
        element.style.display = "";
    }
}

function showLogin() {
    console.log("showLogin called"); // Debugging log
    if (loginContainer) {
        loginContainer.style.display = "flex"; // Directly set display property
        console.log("loginContainer style.display:", loginContainer.style.display);
    }
    if (appContainer) {
        appContainer.style.display = "none"; // Directly set display property
        console.log("appContainer style.display:", appContainer.style.display);
    }
}

function showApp() {
    console.log("showApp called"); // Debugging log
    if (loginContainer) {
        loginContainer.style.display = "none"; // Directly set display property
        console.log("loginContainer style.display:", loginContainer.style.display);
    }
    if (appContainer) {
        appContainer.style.display = "block"; // Directly set display property
        console.log("appContainer style.display:", appContainer.style.display);
    }
    if (logoutBtn) {
        logoutBtn.style.display = "inline-block"; // Directly set display property
        console.log("logoutBtn style.display:", logoutBtn.style.display);
    }
}

function logout() {
    localStorage.removeItem("sessionToken"); // Remove token from localStorage
    showLogin();
    if (loginForm) loginForm.reset();
    if (loginError) loginError.textContent = "";
}

// Check for an existing session token on page load
window.addEventListener("load", () => {
    const savedToken = localStorage.getItem("sessionToken");
    if (savedToken) {
        console.log("Found saved session token:", savedToken); // Debugging log
        showApp();
        fetchBooks();
        showOverview();
    } else {
        console.log("No saved session token found"); // Debugging log
        showLogin();
    }
});

async function login(password) {
    try {
        console.log("Attempting login with password:", password); // Debugging log
        const res = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: { "Authorization": "Basic " + btoa(":" + password) },
        });
        console.log("Login response status:", res.status); // Debugging log
        if (!res.ok) {
            const errorText = await res.text();
            console.error("Login error response:", errorText); // Debugging log
            throw new Error("Invalid password: " + errorText);
        }
        const data = await res.json();
        console.log("Login response data:", data); // Debugging log
        localStorage.setItem("sessionToken", data.token); // Save token to localStorage
        console.log("Session token set and saved:", data.token); // Debugging log
        showSnackbar("Login successful!");
        showApp();
        fetchBooks();
        showOverview();
    } catch (e) {
        console.error("Error during login:", e); // Debugging log
        if (loginError) loginError.textContent = "Login failed: " + e.message;
        showSnackbar("Login failed: " + e.message, "error");
    }
}

if (bookList) {
    bookList.addEventListener("click", e => {
        const card = e.target.closest(".book-card");
        if (card) {
            fetchBookDetail(card.dataset.isbn);
        }
    });
}

if (backBtn) {
    backBtn.addEventListener("click", () => {
        showOverview();
    });
}

if (loginForm) {
    loginForm.addEventListener("submit", e => {
        e.preventDefault();
        const pw = document.getElementById("password").value;
        login(pw);
    });
}

if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
}

if (importBtn) {
    importBtn.addEventListener("click", async () => {
        try {
            console.log("Import button clicked"); // Debugging log
            const token = getSessionToken();
            const res = await fetch("http://localhost:8000/import-books", {
                method: "POST",
                headers: { "Authorization": "Bearer " + token },
            });
            console.log("Response status:", res.status); // Debugging log
            if (!res.ok) {
                const errorText = await res.text();
                console.error("Error response:", errorText); // Debugging log
                throw new Error("Failed to import books: " + errorText);
            }
            const data = await res.json();
            console.log("Response data:", data); // Debugging log
            showSnackbar(`${data.imported} books imported successfully!`);
            fetchBooks(); // Refresh the book list
        } catch (e) {
            console.error("Error during import:", e); // Debugging log
            showSnackbar(`Error: ${e.message}`, 'error');
        }
    });
}

if (addBtn && addFormContainer) {
    addBtn.addEventListener("click", () => {
        addFormContainer.classList.remove("hidden");
        appContainer.classList.add("hidden");
        if (addError) addError.textContent = "";
        // Prefill the form with default values
        document.getElementById("add-isbn").value = "123";
        document.getElementById("add-title").value = "Default Title";
        document.getElementById("add-author").value = "Default Author";
        document.getElementById("add-year").value = "2025";
        document.getElementById("add-publisher").value = "Default Publisher";
        document.getElementById("add-cover").value = "http://example.com/default-cover.jpg";
    });
}
if (cancelAdd && addFormContainer && appContainer) {
    cancelAdd.onclick = function(e) {
        e.preventDefault();
        addFormContainer.classList.add("hidden");
        appContainer.classList.remove("hidden");
    };
}
if (addForm) {
    addForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const book = {
            "ISBN": document.getElementById("add-isbn").value.trim(),
            "title": document.getElementById("add-title").value.trim(),
            "author": document.getElementById("add-author").value.trim(),
            "year": parseInt(document.getElementById("add-year").value, 10),
            "publisher": document.getElementById("add-publisher").value.trim(),
            "cover": document.getElementById("add-cover").value.trim(),
            "gender": document.getElementById("add-genre").value.trim(),  // Backend expects "gender" field
            "price": document.getElementById("add-price").value.trim(),
            "rating": document.getElementById("add-rating").value.trim()
        };
        const token = getSessionToken();
        if (!token) {
            console.error("[DEBUG] No session token found. Redirecting to login."); // Debug log
            if (addError) addError.textContent = "You are not logged in. Please log in again.";
            showSnackbar("You are not logged in. Please log in again.", "error");
            showLogin();
            return;
        }
        console.log("[DEBUG] Submitting book to /add-book:", book); // Debug log
        console.log("[DEBUG] Outgoing Authorization header:", "Bearer " + token); // Debug log
        try {
            const res = await fetch("http://localhost:8000/add-book", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify(book)
            });
            console.log("[DEBUG] Response status:", res.status); // Debug log
            if (res.status === 401) {
                console.error("[DEBUG] Session expired. Redirecting to login."); // Debug log
                localStorage.removeItem("sessionToken");
                if (addError) addError.textContent = "Session expired. Please log in again.";
                showSnackbar("Session expired. Please log in again.", "error");
                showLogin();
                return;
            }
            if (!res.ok) {
                const errorText = await res.text();
                console.error("[DEBUG] Error response from /add-book:", errorText); // Debug log
                if (addError) addError.textContent = errorText;
                
                // Parse error message for user-friendly display
                let errorMessage = "Failed to add book";
                try {
                    const errorData = JSON.parse(errorText);
                    if (errorData.detail) {
                        errorMessage = errorData.detail;
                    }
                } catch (e) {
                    errorMessage = errorText || "Failed to add book";
                }
                
                showSnackbar(errorMessage, "error");
                return;
            }
            console.log("[DEBUG] Book added successfully."); // Debug log
            addFormContainer.classList.add("hidden");
            appContainer.classList.remove("hidden");
            fetchBooks();
            showSnackbar("Book added successfully!");
        } catch (err) {
            console.error("[DEBUG] Exception during /add-book request:", err); // Debug log
            if (addError) addError.textContent = err.message;
            showSnackbar("Network error: " + err.message, "error");
        }
    });
}

// Initial load (only if elements exist)
if (bookList && bookDetail && backBtn) {
    showLogin();
}

// For testing purposes
window.renderBooks = renderBooks;
window.renderBookDetail = renderBookDetail;
window.bookDetail = bookDetail;
window.bookList = bookList;
window.backBtn = backBtn;
