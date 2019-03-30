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
