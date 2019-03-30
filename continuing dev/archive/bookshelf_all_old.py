import pickle
import functools
import time
import os

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

    def __str__(self):
        return self.name

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

    def print_bookshelf_summary(self):
        """Print the summary information for the the bookshelf."""
        
        print(f'Books: {self.books_count}\nReviews: {self.reviews_count}')


    def print_books_titles(self, sort_val=None):
        """Print the book titles for all books in the bookshelf, sorted by the sort method (if provided)."""
        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            books_sorted = self.books

        if books_sorted:
            [print(book.get_title()) for book in books_sorted]
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
            
            
@functools.total_ordering
class Book():
    '''An entity that represents a book and associated data.
    
    Class Attributes:
    book_count
    book_statuses = 1: 'Want to Read', 
                    2: 'Reviewed', 
                    3: 'Read_No_Review', 
                    4: 'Don't want to read'
    
    Instance Attributes:
'Title', 'Author', 'ISBN', 'Average Rating', 'Publisher', 'Binding', 'Year Published', 'Original Publication Year', 
'Date Read', 'Date Added', 'Bookshelves', 'My Review', 'My Rating', 

    title
    author
    ISBN
    url (to Amazon/goodreads/etc.)
    recommended_by (who recommended the book)
    other (text field for whatever additional notes the user would like to record about the book, 
        not including review information)
    book_status - (Want to Read, Reviewed, Read_No_Review, Don't want to read)
    bookshelves (list of bookshelves the book has been added to)
    reviews
    
    Methods:
    get_title
    get_book_info
    print_reviews
    add_review
    '''
    book_count = 0

    book_statuses = {
        1: "Want to Read",
        2: "Reviewed",
        3: "Read_No_Review",
        4: "Don't want to read"
    }

    def __init__(self,
                 title=None,
                 author=None,
                 ISBN=None,
                 url=None,
                 recommended_by=None,
                 other=None,
                 book_status=1,
                 bookshelves=[],
                 review=None):
        if title == None:
            self.title = input("Enter a title: ")
            self.author = input("Enter an author: ")
            self.ISBN = input("Enter an ISBN (if you have one): ")
            self.url = input(
                "Enter a url for Amazon/Goodreads/etc.(if you have one): ")
            self.recommended_by = input(
                "Enter details for who recommended the book (if you have one): "
            )
            self.other = input(
                "Enter any additional notes the you would like to record about the book, \
                \not including review information: ")
            self.book_status = int(
                input('Enter any number for the status of the book: \n\
                1 = "Want to Read"\n\
                2 = "Reviewed"\n\
                3 = "Read_No_Review"\n\
                4 = "Don\'t want to read"\n\
                Status: '))
            self.bookshelves = bookshelves
        else:
            self.title = title
            self.author = author
            self.ISBN = ISBN
            self.url = url
            self.recommended_by = recommended_by
            self.other = other
            self.book_status = Book.book_statuses[book_status]
            self.bookshelves = bookshelves
        if review == None:
            self.reviews = []
            if book_status == 2:
                if int(
                        input(
                            'Would you like to review this book now? (1 = Yes, 0 = No)\n'
                        )) == 1:
                    self.add_review()
                else:
                    self.book_status = Book.book_statuses[3]
                    print(f"Changing book status to: {self.book_status}")
        else:
            self.add_review(review)
        Book.book_count += 1

    def __lt__(self, other):
        try:
            return self.title < other.title
        except:
            return False

    def __eq__(self, other):
        try:
            return self.title == other.title
        except:
            return False

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title

    def get_book_info(self):
        
        return (f"{self}\n\
        Author: {self.author}\n\
        ISBN: {self.ISBN}\n\
        url: {self.url}\n\
        Recommended by: {self.recommended_by}\n\
        Other: {self.other}\n\
        Status: {self.book_status}\n\
        Bookshelves: {', '.join(str(bookshelf) for bookshelf in self.bookshelves)}\n\
        Reviews: {len(self.reviews)}")

    def add_to_bookshelf(self, bookshelf=None):
        '''method to ad a book to a bookshelf and prompt user if no bookshelf provided. Possible states: 
            1. bookshelf provided
            2. No bookshelf provided - user prompted to pick a bookshelf or add a bookshelf'''
        if bookshelf == None:
            bookshelves = Bookshelf.bookshelves
            counter = 0
            words = f"Choose a bookshelf to add {self} to:\n\
            Enter 'a' to add a new bookshelf"

            for bookshelf in bookshelves:
                words += f"\n\tEnter '{counter}' to add to {bookshelf}"
                counter += 1
            words += f"\nBookshelf choice: "
            while True:
                chosen_bookshelf = input(words).lower()
                if chosen_bookshelf == 'a' or int(chosen_bookshelf) in range(
                        0, counter):
                    if chosen_bookshelf == 'a':
                        bookshelf = Bookshelf()
                    else:
                        bookshelf = bookshelves[int(chosen_bookshelf)]
                    break
                else:
                    print("\nPlease try again")

            bookshelf.add_book(self)
            print(f"{self} added to {bookshelf}")

    def add_review(self, review=None):
        if review == None:
            self.reviews.append(Review(self))
        else:
            self.reviews.append(review)
        self.book_status = Book.book_statuses[2]
        for bookshelf in self.bookshelves:
            bookshelf.reviews_count += 1

        print(f"\nReview added to {self.title}:\n\
        {self.reviews[-1]}")

    def print_reviews(self, sort_val=None):
        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            reviews_sorted = self.reviews

        if reviews_sorted:
            for review in reviews_sorted:
                print(review, '\n')
        else:
            print(f"{self.title}: No reviews yet!")


class Review():
    '''An entity that represents a book review and associated data.
    
    Class Attributes:
    rating (1-5)
    review_count
    formats = 1: "Physical Book",
              2: "ebook",
              3: "Audiobook",
              4: "Other"

    Instance Attributes:
    title (title of the book being reviewed)
    rating (1-5)
    start_date
    end_date
    big_idea
    other_notes_takeaways
    format_consumed
        
    Methods:
    get_title
    '''
    formats = {1: "Physical Book", 2: "ebook", 3: "Audiobook", 4: "Other"}

    review_count = 0
    rating = range(1, 5)

    def __init__(self,
                 book=None,
                 rating=None,
                 start_date=None,
                 end_date=None,
                 big_idea=None,
                 other_notes_takeaways=None,
                 format_consumed=4):
        if book == None:
            raise Exception("Need a book!")
        elif rating == None:
            self.title = book.title
            self.rating = self.verify_rating(rating)  #add/verify the rating
            self.start_date = input("Enter a start_date: ")
            self.end_date = input("Enter a end_date: ")
            self.big_idea = input("Enter the big_idea: ")
            self.other_notes_takeaways = input("Enter other_notes_takeaways: ")
            self.format_consumed = int(
                input('Enter any number for the format of the book: \n\
                1 = "Physical Book"\n\
                2 = "ebook"\n\
                3 = "Audiobook"\n\
                4 = "Other"\n\
                Format: '))
        else:
            self.title = book.title
            self.rating = self.verify_rating(rating)  #add/verify the rating
            self.start_date = start_date
            self.end_date = end_date
            self.big_idea = big_idea
            self.other_notes_takeaways = other_notes_takeaways
            self.format_consumed = Review.formats[format_consumed]
        book.add_review(self)
        Review.review_count += 1

    def verify_rating(self, rating=None):
        '''method to verify if rating is in 1-5.  Possible states: 
            1. no rating provided
            2. rating provided is not in range
            3. rating is ok'''
        if rating == None:
            rating = input("Enter a rating (1-5 as an integer): ")
        while rating not in range(1, 6) or type(rating) is not int:
            print(rating)
            try:
                rating = int(rating)
                if rating not in range(1, 6):
                    raise
            except:
                rating = input(
                    "Invalid entry - please enter a rating (1-5 as an integer): "
                )
        return rating

    def get_title(self):
        return self.title

    def __repr__(self):
        return (f"{self.title}\n\
        rating: {self.rating}\n\
        start_date: {self.start_date}\n\
        end_date: {self.end_date}\n\
        Big Idea: {self.big_idea}\n\
        Other notes & takeaways: {self.other_notes_takeaways}\n\
        format_consumed: {self.format_consumed}")
    
    def __str__(self):
        return (f"{self.title}\n\
        rating: {self.rating}\n\
        start_date: {self.start_date}\n\
        end_date: {self.end_date}\n\
        Big Idea: {self.big_idea}\n\
        Other notes & takeaways: {self.other_notes_takeaways}\n\
        format_consumed: {self.format_consumed}")


class Bookshelf_manager:
    """This class creates new/loads instances of the bookshelf, book, and review objects 
    and allows for user interaction"""

    menu = {
        'L': '(L)ist my books',
        'G': '(G)et the info about a book',
        'A': '(A)dd a book',
        'R': '(R)eview a book',
        'C': 'save and (C)lose',
        'S': '(S)ettings'
    }

    def __init__(self):
        #Generate new interaction instance and allow users to interact with their bookshelves until the user selects save and close = "C"
        self.intro()  # introduce the program
        self.load_or_add_bookshelf()  # load or add a bookshelf

        while True:

            #Prompt to save and close
            menu = Bookshelf_manager.menu
            menu_option = ""
            while True:
                print('\nWhat would you like to do next?\n\nEnter: ')
                for item in menu:
                    print(f'\t({item}) to {menu[item]}')
                menu_option = input('\n').upper()
                if menu_option in menu:
                    break
                else:
                    os.system('clear')
                    print(f"Your entry '{menu_option}' is not recognized")
            if menu_option == "L":
                self.list_books()
            elif menu_option == "G":
                self.get_book_info()
            elif menu_option == "C":
                self.bookshelf.save_bookshelf()
                print(f'{self.bookshelf} saved.  Have a wonderful day!\n')
                break

     

    def intro(self):
        print()
        print(
            "Let's manage our bookshelf. You will be prompted to load an existing bookshelf or set up a new one."
        )
        print("Then you will have the opportunity to add books and reviews.")
        print(
            "You can see the books on your bookshelf, and select them to see their details."
        )
        print("First let's set up your bookshelf.")
        time.sleep(0)
        print()

    def load_or_add_bookshelf(self):
        load_or_add = ""
        while True:
            load_or_add = input(
                'Would you like to load an existing bookshelf, or add a new one? Enter (L) to load an existing bookshelf or (A) to add a new bookshelf\n'
            ).upper()
            if load_or_add == "L" or load_or_add == "A":
                break
        if load_or_add == "A":
            os.system('clear')
            bookshelf_name = input(
                "What would you like to call your new bookshelf?\n")
            self.bookshelf = Bookshelf(bookshelf_name)
            print(f'\n{self.bookshelf} created!\n')
        else:
            os.system('clear')
            while True:
              try:
                  bookshelf_file = input(
                      "What is the file name (with path) of the bookshelf you would like to load?\n"
                  )
                  self.bookshelf = Bookshelf.load_bookshelf(bookshelf_file)
                  break
              except:
                  print(f"Your entry '{bookshelf_file}' is not recognized")
            self.bookshelf.reset_bookshelf()
            print(f'\n"{self.bookshelf}" bookshelf loaded:')
            self.bookshelf.print_bookshelf_summary()
            print()

    def list_books(self):
        os.system('clear')
        self.bookshelf.print_ascii_books()
    
    def get_book_info(self):
        os.system('clear')
        self.bookshelf.print_ascii_books()
        prompt = int(input("Which book would you like? (Enter the number below the book on the bookshelf)\n"))
        print('\n' + self.bookshelf.books[prompt - 1].get_book_info() +
              '\n\nReview: ')
        self.bookshelf.books[prompt - 1].print_reviews()


# Main Bookshelf Program - Conor Healy
# The main program prompts the user to load a bookshelf or create a new one.

os.system('clear')
Bookshelf_manager()


