"""A program to manage my bookshelves, books, and reviews."""

import pickle
import functools
import time
import os
import numpy as np
import pandas as pd
from datetime import date


class Bookshelf():
    """An entity that represents a place for all my books.

    Attributes:
        Bookshelf.bookshelf_count (how many bookshelves are there?)
        Bookshelf.bookshelves (all my bookshelves)
        name
        books (list)
        filtered_books (list with the current filters applied)
        filter_type (label of the most recent filter)
        sort_val (description of the most recent sort)
        books_count
        reviews_count
        date_added

    Methods:
        save_bookshelf
        load_bookshelf
        get_books
        get_bookshelves
        reset_bookshelf
        add_book
        filter_books (generic filter method)
        filter_books_status (method to filter based on book status)
        sort_books
        print_bookshelf_summary
        print_books_titles
        print_books_info
        print_reviews
        print_ascii_books
        multi_input
        load_good_book_row
        load_goodreads_csv

    """
    bookshelf_count = 0
    bookshelves = []

    def __init__(self, name="bookshelf"):
        self.name = name
        self.books = []
        Bookshelf.bookshelves.append(self)
        Bookshelf.bookshelf_count += 1
        self.books_count = 0
        self.reviews_count = 0
        self.filtered_books = self.books.copy()
        self.filter_type = 'All Books'
        self.sort_val = 'None'
        self.date_added = date.today()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    @classmethod
    def load_bookshelf(cls, file):
        """Method to load the bookshelf. Args:
            file = the file you want to open (usually named <file>.bkshlf)
        """
        return pickle.load(open(file, "rb"))

    def save_bookshelf(self):
        """Method to save the bookshelf."""
        pickle.dump(self, open(f"{self.name}.bkshlf", "wb"))

    def get_books(self):
        """Method that returns the list of filtered books."""
        return self.filtered_books

    def get_bookshelves():
        """Method that returns the list of all bookshelves."""
        return Bookshelf.bookshelves

    def reset_bookshelf(self):
        """Method to reset the bookshelf. All filters and sort are removed by resetting the
        filtered_books list to match the original books list.
        All counters are reset to 0 then recalculated.
        """
        Bookshelf.bookshelf_count = len(Bookshelf.bookshelves)
        self.filtered_books = self.books.copy()
        self.books_count = 0
        self.reviews_count = 0
        self.filter_type = 'All Books'
        self.sort_val = 'None'
        for book in self.filtered_books:
            self.books_count += 1
            book.reviews_count = len(book.reviews)
            self.reviews_count += len(book.reviews)

    def add_book(self, book=None):
        """Add a book to the bookshelf.
        If a book is not provided, user will be prompted to add the book manually.
        """
        if book is None:
            book = Book(bookshelves=[self])
        self.books.append(book)
        self.filtered_books.append(book)
        self.books_count += 1
        print(f"\n{book.get_book_info()}\n\n{book} added to {self.name}")

    def filter_books(self):
        """Method to filter the filtered_books list for the first 2 books.
        This is a generic template that could be enhanced in future releases
        """
        self.filtered_books = self.filtered_books[0:2]
        self.filter_type = '1st 2 books'

    def filter_books_status(self, status=None):
        """Method to filter the filtered_books list based on the status provided."""
        if status is not None:
            temp_books = []
            for book in self.filtered_books:
                if book.book_status == status:
                    temp_books.append(book)
            self.filtered_books = temp_books
            self.filter_type = status

    def sort_books(self, sort_val='Title', reverse_arg=False):
        """Method to sort the filtered_books list based on the status provided.
        Args:
            sort_val (the status by which to sort)
            revers_arg (Boolean flag for whether to reverse the sort)
        """
        for book in self.filtered_books:
            book.sort_val = book.sort_book(sort_val)
        self.filtered_books = sorted(self.filtered_books, reverse=reverse_arg)
        sort_dir = '(D)' if reverse_arg else '(A)'
        self.sort_val = sort_val + sort_dir

    def print_bookshelf_summary(self):
        """Print the summary information for the the bookshelf."""
        print(f'\nBookshelf: {self}\nFilter: {self.filter_type}\nSort: {self.sort_val}')
        print(f'Books: {self.books_count}\nReviews: {self.reviews_count}')

    def print_books_titles(self):
        """Print the book titles for all books in the bookshelf,
        sorted by the sort method (if provided).
        """
        if self.filtered_books:
            for book in self.filtered_books:
                print(book.get_title())
        else:
            print("No books to print: Bookshelf is empty!  Find some books!")

    def print_books_info(self):
        """Print the full book information for all books in the bookshelf (not including reviews),
        sorted by the sort method (if provided).
        """
        if self.filtered_books:
            for book in self.filtered_books:
                print(book.get_book_info(), '\n')
        else:
            print(
                "No books to print info: Bookshelf is empty!  Find some books!"
            )

    def print_reviews(self):
        """Print the full review information for all books in the bookshelf,
        sorted by the sort method (if provided).
        """
        if self.filtered_books:
            for book in self.filtered_books:
                book.print_reviews()
                print()
        else:
            print("No books to print reviews for: Bookshelf is empty!  Find some books!")

    def print_ascii_books(bookshelf,
                          letters_per_ascii_book=20,
                          ascii_books_per_row=10):
        '''method to print the bookshelf in ascii art format, sorted by the value provided.
        The height of each shelf/book can be controlled by the letters_per_ascii_book, and
        the width can be controlled by the ascii_books_per_row.

        Format inspired by https://codegolf.stackexchange.com/questions/111833/ascii-bookshelves'''

        print(f'\n Bookshelf: {bookshelf}\t\tFilter: {bookshelf.filter_type}\tSort: {bookshelf.sort_val}')
        books = [book.get_title() for book in bookshelf.filtered_books]
        num_books = len(books)
        books_count = len(books)
        k = '|' + '-------' * ascii_books_per_row + '|'
        if books_count:
            while books_count:
                books_in_row = books_count % ascii_books_per_row or ascii_books_per_row
                print(k + '\n' +
                      ('|' + '       ' * (ascii_books_per_row - books_in_row) +
                       '/_____/' * books_in_row + '|'))
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
                        book_string += f'|  {book_string_letter}  |'
                        book_num = num_books - books_count + i + 1
                        col_string += f'  {book_num:-3}  '
                    print('|' + '       ' * (ascii_books_per_row - books_in_row) +
                          book_string + '|')
                    num_letters -= 1
                print('|' + '       ' * (ascii_books_per_row - books_in_row) +
                      "^-----^" * books_in_row + '|' + '\n' + k)
                print('|' + '       ' * (ascii_books_per_row - books_in_row) +
                      col_string + '|')
                books_count -= books_in_row
        else:
            print(k + '\n' + ('|' + '       ' * ascii_books_per_row + '|' + '\n') *
                  (letters_per_ascii_book + 4) + k)
            print("No books to print: Bookshelf is empty!  Find some books!")

    def multi_input(instructions='Enter the string and then press ENTER twice to end your input:'):
        """Method to allow users to enter multiple lines of input using the input() function.
        Recurring input is ended when the user inputs a null value (by pressing ENTER twice).

        Args:
            instructions (provided to the user to explain how the input will work)
        """
        output = ''
        print(instructions)
        while True:
            s = input()
            if s:
                output = output + '\n' + s
            else:
                break
        return output

    def load_goodreads_csv(self, goodreads_csv_file='no csv'):
        error_msg = ''
        while True:
            try:
                csv_data = pd.read_csv(goodreads_csv_file)
                csv_data = csv_data.assign(isbn_clean=[x[2:-1] for x in csv_data['ISBN']])
                csv_data = csv_data.assign(isbn13_clean=[x[2:-1] for x in csv_data['ISBN13']])
                csv_data = csv_data.join(csv_data['My Review'].str.extract(r'(?P<The_Big_Idea>(?<=The Big Idea:).*?(?=Highlights:))').fillna(''))
                csv_data = csv_data.join(csv_data['My Review'].str.extract(r'(?P<Highlights>(?<=Highlights:).*?(?=Actionable Items:))').fillna(''))
                csv_data = csv_data.join(csv_data['My Review'].str.extract(r'(?P<Actionable_Items>(?<=Actionable Items:).*?(?=Other Notes & Takeaways:))').fillna(''))
                csv_data = csv_data.join(csv_data['My Review'].str.extract(r'(?P<Other_Notes_and_Takeaways>(?<=Other Notes & Takeaways:).*?(?=Format Consumed:))').fillna(''))
                csv_data = csv_data.join(csv_data['My Review'].str.extract(r'(?P<Format_Consumed>(?<=Format Consumed:<br\/>).*?(?=$))').fillna(''))
                break
            except:
                print(f'{error_msg}Please enter the file path for the Goodreads csv file you want to load. ("path/goodreads_library_export.csv")\nCurrent working directory is: {os.getcwd()}')
                goodreads_csv_file = input("Enter the file path: ")
                error_msg = f'Invalid entry - {goodreads_csv_file} - ' #by placing this here, this message will only be added on loops 2+
        csv_data.apply(lambda x: Bookshelf.load_good_book_row(good_book_row = x, bookshelf_list = self.bookshelves), axis=1)

    def load_good_book_row(good_book_row, bookshelf_list):
        book_review = None    
        if pd.notnull(good_book_row['My Review']):
            try: 
                review_format_consumed = Review.formats_rev[good_book_row['Format_Consumed']] if good_book_row['Format_Consumed'] != '' else 4
            except:
                review_format_consumed = 4
            book_review = Review(book=good_book_row['Title'],
                                 rating=good_book_row['My Rating'],
                                 start_date=good_book_row['Date Read'],
                                 end_date=good_book_row['Date Read'],
                                 big_idea=good_book_row['The_Big_Idea'] if good_book_row['Other_Notes_and_Takeaways'] != '' else '',
                                 highlights=good_book_row['Highlights'] if good_book_row['Other_Notes_and_Takeaways'] != '' else '',
                                 actionable_items=good_book_row['Actionable_Items'] if good_book_row['Other_Notes_and_Takeaways'] != '' else '',
                                 other_notes_takeaways=good_book_row['Other_Notes_and_Takeaways'] if good_book_row['Other_Notes_and_Takeaways'] != '' else good_book_row['My Review'],
                                 format_consumed= review_format_consumed)
        Book(title=good_book_row['Title'],
                    author=good_book_row['Author'],
                    isbn=good_book_row['isbn_clean'],
                    book_status=1 if good_book_row['Exclusive Shelf'] == 'to-read' else 3,
                    bookshelves = bookshelf_list,
                    review = book_review
                   )
        print(f"\n{good_book_row['Title']} added to {bookshelf_list}")


@functools.total_ordering
class Book():
    """An entity that represents a book and associated data.

    Attributes:
        Book.book_count
        Book.book_statuses = 1: 'Want to Read',
                             2: 'Reviewed',
                             3: 'Read_No_Review',
                             4: 'Don't want to read'
        title (of the book)
        author
        isbn
        url (to Amazon/goodreads/etc.)
        recommended_by (who recommended the book)
        other (text field for whatever additional notes the user would like to
            record about the book, not including review information)
        book_status - (possible statuses of the book: "Want to Read", etc.)
        bookshelves (list of bookshelves the book has been added to)
        reviews (list of reviews added to the book)

    Methods:
        get_title
        get_book_info
        sort_book
        add_to_bookshelf
        input_book_status
        add_review
        print_reviews
    """
    book_count = 0

    # dictionary of statuses directly applied to the books
    book_statuses = {
        1: "Want to Read",
        2: "Reviewed",
        3: "Read, but not reviewed",
        4: "Don't want to read"
    }

    # dictionary of statuses used to prompt users to describe the status of a book upon init
    add_book_statuses = {
        1: "Want to Read",
        2: "Want to Review",
        3: "Read, but don\'t want to review now",
        4: "Don't want to read"
    }

    def __init__(self,
                 title=None,
                 author=None,
                 isbn=None,
                 url=None,
                 recommended_by=None,
                 other='',
                 book_status=1,
                 bookshelves=[],
                 review=None):
        if title is None:
            print('Please enter the information for your book.')
            self.title = input("Enter a title: ")
            self.author = input("Enter the author: ")
            self.isbn = input("Enter the ISBN (if you have one): ")
            self.url = input(
                "Enter a url for Amazon/Goodreads/etc.(if you have one): ")
            self.recommended_by = input(
                "Enter details for who recommended the book (if you have one): "
            )
            print("Enter any additional notes the you would like to record about the book,")
            print("not including review information,")
            self.other = Bookshelf.multi_input(instructions='then press ENTER twice to end your input:')
            self.book_status = self.input_book_status()
            self.bookshelves = bookshelves
            self.sort_val = self.title
            self.date_added = date.today()
        else:
            self.title = title
            self.author = author
            self.isbn = isbn
            self.url = url
            self.recommended_by = recommended_by
            self.other = other
            self.book_status = Book.book_statuses[book_status]
            self.bookshelves = bookshelves
            self.sort_val = self.title
            self.date_added = date.today()
        self.reviews = []
        if review is None:
            if self.book_status == 'Reviewed':
                print('\nWould you like to review this book now? (1 = Yes, Anything else = No)')
                try:
                    if int(input('Entry: ')) == 1:
                        self.add_review()
                    else:
                        raise
                except:
                    self.book_status = Book.book_statuses[3]
                    print(f"Changing book status to: {self.book_status}")
        else:
            self.add_review(review)
        for bookshelf in self.bookshelves:
            bookshelf.add_book(self)
        Book.book_count += 1

    def __lt__(self, other):
        try:
            return self.sort_val < other.sort_val
        except:
            return False

    def __eq__(self, other):
        try:
            return self.sort_val == other.sort_val
        except:
            return False

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.__repr__()

    def get_title(self):
        """Method that returns the title of the book."""
        return self.title

    def get_book_info(self):
        """Method that returns a string providing key information about the book."""
        other = self.other.replace('\n', '\n\t\t')
        book_info = f"{self}\n"
        book_info += f"\tAuthor: {self.author}\n"
        book_info += f"\tISBN: {self.isbn}\n"
        book_info += f"\turl: {self.url}\n"
        book_info += f"\tRecommended by: {self.recommended_by}\n"
        book_info += f"\tOther: {other}\n"
        book_info += f"\tStatus: {self.book_status}\n"
        book_info += f"\tBookshelves: {', '.join(str(bookshelf) for bookshelf in self.bookshelves)}\n"
        book_info += f"\tDate book added to my library: {self.date_added}\n"
        book_info += f"\tReviews: {len(self.reviews)}"
        return book_info

    def sort_book(self, sort_val='Title'):
        """method to return a value by which a book can be sorted.
        If no sort_val is provided, will return the book title.
        """
        if sort_val == 'Author':
            return self.author.upper()
        elif sort_val == 'ISBN':
            return self.isbn.upper()
        elif sort_val == 'url':
            return self.url.upper()
        elif sort_val == 'Recommended by':
            return self.recommended_by.upper()
        elif sort_val == 'Other':
            return self.other.upper()
        elif sort_val == 'Status':
            return self.book_status.upper()
        elif sort_val == 'Date book was added to library':
            return self.date_added
        elif sort_val == '# of Reviews':
            return len(self.reviews)
        elif sort_val == 'Latest Review Rating':
            if self.reviews:
                return self.reviews[-1].rating
            return 0
        # When sorting by Last Review Date, it's not clear what the ideal sort state is
        # for books without reviews.  Currently returing the book's date_added.
        elif sort_val == 'Latest Review Date':
            if self.reviews:
                return self.reviews[-1].date_added
            return self.date_added
        return self.title.upper()


    def add_to_bookshelf(self, bookshelf=None):
        """method to add a book to a bookshelf and prompt user if no bookshelf provided.
        Possible states:
            1. bookshelf provided
            2. No bookshelf provided - user prompted to pick a bookshelf or add a bookshelf
        """
        if bookshelf is None:
            bookshelves = Bookshelf.bookshelves
            counter = 0
            words = f"Choose a bookshelf to add {self} to:\n\
            Enter 'a' to add a new bookshelf"

            for existing_bookshelf in bookshelves:
                words += f"\n\tEnter '{counter}' to add to {existing_bookshelf}"
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

    def input_book_status(self):
        """method to gather book_status from users, until the user inputs a valid book_status.
        Possible states:
            1. no book_status provided
            2. book_status provided is not in range
            3. book_status is ok
        """
        while True:
            print('Enter a number corresponding to the book_status of the book:')
            for item in Book.book_statuses:
                print(f'\t{item} = "{Book.add_book_statuses[item]}"')
            book_status_option = input('\tEntry: ')

            try:
                book_status_option = int(book_status_option)
                if book_status_option in Book.book_statuses.keys():
                    break
                else:
                    raise
            except:
                print(f"Your entry '{book_status_option}' is not recognized\n")
        return Book.book_statuses[book_status_option]

    def add_review(self, review=None):
        """Method to add a review to the book."""
        print(f'Reviewing {self}:')
        if review is None:
            self.reviews.append(Review(self))
        else:
            self.reviews.append(review)
        self.book_status = Book.book_statuses[2]
        for bookshelf in self.bookshelves:
            bookshelf.reviews_count += 1

        print(f"\nReview added to {self.title}:\n\
        {self.reviews[-1]}")

    def print_reviews(self):
        """Method to print the reviews of the book."""
        if self.reviews:
            for review in self.reviews:
                print(review, '\n')
        else:
            print(f"{self.title}: No reviews yet!")


class Review():
    """An entity that represents a book review and associated data.

    Attributes:
        Review.formats = 1: "Physical Book",
                         2: "eBook",
                         3: "Audiobook",
                         4: "Other"
        Review.formats_rev (reverse of formats dictionary for easy lookup by format name)
        Review.rating_range (1-5)
        Review.review_count
        book (the book being reviewed)
        rating_range (1-5)
        start_date
        end_date
        big_idea
        highlights
        actionable_items
        other_notes_takeaways
        format_consumed

    Methods:
        input_format
        verify_rating
        get_title
    """
    formats = {1: "Physical Book", 2: "eBook", 3: "Audiobook", 4: "Other"}
    formats_rev = {value: key for key, value in formats.items()}
    rating_range = range(1, 6)
    review_count = 0

    def __init__(self,
                 book=None,
                 rating=None,
                 start_date=None,
                 end_date=None,
                 big_idea=None,
                 highlights=None,
                 actionable_items=None,
                 other_notes_takeaways=None,
                 format_consumed=4):
        if book is None:
            raise Exception("Need a book!")
        elif rating is None:
            print('Please enter the information for your review.')
            self.title = book.title
            self.rating = self.verify_rating(rating)  #add/verify the rating
            self.start_date = input("Enter a start_date: ")
            self.end_date = input("Enter a end_date: ")
            self.big_idea = Bookshelf.multi_input(instructions='Enter the big_idea, then press ENTER twice to end your input:')
            self.highlights = Bookshelf.multi_input(instructions='Enter the highlights, then press ENTER twice to end your input:')
            self.actionable_items = Bookshelf.multi_input(instructions='Enter the actionable_items, then press ENTER twice to end your input:')
            self.other_notes_takeaways = Bookshelf.multi_input(instructions='Enter other_notes_takeaways, then press ENTER twice to end your input:')
            self.format_consumed = self.input_format()
            self.date_added = date.today()
        else:
            self.title = book.title
            self.rating = self.verify_rating(rating)  #add/verify the rating
            self.start_date = start_date
            self.end_date = end_date
            self.big_idea = big_idea
            self.highlights = highlights
            self.actionable_items = actionable_items
            self.other_notes_takeaways = other_notes_takeaways
            self.format_consumed = Review.formats[format_consumed]
            self.date_added = date.today()
        Review.review_count += 1

    def input_format(self):
        """method to gather format from users, until the user inputs a valid format.
        Possible states:
            1. no format provided
            2. format provided is not in range
            3. format is ok
        Returns a valid format
        """

        while True:
            print('Enter a number corresponding to the format of the book:')
            for item in Review.formats:
                print(f'\t{item} = "{Review.formats[item]}"')
            format_option = input('\tEntry: ')

            try:
                format_option = int(format_option)
                if format_option in Review.formats.keys():
                    break
                else:
                    raise
            except:
                print(f"Your entry '{format_option}' is not recognized\n")
        return Review.formats[format_option]

    def verify_rating(self, rating=None):
        """method to verify if rating is in the rating_range.
        Possible states:
            1. no rating provided
            2. rating provided is not in range
            3. rating is ok
        Returns a valid rating
        """
        if rating is None:
            rating = input(f"\nEnter a rating ({Review.rating_range[0]}-{Review.rating_range[-1]} as an integer): ")
        while rating not in Review.rating_range or not isinstance(rating, int):
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
        """Method to return the title of the book."""
        return self.title

    def __repr__(self):
        other_notes_takeaways = self.other_notes_takeaways.replace('\n', '\n\t\t')
        big_idea = self.big_idea.replace('\n', '\n\t\t')
        highlights = self.highlights.replace('\n', '\n\t\t')
        actionable_items = self.actionable_items.replace('\n', '\n\t\t')
        review_info = f"{self.title}\n"
        review_info += f"\tRating: {self.rating}\n"
        review_info += f"\tDate Rated: {self.date_added}\n"
        review_info += f"\tStart Date: {self.start_date}\n"
        review_info += f"\tEnd Date: {self.end_date}\n"
        review_info += f"\tBig Idea: {big_idea}\n"
        review_info += f"\tHighlights: {highlights}\n"
        review_info += f"\tActionable Items: {actionable_items}\n"
        review_info += f"\tOther Notes & Takeaways: {other_notes_takeaways}\n"
        review_info += f"\tFormat Consumed: {self.format_consumed}"
        return review_info

    def __str__(self):
        return self.__repr__()


class BookshelfManager:
    """This class creates new/loads instances of the bookshelf, book, and review objects
    and allows for user interaction

    Attributes:
        BookshelfManager.menu
        BookshelfManager.settings_dict
        BookshelfManager.filters_dict
        BookshelfManager.sorts_dict

    Methods:
        intro
        load_or_add_bookshelf
        list_books
        settings
        filter_books
        sort_books
        choose_book
        get_book_info
        review_a_book
        input_book_choice
    """

    # dictionary representing the Main Menu options
    menu = {
        'L': '(L)ist my books',
        'F': '(F)ilter my books',
        'T': 'sor(T) my books',
        'G': '(G)et the info about a book',
        'A': '(A)dd a book',
        'O': 'l(O)ad a goodreads csv file',
        'R': '(R)eview a book',
        'C': 'save and (C)lose',
        'Q': '(Q)uit without saving',
        'S': '(S)ettings'
    }

    # dictionary representing the Settings Menu options
    settings_dict = {
        'R': '(R)eset my bookshelf (filters, sort, and counters will return to factory settings)',
        'E': '(E)xit to Main Menu',
        'B': '(B)eta Features'
    }

    # dictionary representing the Filters Menu options
    filters_dict = {
        '0': "Filter by 1st 2 books",
        '1': "Filter by 'Want to Read'",
        '2': "Filter by 'Reviewed'",
        '3': "Filter by 'Read, but not reviewed'",
        '4': "Filter by 'Don't want to read'",
        'R': '(R)eset my bookshelf (filters, sort, and counters will return to factory settings)',
        'E': '(E)xit to Main Menu'
    }

    # dictionary representing the Sort Menu options
    sorts_dict = {
        '0': 'Title',
        '1': 'Author',
        '2': 'ISBN',
        '3': 'url',
        '4': 'Recommended by',
        '5': 'Other',
        '6': 'Status',
        '7': 'Date book was added to library',
        '8': '# of Reviews',
        '9': 'Latest Review Rating',
        'A': 'Latest Review Date',
        'E': '(E)xit to Main Menu'
    }

    def __init__(self):
        """Generate new interaction instance and allow users to interact with their bookshelves
        until the user selects one of the exit/quit/close options.
        """
        self.intro()  # introduce the program
        self.load_or_add_bookshelf()  # load or add a bookshelf
        while True:
            #Prompt to save and close
            menu = BookshelfManager.menu
            menu_option = ""
            while True:
                print('\nMain Menu\nWhat would you like to do next?\n\nEnter: ')
                for item in menu:
                    print(f'\t({item}) to {menu[item]}')
                menu_option = input('\nEntry: ').upper()
                if menu_option in menu:
                    break
                else:
                    os.system('clear')
                    print(f"Your entry '{menu_option}' is not recognized")
            if menu_option == "L":
                self.list_books()
            elif menu_option == "F":
                self.filter_books()
            elif menu_option == "T":
                self.sort_books()
            elif menu_option == "G":
                self.get_book_info()
            elif menu_option == "A":
                self.bookshelf.add_book()
            elif menu_option == "O":
                self.bookshelf.load_goodreads_csv()
            elif menu_option == "R":
                self.review_a_book()
            elif menu_option == "S":
                self.settings()
            elif menu_option == "Q":
                os.system('clear')
                print('Are you sure you want to quit? All your work will be lost!')
                print("Enter 'Quit' to confirm that you want to quit without saving")
                quit_entry = input('\nEntry: ')
                if quit_entry == 'Quit':
                    print('Have a wonderful day!\n')
                    break
                else:
                    print(f"Your entry '{quit_entry}' did not match the characters 'Quit'")
            elif menu_option == "C":
                self.bookshelf.save_bookshelf()
                print(f'{self.bookshelf} saved as {self.bookshelf}.bkshlf. Have a wonderful day!\n')
                break

    def intro(self):
        """Method to print the user introduction to the BookshelfManager and menus."""
        print()
        print("Let's manage our bookshelf.")
        print()
        print("You will be prompted to load an existing bookshelf or set up a new one.")
        print("Then you will have the opportunity to add books and reviews.")
        print("You can see the books on your bookshelf, and select them to see their details.")
        print("First let's set up your bookshelf.")
        time.sleep(0)
        print()

    def load_or_add_bookshelf(self):
        """Method to prompt user and manage loading or adding of the bookshelf."""
        load_or_add = ""
        while True:
            print('Would you like to load an existing bookshelf, or add a new one?')
            load_or_add = input(
                'Enter (L) to load an existing bookshelf or (A) to add a new bookshelf\nEntry: '
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
                    print("What is the file name (with path) of the bookshelf you would like to load?")
                    bookshelf_file = input("(Type 'C' to Cancel)\n")
                    if bookshelf_file.upper() == 'C':
                        self.load_or_add_bookshelf()
                        break
                    else:
                        self.bookshelf = Bookshelf.load_bookshelf(bookshelf_file)
                        break
                except:
                    print(f"Could not find a file with the name '{bookshelf_file}'")
            self.bookshelf.reset_bookshelf()
            print(f'\n"{self.bookshelf}" bookshelf loaded:')
            self.bookshelf.print_bookshelf_summary()
            print()

    def list_books(self):
        os.system('clear')
        self.bookshelf.print_ascii_books()

    def settings(self):
        """Method to prompt user and manage interaction with the settings menu."""
        while True:
            #Prompt to choose settings
            settings_dict = BookshelfManager.settings_dict
            settings_option = ""
            while True:
                print('\nSettings Menu\nWhat would you like to do next?\n\nEnter: ')
                for item in settings_dict:
                    print(f'\t({item}) to {settings_dict[item]}')
                settings_option = input('\nEntry: ').upper()
                if settings_option in settings_dict:
                    break
                else:
                    os.system('clear')
                    print(f"Your entry '{settings_option}' is not recognized")
            if settings_option == "R":
                self.bookshelf.reset_bookshelf()
                print(f"\nFilters, sort, and counters for '{self.bookshelf}' have been reset to factory settings.\n")
            if settings_option == "B":
                print(f'self.bookshelf: {self.bookshelf}')
                print(f'self.bookshelf.books: {self.bookshelf.books}')
                print(f'self.bookshelf.books[0]: {self.bookshelf.books[0]}')
                print(f'self.bookshelf.books[0].bookshelves: {self.bookshelf.books[0].bookshelves}')
            elif settings_option == "E":
                print(f'Returning to Main Menu\n')
                break

    def filter_books(self):
        """Method to prompt user and manage interaction with the filters menu."""
        while True:
            #Prompt to choose filter or sort
            filters_dict = BookshelfManager.filters_dict
            filters_option = ""
            while True:
                print('\nFilter & Sort Menu\nWhat would you like to do next?\n\nEnter: ')
                for item in filters_dict:
                    print(f'\t({item}) to {filters_dict[item]}')
                filters_option = input('\nEntry: ').upper()
                if filters_option in filters_dict:
                    break
                else:
                    os.system('clear')
                    print(f"Your entry '{filters_option}' is not recognized")
            if filters_option == "R":
                self.bookshelf.reset_bookshelf()
                print(f"\nFilters, sort, and counters for '{self.bookshelf}' have been reset to factory settings.\n")
            elif filters_option == "0":
                self.bookshelf.filter_books()
                print(f"\n'{self.bookshelf}' has been filtered by the first 2 books in the list.\n")
            elif filters_option in ['1', '2', '3', '4']:
                self.bookshelf.filter_books_status(Book.book_statuses[int(filters_option)])
                print(f"\n'{self.bookshelf}' has been filtered by books with a status of {filters_dict[filters_option]}.\n")
            elif filters_option == "E":
                print(f'Returning to Main Menu\n')
                break

    def sort_books(self):
        """Method to prompt user and manage interaction with the sort menu."""
        while True:
            #Prompt to choose filter or sort
            sorts_dict = BookshelfManager.sorts_dict
            sort_option = ""
            while True:
                print('\nSort Menu\nHow would you like to Sort?\n\nEnter: ')
                for item in sorts_dict:
                    print(f'\t({item}) to sort by {sorts_dict[item]}')
                sort_option = input('\nEntry: ').upper()
                if sort_option in sorts_dict:
                    break
                else:
                    os.system('clear')
                    print(f"Your entry '{sort_option}' is not recognized")
            if sort_option == "E":
                print(f'Returning to Main Menu\n')
                break
            while True:
                #Prompt to choose ascending or descending
                sort_order_dict = {'A':' (A)scending', 'D':' (D)escending'}
                sort_order = ""
                while True:
                    print('\nAscending or Descending?\n\nEnter: ')
                    for item in sort_order_dict:
                        print(f'\t({item}) to sort by {sort_order_dict[item]}')
                    sort_order = input('\nEntry: ').upper()
                    if sort_order in sort_order_dict:
                        break
                    else:
                        os.system('clear')
                        print(f"Your entry '{sort_order}' is not recognized")
                if sort_order == "D":
                    reverse_option = True
                else:
                    reverse_option = False
                self.bookshelf.sort_books(sort_val=sorts_dict[sort_option], reverse_arg=reverse_option)
                print(f"\n'{self.bookshelf}' has been sorted by book {sorts_dict[sort_option]} {sort_order_dict[sort_order]}.\n")
                break

    def choose_book(self):
        """Method to prompt user and manage interaction with the choose book menu."""
        self.list_books()
        if self.bookshelf.books_count > 0:
            if self.bookshelf.books_count == 1:
                book_choice = 1
                print(f'{self.bookshelf.books[book_choice - 1]} is your only book:')
            else:
                book_choice = self.input_book_choice()
        return self.bookshelf.filtered_books[book_choice - 1]

    def get_book_info(self):
        """Method to prompt user and manage interaction with the get book info menu."""
        book_choice = self.choose_book()
        print(f'\n{book_choice.get_book_info()}\n\nReview(s): ')
        book_choice.print_reviews()

    def review_a_book(self):
        """Method to prompt user and manage interaction with the review a book menu."""
        book_choice = self.choose_book()
        book_choice.add_review()

    def input_book_choice(self):
        """method to gather a book choice from users, until the user inputs a valid book choice.
        Possible states:
            1. no book choice provided
            2. book choice provided is not in range
            3. book choice is ok"""

        while True:
            print("Which book would you like? (Enter the number below the book on the bookshelf)")
            book_choice = input('Entry: ')
            print()

            try:
                book_choice = int(book_choice)
                if book_choice - 1 in range(0, self.bookshelf.books_count):
                    break
                else:
                    raise
            except:
                print(f"Your entry '{book_choice}' is not recognized\n")
        return book_choice


# Main Bookshelf Program - Conor Healy
# The main program prompts the user to load a bookshelf or create a new one.

os.system('clear')
BookshelfManager()
