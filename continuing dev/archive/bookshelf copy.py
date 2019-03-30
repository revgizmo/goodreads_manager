'''A program to manage my bookshelves, books, and reviews.'''

import pickle
import functools
import time
import os


class BookshelfManager:
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
        '''Generate new interaction instance and allow users to interact with their bookshelves
        until the user selects save and close = "C"'''
        self.intro()  # introduce the program

        while True:

            #Prompt to save and close
            menu = BookshelfManager.menu
            menu_option = ""
            while True:
                print('\nWhat would you like to do next?\n\nEnter: ')
                for item in menu:
                    print(f'\t({item}) to {menu[item]}')
                menu_option = input('\nEntry: ').upper()
                if menu_option in menu:
                    break
                else:
                    os.system('clear')
                    print(f"Your entry '{menu_option}' is not recognized")
            if menu_option == "C":
                print(f'self.bookshelf saved.  Have a wonderful day!\n')
                # print(f'{self.bookshelf} saved.  Have a wonderful day!\n')
                break



    def intro(self):
        print()
        print("Let's manage our bookshelf.\n\
            You will be prompted to load an existing bookshelf or set up a new one.")
        print("Then you will have the opportunity to add books and reviews.")
        print("You can see the books on your bookshelf, and select them to see their details.")
        print("First let's set up your bookshelf.")
        # time.sleep(0)
        print()


# Main Bookshelf Program - Conor Healy
# The main program prompts the user to load a bookshelf or create a new one.

os.system('clear')
BookshelfManager()
