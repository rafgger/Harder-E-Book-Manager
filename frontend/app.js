const API_URL = "http://localhost:8000/books";

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
let sessionToken = null;

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
    `;
}

async function fetchBooks() {
    const headers = sessionToken ? { "Authorization": "Bearer " + sessionToken } : {};
    const res = await fetch(API_URL, { headers });
    const books = await res.json();
    renderBooks(books);
}

async function fetchBookDetail(isbn) {
    const headers = sessionToken ? { "Authorization": "Bearer " + sessionToken } : {};
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
    sessionToken = null;
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
        sessionToken = savedToken;
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
        sessionToken = data.token;
        localStorage.setItem("sessionToken", sessionToken); // Save token to localStorage
        console.log("Session token set and saved:", sessionToken); // Debugging log
        showApp();
        fetchBooks();
        showOverview();
    } catch (e) {
        console.error("Error during login:", e); // Debugging log
        if (loginError) loginError.textContent = "Login failed: " + e.message;
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
            const res = await fetch("http://localhost:8000/import-books", {
                method: "POST",
                headers: { "Authorization": "Bearer " + sessionToken },
            });
            console.log("Response status:", res.status); // Debugging log
            if (!res.ok) {
                const errorText = await res.text();
                console.error("Error response:", errorText); // Debugging log
                throw new Error("Failed to import books: " + errorText);
            }
            const data = await res.json();
            console.log("Response data:", data); // Debugging log
            alert(`${data.imported} books imported successfully!`);
            fetchBooks(); // Refresh the book list
        } catch (e) {
            console.error("Error during import:", e); // Debugging log
            alert(`Error: ${e.message}`);
        }
    });
}

if (addBtn && addFormContainer) {
    addBtn.addEventListener("click", () => {
        addFormContainer.classList.remove("hidden");
        appContainer.classList.add("hidden");
        if (addError) addError.textContent = "";
        addForm.reset();
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
            ISBN: document.getElementById("add-isbn").value.trim(),
            title: document.getElementById("add-title").value.trim(),
            author: document.getElementById("add-author").value.trim(),
            year: parseInt(document.getElementById("add-year").value, 10),
            publisher: document.getElementById("add-publisher").value.trim(),
            cover: document.getElementById("add-cover").value.trim()
        };
        try {
            const res = await fetch("http://localhost:8000/add-book", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + sessionToken
                },
                body: JSON.stringify(book)
            });
            if (!res.ok) {
                const errorText = await res.text();
                if (addError) addError.textContent = errorText;
                return;
            }
            addFormContainer.classList.add("hidden");
            appContainer.classList.remove("hidden");
            fetchBooks();
        } catch (err) {
            if (addError) addError.textContent = err.message;
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
