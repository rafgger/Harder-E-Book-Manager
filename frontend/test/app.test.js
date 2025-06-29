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
        window.bookList = bookList;
        window.bookDetail = bookDetail;
        window.backBtn = backBtn;
        window.logoutBtn = logoutBtn;
        window.loginContainer = loginContainer;
        window.loginForm = loginForm;
        window.loginError = loginError;
        window.appContainer = appContainer;
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

    it('should show login on load and app after login', function(done) {
        window.showLogin();
        chai.expect(window.loginContainer.classList.contains('hidden')).to.be.false;
        chai.expect(window.appContainer.classList.contains('hidden')).to.be.true;
        window.showApp();
        chai.expect(window.loginContainer.classList.contains('hidden')).to.be.true;
        chai.expect(window.appContainer.classList.contains('hidden')).to.be.false;
        done();
    });

    it('should show login after logout', function(done) {
        window.showApp();
        window.logout();
        chai.expect(window.loginContainer.classList.contains('hidden')).to.be.false;
        chai.expect(window.appContainer.classList.contains('hidden')).to.be.true;
        done();
    });
});
```