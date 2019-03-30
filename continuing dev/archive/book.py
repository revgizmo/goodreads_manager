import functools


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
        Bookshelves: {self.bookshelves}\n\
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
