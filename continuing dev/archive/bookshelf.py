import pickle


class Bookshelf():
    '''An entity that represents a place for all my books.
    
    Attributes:
    Bookshelf.bookshelf_count (how many bookshelves are there?)
    books (list)
    name
    books_count
    reviews_count
    
    Methods
    get_books
    print_books_titles
    print_books_info
    print_reviews
    print_ascii_books
    add_book
    save_bookshelf
    load_bookshelf
    '''
    bookshelf_count = 0
    bookshelves = []

    def __init__(self, name="bookshelf"):
        self.name = name
        self.books = []
        Bookshelf.bookshelves.append(self)
        Bookshelf.bookshelf_count += 1
        self.books_count = 0
        self.reviews_count = 0

    def __repr__(self):
        return self.name

    @classmethod
    def load_bookshelf(cls, file):
        return pickle.load(open(file, "rb"))

    def save_bookshelf(self):
        pickle.dump(self, open(f"{self.name}.bkshlf", "wb"))

    def get_books(self):
        return (self.books)

    def get_bookshelves():
        return (Bookshelf.bookshelves)

    def reset_bookshelf(self):
        Bookshelf.bookshelf_count = 0
        for bookshelf in Bookshelf.bookshelves:
            Bookshelf.bookshelf_count += 1

        self.books_count = 0
        self.reviews_count = 0
        for book in self.books:
            self.books_count += 1
            book.reviews_count = 0
            for review in book.reviews:
                book.reviews_count += 1
                self.reviews_count += 1

    def add_book(self, book=None):
        """Add a book to the bookshelf.  If a book is not provided, user will be prompted to add the book manually."""
        if book == None:
            book = Book()
        self.books.append(book)
        book.bookshelves.append(self)
        self.books_count += 1

        print(f"{book.get_book_info()} \nadded to {self.name}")

    def print_books_titles(self, sort_val=None):
        """Print the book titles for all books in the bookshelf, sorted by the sort method (if provided)."""
        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            books_sorted = self.books

        if books_sorted:
            [print(book.get_title(), '\n') for book in books_sorted]
        else:
            print("No books to print: Bookshelf is empty!  Find some books!")

    def print_books_info(self, sort_val=None):
        """Print the full book information for all books in the bookshelf (not including reviews), 
        sorted by the sort method (if provided)."""
        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            books_sorted = self.books

        if books_sorted:
            [print(book.get_book_info(), '\n') for book in books_sorted]
        else:
            print(
                "No books to print info: Bookshelf is empty!  Find some books!"
            )

    def print_reviews(self, sort_val=None):
        """Print the full review information for all books in the bookshelf, 
        sorted by the sort method (if provided)."""

        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            books_sorted = self.books

        if books_sorted:
            for book in books_sorted:
                book.print_reviews()
                print()
        else:
            print(
                "No books to print reviews for: Bookshelf is empty!  Find some books!"
            )

    def print_ascii_books(self,
                          sort_val=None,
                          letters_per_ascii_book=20,
                          books_per_row=14):
        '''method to print the bookshelf in ascii art format, sorted by the value provided. 
        The height of each shelf/book can be controlled by the letters_per_ascii_book, and 
        the width can be controlled by the books_per_row.
        
        Format inspired by https://codegolf.stackexchange.com/questions/111833/ascii-bookshelves'''
        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            books_sorted = self.books

        books = [book.get_title() for book in self.books]
        num_books = len(books)
        books_count = len(books)
        k = '|' + '-----' * books_per_row + '|'
        if books_count:
            while books_count:
                books_in_row = books_count % books_per_row or books_per_row
                print(k + '\n' +
                      ('|' + '     ' * (books_per_row - books_in_row) +
                       '/___/' * books_in_row + '|'))
                num_letters = letters_per_ascii_book
                while num_letters:
                    book_string = ''
                    col_string = ''
                    for i in range(0, books_in_row):
                        temp_book = books[num_books - books_count + i]
                        if letters_per_ascii_book - num_letters < len(
                                temp_book):
                            book_string_letter = temp_book[
                                letters_per_ascii_book - num_letters]
                        else:
                            book_string_letter = ' '
                        book_string += f'| {book_string_letter} |'
                        col_string += f' {num_books - books_count + i + 1:-2}  '
                    print('|' + '     ' * (books_per_row - books_in_row) +
                          book_string + '|')
                    num_letters -= 1
                print('|' + '     ' * (books_per_row - books_in_row) +
                      "^---^" * books_in_row + '|' + '\n' + k)
                print('|' + '     ' * (books_per_row - books_in_row) +
                      col_string + '|')
                books_count -= books_in_row
        else:
            print(k + '\n' + ('|' + '     ' * books_per_row + '|' + '\n') *
                  (letters_per_ascii_book + 2) + k)
            print("No books to print: Bookshelf is empty!  Find some books!")