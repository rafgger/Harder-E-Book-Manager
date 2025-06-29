### Role:
You're a web application developer building a sleek, minimalist interface for managing e-books.

### Project Goal:
Adjust the already present responsive web application to have the following features.

- Simple authentication/login screen (e.g., password stored in a config file)  
- Page with a form for adding a new book (the form must have validation)  
- Import button – Triggers the import of books into the database from a `books.json` file  
  (the file will contain structured JSON data of several books and will be statically placed in the app directory)

### Technical Requirements:

Backend:

- FastAPI, adjust the already present backend.
- Run appropriate tests.

Frontend:

- Adjust SASS for styling; `.scss` files should be separated from public CSS files (e.g., in a `src/` directory)  
- Use plain JavaScript (no framework), utilizing modern ES6+ syntax 
- Run appropriate tests. 


Documentation:

- `README.md` with a short installation guide and login credentials configuration instructions


//
In PgAdmin I have the Database Books, and the table books with:

ISBN,Book-Title,Book-Author,Year-Of-Publication,Publisher,Image-URL-M
0195153448,Classical Mythology,Mark P. O. Morford,2002,Oxford University Press,http://images.amazon.com/images/P/0195153448.01.MZZZZZZZ.jpg
0002005018,Clara Callan,Richard Bruce Wright,2001,HarperFlamingo Canada,http://images.amazon.com/images/P/0002005018.01.MZZZZZZZ.jpg
0060973129,Decision in Normandy,Carlo D'Este,1991,HarperPerennial,http://images.amazon.com/images/P/0060973129.01.MZZZZZZZ.jpg


//
If you are unsure about anything ask me instead of making assumptions.

//
run tests to confirm the functionality of the code
the frontend test using Mocha
finally create a README file with instructions on how to run the application and a description of the project.