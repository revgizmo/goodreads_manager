
# coding: utf-8

# # Design Document (10 points):
# 
# 
# ## Summary 
# 1. I intend to implement a tool to manage book ratings, reviews and thoughts.
# 
# ## Expected Classes (4-5+):
# 1. ### <u>__Bookshelf__</u> (class): 
# 
#     1. Purpose
#         1. A place for all my books
#         1. Do I really need a bookshelf class? Probably not now, but I could see wanting one to manage different people, work/personal, by subject, etc.
# 
#     1. Methods/functions
#         1. Filter to top reviews
#         1. Subset by genre
#         1. A way to save and load my bookshelf
# 
#     1. Expected i/o and attributes
#         1.  

# In[1]:


import pickle


class Bookshelf():
    '''An entity that represents a place for all my books.
    
    Attributes:
    books
    
    Methods
    get_books
    print_books
    print_books_info
    print_reviews
    add_book
    save_bookshelf
    load_bookshelf
    '''
    count = 0

    def __init__(self, name="bookshelf"):
        self.name = name
        self.books = []
        Bookshelf.count += 1

    def __repr__(self):
        return self.name

    def get_books(self):
        return (self.books)

    def print_books(self, sort_val=None):
        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            books_sorted = self.books

        if books_sorted:
            [print(book.get_title(), '\n') for book in books_sorted]
        else:
            print("No books to print: Bookshelf is empty!  Find some books!")

    def print_books_info(self, sort_val=None):
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

    def add_book(self, book=None):
        if book == None:
            title = input("Enter a title: ")
            author = input("Enter an author: ")
            ISBN = input("Enter an ISBN (if you have one): ")
            url = input(
                "Enter a url for Amazon/Goodreads/etc.(if you have one): ")
            other = input(
                "Enter any additional notes the you would like to record about the book, \
                \not including review information: ")
            book_status = int(
                input('Enter any number for the status of the book: \n\
            1 = "Want to Read"\n\
            2 = "Reviewed"\n\
            3 = "Read_No_Review"\n\
            4 = "Don\'t want to read"'))
            temp_book = Book(title, author, ISBN, url, other, book_status)
            print(temp_book.get_book_info(), '\n')

            if int(
                    input(
                        'Would you like to review this book now? (1 = Yes, 0 = No)'
                    )) == 1:
                temp_book.add_review()

            self.books.append(temp_book)
            print(f"\n{self.books[-1]}")
        else:
            self.books.append(book)

    def save_bookshelf(self):
        pickle.dump(self, open(f"{self.name}.bkshlf", "wb"))

    @classmethod
    def load_bookshelf(cls, file):
        return pickle.load(open(file, "rb"))

    def print_ascii_books(self, sort_val=None):
        if sort_val:
            raise Exception("Need to make sort() work with the Books class")
        else:
            books_sorted = self.books

        books_sorted.ascii_book()

    def print_ascii_books(self,
                          sort_val=None,
                          letters_per_book=20,
                          books_per_row=14):
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
                num_letters = letters_per_book
                while num_letters:
                    book_string = ''
                    col_string = ''
                    for i in range(0, books_in_row):
                        temp_book = books[num_books - books_count + i]
                        if letters_per_book - num_letters < len(temp_book):
                            book_string_letter = temp_book[letters_per_book -
                                                           num_letters]
                        else:
                            book_string_letter = ' '
                        book_string += f'| {book_string_letter} |'
                        col_string += f' {num_books - books_count + i:-2}  '
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
                  (letters_per_book + 2) + k)
            print("No books to print: Bookshelf is empty!  Find some books!")


# 1. ### <u>__Book__</u> (class):
# 
#     1. Purpose
#         1. Record each book the user has on their list with descriptive information and references to any reviews made of the book.
# 
#     1. Methods/functions
#         1. Add Book
#         1. Edit Book 
#         1. Get Book_name
#         1. Get book_info (all info)
#         1. Return all books entered/reviewed
#         1. Return Review(s)
#         1. Return Actionable Items across all books
# 
#     1. Expected i/o and attributes
#         1. Title
#         1. Author
#         1. ISBN
#         1. url to Amazon/goodreads
#         1. "Other" - text field for whatever additional notes the user would like to record about the book (not including review information)
#         1. Book status - (Reviewed, Want to Read, Read_No_Review, Don't want to read)
#         1. Reviews - (exact functionality TBD) - creation, modification, deletion

# In[2]:


class Book():
    '''An entity that represents a book and associated data.
    
    Class Attributes:
    book_statuses = 1: 'Want to Read', 
                2: 'Reviewed', 
                3: 'Read_No_Review', 
                4: 'Don't want to read'
    
    Instance Attributes:
    title
    author
    ISBN
    url (to Amazon/goodreads/etc.)
    other (text field for whatever additional notes the user would like to record about the book, 
        not including review information)
    book_status - (Want to Read, Reviewed, Read_No_Review, Don't want to read)
    
    Methods:
    get_title
    get_book_info
    '''
    count = 0

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
                 other=None,
                 book_status=1,
                 review=None):
        if title == None:
            raise Exception("Need a book title!")
        else:
            self.title = title
            self.author = author
            self.ISBN = ISBN
            self.url = url
            self.other = other
            if review == None:
                self.reviews = []
            else:
                self.reviews = [review]
            # Will want book_status to automatically reflect if there is a Review
            self.book_status = Book.book_statuses[book_status]
        Book.count += 1

    def get_title(self):
        return self.title

    def get_book_info(self):
        return (f"{self}\n        Author: {self.author}\n        ISBN: {self.ISBN}\n        url: {self.url}\n        Other: {self.other}\n        Status: {self.book_status}\n        Reviews: {len(self.reviews)}")

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

    def __repr__(self):
        return self.title

    def add_review(self, review=None):
        if review == None:
            rating = input("Enter a rating: ")
            start_date = input("Enter a start_date: ")
            end_date = input("Enter a end_date: ")
            big_idea = input("Enter the big_idea: ")
            other_notes_takeaways = input("Enter other_notes_takeaways: ")

            self.reviews.append(
                Review(self, rating, start_date, end_date, big_idea,
                       other_notes_takeaways))
            print(f"\n{self.reviews[-1]}")
        else:
            self.reviews.append(review)


# 1. ### <u>__Review__</u> (class): 
# 
#     1. Purpose
#         1. Capture reader notes related to a book
#     
#     1. Methods/functions
#         1. Add Review
#         1. Edit Review
#     
#     1. Expected i/o and attributes
#         1. Rating (1-5), 
#         1. Start/end dates of reading session
#         1. The Big Idea: What were the big ideas of the book?
#         1. Other Notes & Takeaways
#             1. maybe just one text string per review? or __possibly class/instances__?
# 
#         

# In[3]:


class Review():
    '''An entity that represents a book review and associated data.
    
    Attributes:
    rating (1-5), 
    Start/end dates of reading session
    The Big Idea: What were the big ideas of the book?
    Other Notes & Takeaways
    
    Methods:
    
    '''
    count = 0

    def __init__(self,
                 book=None,
                 rating=None,
                 start_date=None,
                 end_date=None,
                 big_idea=None,
                 other_notes_takeaways=None):
        if book == None:
            raise Exception("Need a book!")
        elif rating == None:
            raise Exception("Need a rating!")
        else:
            self.title = book.title
            self.rating = rating
            self.start_date = start_date
            self.end_date = end_date
            self.big_idea = big_idea
            self.other_notes_takeaways = other_notes_takeaways
            book.reviews.append(self)
        Review.count += 1

    def get_title(self):
        return self.title

    def __repr__(self):
        return (f"{self.title}\n        rating: {self.rating}\n        start_date: {self.start_date}\n        end_date: {self.end_date}\n        Big Idea: {self.big_idea}\n        Other notes & takeaways: {self.other_notes_takeaways}")


# In[4]:


def InputBook(bookshelf):
    title = input("Enter a title: ")
    author = input("Enter an author: ")
    ISBN = input("Enter an ISBN (if you have one): ")
    url = input("Enter a url for Amazon/Goodreads/etc.(if you have one): ")
    other = input(
        "Enter any additional notes the you would like to record about the book, not including review information: "
    )
    book_status = int(
        input('Enter any number for the status of the book: \n\
    1 = "Want to Read"\n\
    2 = "Reviewed"\n\
    3 = "Read_No_Review"\n\
    4 = "Don\'t want to read"'))

    bookshelf.books.append(Book(title, author, ISBN, url, other, book_status))
    print(bookshelf.books[-1].get_book_info())


# In[5]:


def InputReview(book):
    rating = input("Enter a rating: ")
    start_date = input("Enter a start_date: ")
    end_date = input("Enter a end_date: ")
    big_idea = input("Enter the big_idea: ")
    other_notes_takeaways = input("Enter other_notes_takeaways: ")

    book.reviews.append(
        Review(book, rating, start_date, end_date, big_idea,
               other_notes_takeaways))
    print(f"\n{book.reviews[-1]}")


# 1. ### <u>__Highlighted Sections__</u> (class): 
#                 
#     1. Purpose
#         1. Capture Quotes or other highlighted sections)
# 
#     1. Methods/functions
#         1.  Set Highlight
#         1.  Get Highlight
# 
#     1. Expected i/o and attributes
#         1. page #
#         1. Details
# 
# 1. ### <u>__Actionable Items__</u> (class): 
# 
#     1. Purpose
#         1. (Ideas I might want to try in the future and notes regarding the idea.)
# 
#     1. Methods/functions
#         1.  
# 
#     1. Expected i/o and attributes
#         1. Actionable Item description/information/name, 
#         1. due date?
# 
# 1. ### <u>__Format consumed__</u> (possible class with children): 
#     1. (Physical Book, ebook, Audiobook, Other, etc.)
#         
# 
# ## Out of scope: 
# 1. Reporting on number of books, 
# 1. Timing of reading/reviews, 
# 1. Details on highlights/quotes to separate explicit quotations from highlights/thoughts & print of explicit quotations)
# 1. Deduplication of books and reviews
#     1. Double check titles
#     1. Double check every other value at the class level
#     1. Offer to merge if missing data, and prompt user to choose between them
#     1. Prompt user throughout merge process
# 1. Create magic methods for eq, lt, gt so that sort works, add, sub to append, remove
# 1. Edit existing books/reviews.
#     1. https://stackoverflow.com/questions/2533120/show-default-value-for-editing-on-python-input-possible/2533134
# 1. InputBook(): add question: do you want to review now? and appropriate functionality
# 1. Update book_status to automatically reflect if there is a Review
# 
# 
#     

# # Example:
# 
# 1. Create an example bookshelf
# 1. Create a couple books
# 1. Add the books to my bookshelf (using different methods)
# 1. Create a couple reviews
# 
# 
# 

# ## Create an example bookshelf

# In[6]:


# 1. Create an example bookshelf
my_bookshelf = Bookshelf()


# In[7]:


print(my_bookshelf)
print(my_bookshelf.books)
print(my_bookshelf.get_books())
my_bookshelf.print_books()
my_bookshelf.print_books_info()
my_bookshelf.print_reviews()
# print(a.book_statuses[2])


# ## Create a couple books
# 
# ### Create "Book1: Hello World!"

# In[8]:


# 1. Create a couple books

book1 = Book("Book1: Hello World!", book_status=2)
print(book1.__dict__)
print()

print(f"Book: {book1}")
print(f"Book Title: {book1.title}")
print(f"\"{book1.title}\" Author: {book1.author}")
print(f"\"{book1.title}\" ISBN: {book1.ISBN}")
print(f"\"{book1.title}\" url: {book1.url}")
print(f"\"{book1.title}\" Other: {book1.other}")
print(f"\"{book1.title}\" Status: {book1.book_status}")
print()
print()


# ### Create "Book2: Thinking Fast & Slow"

# In[9]:


book2 = Book("Book2: Thinking Fast & Slow", "Daniel Kahnamen")
print(book2.__dict__)
print()
print(book2)
print()
book2.get_title()
print()
print(book2.get_book_info())


# In[10]:


print(my_bookshelf)
print(my_bookshelf.books)
print(my_bookshelf.get_books())
my_bookshelf.print_books()
my_bookshelf.print_books_info()
my_bookshelf.print_reviews()
# print(a.book_statuses[2])


# ## Add the books to my bookshelf (using different methods)

# In[11]:


# 1. Add the books to my bookshelf (using different methods)
my_bookshelf.books.append(book1)
my_bookshelf.add_book(book2)


# In[12]:


my_bookshelf.print_books()
print("\n\n")
#my_bookshelf.print_books("sort")


# In[13]:


print(my_bookshelf)
print(my_bookshelf.books)
print(my_bookshelf.get_books())
my_bookshelf.print_books()
my_bookshelf.print_books_info()
my_bookshelf.print_reviews()
# print(a.book_statuses[2])


# ## Create a couple reviews

# In[14]:


# 1. Create a couple reviews

#Create review for book 1
review1 = Review(book1, rating=5)

print(review1)

print()

#Create review for book 2
review2 = Review(
    book2,
    rating=1,
    start_date="2019-01-01",
    end_date="2019-02-29",
    big_idea="The world needs a Hello",
    other_notes_takeaways=
    "\n\t\t- Bullet 1\n\t\t- Bullet 2\n\t\t- ...\n\t\t- Bullet n")
print(review2)


# In[15]:


print(my_bookshelf)
print(my_bookshelf.books)
print(my_bookshelf.get_books())
my_bookshelf.print_books()
my_bookshelf.print_books_info()
my_bookshelf.print_reviews()
# print(a.book_statuses[2])


# ## Print out the example bookshelf

# In[16]:


print("print(my_bookshelf)")
print(my_bookshelf)

print("\n---\n\n print(my_bookshelf.books)")
print(my_bookshelf.books)

print("\n---\n\n my_bookshelf.print_books()")
my_bookshelf.print_books()

print("\n---\n\n my_bookshelf.print_ascii_books()")
my_bookshelf.print_ascii_books()

print("\n---\n\n my_bookshelf.print_books_info()")
my_bookshelf.print_books_info()

print("\n---\n\n print(my_bookshelf.get_books())")
print(my_bookshelf.get_books())

print("\n---\n\n print(my_bookshelf.print_reviews())")
my_bookshelf.print_reviews()

print(
    "\n---\n\n [print(book.get_title(),'\\n') for book in my_bookshelf.books]")
[print(book.get_title(), '\n') for book in my_bookshelf.books]

print(
    "\n---\n\n [print(book.get_book_info(),'\\n') for book in my_bookshelf.books]"
)
[print(book.get_book_info(), '\n') for book in my_bookshelf.books]

print(
    "\n---\n\n [print(review,'\\n') for book in my_bookshelf.books for review in book.reviews ]"
)
[print(review, '\n') for book in my_bookshelf.books for review in book.reviews]


# In[17]:


print(f'Bookshelf.count: {Bookshelf.count}')
print(f'Book.count: {Book.count}')

print(f'Review.count: {Review.count}')

my_bookshelf.save_bookshelf()
