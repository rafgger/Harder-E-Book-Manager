const API_URL = "http://localhost:8000/books";

const bookList = document.getElementById("book-list");
const bookDetail = document.getElementById("book-detail");
const backBtn = document.getElementById("back-btn");

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
    const res = await fetch(API_URL);
    const books = await res.json();
    renderBooks(books);
}

async function fetchBookDetail(isbn) {
    const res = await fetch(`${API_URL}/${isbn}`);
    const book = await res.json();
    renderBookDetail(book);
    showDetail();
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

// Initial load (only if elements exist)
if (bookList && bookDetail && backBtn) {
    fetchBooks();
    showOverview();
}

// For testing purposes
window.renderBooks = renderBooks;
window.renderBookDetail = renderBookDetail;
window.bookDetail = bookDetail;
window.bookList = bookList;
window.backBtn = backBtn;
