# inspired by https://codegolf.stackexchange.com/questions/111833/ascii-bookshelves
books = [
    "Hello World!", "Thinking Fast & Slow", "cdeabcd", "deabcdea", "eabcdeabc",
    "Hello World!", "Thinking Fast & Slow", "cdeabcd", "deabcdea", "eabcdeabc",
    "Hello World!", "Thinking Fast & Slow", "cdeabcd", "Hello World!",
    "Thinking Fast & Slow", "cdeabcd", "deabcdea", "eabcdeabc", "Hello World!",
    "Thinking Fast & Slow", "cdeabcd", "deabcdea", "eabcdeabc", "Hello World!",
    "Thinking Fast & Slow", "cdeabcd"
]


def ascii_book(books, letters_per_book=5, books_per_row=14):
    num_books = len(books)
    books_count = len(books)
    k = '|' + '-----' * books_per_row + '|'
    while books_count:
        books_in_row = books_count % books_per_row or books_per_row
        print(k + '\n' + ('|' + '     ' * (books_per_row - books_in_row) +
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
        print('|' + '     ' * (books_per_row - books_in_row) + col_string +
              '|')
        books_count -= books_in_row


ascii_book(books, 20, 14)