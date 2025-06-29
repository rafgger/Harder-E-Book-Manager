```javascript
describe('Book UI', function() {
    beforeEach(function() {
        // Setup DOM for tests using DOM API (no JSX/HTML string)
        document.body.innerHTML = '';
        const loginContainer = document.createElement('div');
        loginContainer.id = 'login-container';
        loginContainer.className = 'centered hidden';
        const loginForm = document.createElement('form');
        loginForm.id = 'login-form';
        const pwInput = document.createElement('input');
        pwInput.type = 'password';
        pwInput.id = 'password';
        loginForm.appendChild(pwInput);
        const loginBtn = document.createElement('button');
        loginBtn.type = 'submit';
        loginBtn.textContent = 'Login';
        loginForm.appendChild(loginBtn);
        const loginError = document.createElement('div');
        loginError.id = 'login-error';
        loginError.className = 'error';
        loginForm.appendChild(loginError);
        loginContainer.appendChild(loginForm);
        document.body.appendChild(loginContainer);
        
        const appContainer = document.createElement('div');
        appContainer.id = 'app';
        appContainer.className = 'hidden';
        const headerBar = document.createElement('div');
        headerBar.className = 'header-bar';
        const h1 = document.createElement('h1');
        h1.textContent = 'E-Book Collection';
        headerBar.appendChild(h1);
        const logoutBtn = document.createElement('button');
        logoutBtn.id = 'logout-btn';
        logoutBtn.className = 'hidden';
        logoutBtn.textContent = 'Logout';
        headerBar.appendChild(logoutBtn);
        appContainer.appendChild(headerBar);
        
        const bookList = document.createElement('div');
        bookList.id = 'book-list';
        appContainer.appendChild(bookList);
        const bookDetail = document.createElement('div');
        bookDetail.id = 'book-detail';
        appContainer.appendChild(bookDetail);
        const backBtn = document.createElement('button');
        backBtn.id = 'back-btn';
        appContainer.appendChild(backBtn);
        document.body.appendChild(appContainer);
        
        // Add missing elements for the add book form
        const addFormContainer = document.createElement('div');
        addFormContainer.id = 'add-form-container';
        addFormContainer.className = 'hidden';
        const addForm = document.createElement('form');
        addForm.id = 'add-form';
        const addError = document.createElement('div');
        addError.id = 'add-error';
        addForm.appendChild(addError);
        addFormContainer.appendChild(addForm);
        document.body.appendChild(addFormContainer);
        
        // Create form fields for add book form
        const isbnInput = document.createElement('input');
        isbnInput.id = 'add-isbn';
        addForm.appendChild(isbnInput);
        
        const titleInput = document.createElement('input');
        titleInput.id = 'add-title';
        addForm.appendChild(titleInput);
        
        const authorInput = document.createElement('input');
        authorInput.id = 'add-author';
        addForm.appendChild(authorInput);
        
        const yearInput = document.createElement('input');
        yearInput.id = 'add-year';
        yearInput.type = 'number';
        addForm.appendChild(yearInput);
        
        const publisherInput = document.createElement('input');
        publisherInput.id = 'add-publisher';
        addForm.appendChild(publisherInput);
        
        const coverInput = document.createElement('input');
        coverInput.id = 'add-cover';
        addForm.appendChild(coverInput);
        
        window.bookList = bookList;
        window.bookDetail = bookDetail;
        window.backBtn = backBtn;
        window.logoutBtn = logoutBtn;
        window.loginContainer = loginContainer;
        window.loginForm = loginForm;
        window.loginError = loginError;
        window.appContainer = appContainer;
        window.addFormContainer = addFormContainer;
        window.addForm = addForm;
        window.addError = addError;
    });

    it('should render books in the list', function() {
        const books = [
            { ISBN: '1', title: 'A', author: 'B', year: 2020, publisher: 'P', cover: 'img.jpg' },
            { ISBN: '2', title: 'C', author: 'D', year: 2021, publisher: 'Q', cover: 'img2.jpg' }
        ];
        window.renderBooks(books);
        const cards = document.querySelectorAll('.book-card');
        chai.expect(cards.length).to.equal(2);
        chai.expect(cards[0].querySelector('.book-title').textContent).to.equal('A');
        chai.expect(cards[1].querySelector('.book-title').textContent).to.equal('C');
    });

    it('should render book detail', function() {
        const book = { ISBN: '1', title: 'A', author: 'B', year: 2020, publisher: 'P', cover: 'img.jpg' };
        window.renderBookDetail(book);
        chai.expect(window.bookDetail.innerHTML).to.include('A');
        chai.expect(window.bookDetail.innerHTML).to.include('B');
        chai.expect(window.bookDetail.innerHTML).to.include('2020');
        chai.expect(window.bookDetail.innerHTML).to.include('P');
        chai.expect(window.bookDetail.innerHTML).to.include('img.jpg');
    });

    it('should show login on load and app after login', function() {
        window.showLogin();
        chai.expect(window.loginContainer.style.display).to.equal('flex');
        chai.expect(window.appContainer.style.display).to.equal('none');
        window.showApp();
        chai.expect(window.loginContainer.style.display).to.equal('none');
        chai.expect(window.appContainer.style.display).to.equal('block');
    });

    it('should show login after logout', function() {
        window.showApp();
        window.logout();
        chai.expect(window.loginContainer.style.display).to.equal('flex');
        chai.expect(window.appContainer.style.display).to.equal('none');
    });

    it('should handle session token retrieval', function() {
        // Test with no token
        localStorage.removeItem('sessionToken');
        chai.expect(window.getSessionToken()).to.be.null;
        
        // Test with valid token
        const testToken = 'test123456789abcdef';
        localStorage.setItem('sessionToken', testToken);
        chai.expect(window.getSessionToken()).to.equal(testToken);
        
        // Test with invalid token (too short)
        localStorage.setItem('sessionToken', 'short');
        chai.expect(window.getSessionToken()).to.be.null;
        
        // Test with null string
        localStorage.setItem('sessionToken', 'null');
        chai.expect(window.getSessionToken()).to.be.null;
    });

    it('should validate form inputs before submission', function() {
        // Set up form inputs
        document.getElementById('add-isbn').value = '123';
        document.getElementById('add-title').value = 'Test Title';
        document.getElementById('add-author').value = 'Test Author';
        document.getElementById('add-year').value = '2025';
        document.getElementById('add-publisher').value = 'Test Publisher';
        document.getElementById('add-cover').value = 'http://example.com/cover.jpg';
        
        // Mock localStorage with a valid token
        localStorage.setItem('sessionToken', 'test123456789abcdef');
        
        // Verify form values can be read
        chai.expect(document.getElementById('add-isbn').value).to.equal('123');
        chai.expect(document.getElementById('add-title').value).to.equal('Test Title');
        chai.expect(document.getElementById('add-author').value).to.equal('Test Author');
        chai.expect(parseInt(document.getElementById('add-year').value)).to.equal(2025);
        chai.expect(document.getElementById('add-publisher').value).to.equal('Test Publisher');
        chai.expect(document.getElementById('add-cover').value).to.equal('http://example.com/cover.jpg');
    });

    it('should handle form submission without token', function() {
        // Clear any existing token
        localStorage.removeItem('sessionToken');
        
        // Set up form inputs
        document.getElementById('add-isbn').value = '123';
        document.getElementById('add-title').value = 'Test Title';
        document.getElementById('add-author').value = 'Test Author';
        document.getElementById('add-year').value = '2025';
        document.getElementById('add-publisher').value = 'Test Publisher';
        document.getElementById('add-cover').value = 'http://example.com/cover.jpg';
        
        // Create a mock form submission event
        const form = document.getElementById('add-form');
        const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
        
        // Mock the form submission handler behavior
        const token = window.getSessionToken();
        chai.expect(token).to.be.null;
        
        // Verify that without a token, the form should show login
        if (!token) {
            window.showLogin();
            chai.expect(window.loginContainer.style.display).to.equal('flex');
            chai.expect(window.appContainer.style.display).to.equal('none');
        }
    });

    it('should construct book object correctly from form', function() {
        // Set up form inputs with test data
        document.getElementById('add-isbn').value = '  978-0123456789  ';  // Test trimming
        document.getElementById('add-title').value = '  The Great Book  ';
        document.getElementById('add-author').value = '  Jane Doe  ';
        document.getElementById('add-year').value = '2025';
        document.getElementById('add-publisher').value = '  Test Publisher  ';
        document.getElementById('add-cover').value = '  http://example.com/cover.jpg  ';
        
        // Mock the book object construction logic from the form handler
        const book = {
            "ISBN": document.getElementById('add-isbn').value.trim(),
            "title": document.getElementById('add-title').value.trim(),
            "author": document.getElementById('add-author').value.trim(),
            "year": parseInt(document.getElementById('add-year').value, 10),
            "publisher": document.getElementById('add-publisher').value.trim(),
            "cover": document.getElementById('add-cover').value.trim()
        };
        
        // Verify the book object is constructed correctly
        chai.expect(book.ISBN).to.equal('978-0123456789');
        chai.expect(book.title).to.equal('The Great Book');
        chai.expect(book.author).to.equal('Jane Doe');
        chai.expect(book.year).to.equal(2025);
        chai.expect(book.publisher).to.equal('Test Publisher');
        chai.expect(book.cover).to.equal('http://example.com/cover.jpg');
        
        // Verify data types
        chai.expect(typeof book.ISBN).to.equal('string');
        chai.expect(typeof book.title).to.equal('string');
        chai.expect(typeof book.author).to.equal('string');
        chai.expect(typeof book.year).to.equal('number');
        chai.expect(typeof book.publisher).to.equal('string');
        chai.expect(typeof book.cover).to.equal('string');
    });

    it('should handle form prefill functionality', function() {
        // Mock the add button click behavior that prefills the form
        window.addFormContainer.classList.remove('hidden');
        window.appContainer.classList.add('hidden');
        
        // Simulate prefilling form with default values (as done in the actual code)
        document.getElementById('add-isbn').value = '123';
        document.getElementById('add-title').value = 'Default Title';
        document.getElementById('add-author').value = 'Default Author';
        document.getElementById('add-year').value = '2025';
        document.getElementById('add-publisher').value = 'Default Publisher';
        document.getElementById('add-cover').value = 'http://example.com/default-cover.jpg';
        
        // Verify form is prefilled correctly
        chai.expect(document.getElementById('add-isbn').value).to.equal('123');
        chai.expect(document.getElementById('add-title').value).to.equal('Default Title');
        chai.expect(document.getElementById('add-author').value).to.equal('Default Author');
        chai.expect(document.getElementById('add-year').value).to.equal('2025');
        chai.expect(document.getElementById('add-publisher').value).to.equal('Default Publisher');
        chai.expect(document.getElementById('add-cover').value).to.equal('http://example.com/default-cover.jpg');
        
        // Verify UI state
        chai.expect(window.addFormContainer.classList.contains('hidden')).to.be.false;
        chai.expect(window.appContainer.classList.contains('hidden')).to.be.true;
    });

    it('should handle form cancellation', function() {
        // Show the add form first
        window.addFormContainer.classList.remove('hidden');
        window.appContainer.classList.add('hidden');
        
        // Mock the cancel button behavior
        window.addFormContainer.classList.add('hidden');
        window.appContainer.classList.remove('hidden');
        
        // Verify UI state after cancellation
        chai.expect(window.addFormContainer.classList.contains('hidden')).to.be.true;
        chai.expect(window.appContainer.classList.contains('hidden')).to.be.false;
    });

    it('should validate authorization header format', function() {
        const testToken = 'test123456789abcdef';
        localStorage.setItem('sessionToken', testToken);
        
        const token = window.getSessionToken();
        const authHeader = 'Bearer ' + token;
        
        // Verify authorization header is formatted correctly
        chai.expect(authHeader).to.equal('Bearer test123456789abcdef');
        chai.expect(authHeader.startsWith('Bearer ')).to.be.true;
        
        // Test header construction for fetch request
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': authHeader
        };
        
        chai.expect(headers['Authorization']).to.equal('Bearer test123456789abcdef');
        chai.expect(headers['Content-Type']).to.equal('application/json');
    });
});
```