```javascript
describe('Book UI', function() {
    beforeEach(function() {
        // Setup DOM for tests
        document.body.innerHTML = `
            <div id="book-list"></div>
            <div id="book-detail"></div>
            <button id="back-btn"></button>
        `;
        window.bookList = document.getElementById('book-list');
        window.bookDetail = document.getElementById('book-detail');
        window.backBtn = document.getElementById('back-btn');
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
});
```