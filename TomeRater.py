class User(object):
    def __init__(self, name, email):
        self.name = str(name)
        self.email = str(email)
        self.books = {} #key: Book object, value: user's rating
        self.rating_collection = [] #A list of valid book ratings made by user

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print('Email has been updated to {email}'.format(email = self.email))

    def __repr__(self):
        return 'User {username}, email: {email}, books read: {qty}'.format(username = self.name, email = self.email, qty = len(self.books))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.name:
            return True
        else:
            return False

    def read_books(self, book, rating = None):
        self.books[book] = rating
        if rating is not None:
            self.rating_collection.append(rating)

    def get_average_rating(self):
        if len(self.ratings) > 0:
            return sum(self.ratings)/len(self.ratings)
        else:
            return 0.0

class Book:
    def __init__(self, title, isbn, price):
        self.title = str(title)
        self.isbn = int(isbn)
        self.price = price
        self.ratings = []

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def __repr__(self):
        return '\n{title}, average rated {rating:.1f}'.format(title = self.title, rating = self.get_average_rating())

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print('\nISBN of {title} has been updated to {isbn}'.format(isbn = self.isbn, title = self.title))

    def add_rating(self, rating):
        if self.valid_rating(rating):
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        if len(self.ratings) > 0:
            return sum(self.ratings)/len(self.ratings)
        else:
            return 0.0

    def valid_rating(self, rating):
        if rating is not None:
            if 0 <= rating <= 4:
                return True
        return False

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return '\n{title} by {author}, average rated {rating:.1f}'.format(title = self.title, author = self.author, rating = self.get_average_rating())

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return '\n{title}, a {level} manual on {subject}, average rated {rating:.1f}'.format(title = self.title, level = self.level, subject = self.subject, rating = self.get_average_rating())

#Main Class in this app
class TomeRater:
    def __init__(self):
        self.users = {} #key:User's Email value: User object
        self.books = {} #key:Book object  value: qty of users read it
        self.books_price = {} #key: Book title string: book price

    def __repr__(self):
        return self.print_catalog()

    def create_book(self, title, isbn, price = None):
        if self.not_duplicate_book(isbn):
            new_book = Book(title, isbn, price)
            if self.price_exist(price):
                self.books_price[title] = price
            return new_book

    def create_novel(self, title, author, isbn, price = None):
        if self.not_duplicate_book(isbn):
            new_novel = Fiction(title, author, isbn, price)
            if self.price_exist(price):
                self.books_price[title] = price
            return new_novel

    def create_non_fiction(self, title, subject, level, isbn, price = None):
        if self.not_duplicate_book(isbn):
            new_non_fiction = Non_Fiction(title, subject, level, isbn, price)
            if self.price_exist(price):
                self.books_price[title] = price
            return new_non_fiction

    def add_book_to_user(self, book, email, rating = None):
        if self.user_exist(email):
            self.users[email].read_books(book, rating)
            book.add_rating(rating)
            if self.book_exist(book):
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print ('No user with email {email}!'.format(email = email))

    def add_user(self, name, email, user_books = None):
        if self.user_exist(email):
            print('This User already exists')
        else:
            if self.valid_email(email):
                self.users[email] = User(name, email)
                if user_books is not None:
                    for book in user_books:
                        self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_price_catalog(self):
        for title in self.books_price:
            print('\n{title}, marked price as {price}'.format(title = title, price = self.books_price[title]))

    def print_users(self):
        for user in self.users:
            print(self.users[user])

    def most_read_book(self):
        for book in self.books:
            if self.books[book] == max(self.books.values()):
                return book

    def highest_rated_book(self):
        highest_rating = 0.0
        result_book = None
        for book in self.books:
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
                result_book = book
        return result_book

    def most_positive_user(self):
        highest_rating = 0.0
        result_user = None
        for key in self.users:
            if self.users[key].get_average_rating() > highest_rating:
                highest_rating = self.users[key].get_average_rating()
                result_user = self.users[key]
        return result_user

    def get_n_most_read_books(self, n):
    #This functions print out the first n most read book in descending order
        most_read_book_list = sorted(self.books, key = self.books.get, reverse = True)
        for i in range(n):
            print (most_read_book_list[i])

    def get_n_most_expensive_books(self, n):
        most_expensive_nook_list = sorted(self.books_price, key = self.books_price.get, reverse = True)
        for i in range(n):
            print (most_expensive_nook_list[i])

    def user_exist(self, email):
        if email in self.users:
            return True
        else:
            return False

    def book_exist(self, book):
        if book in self.books:
            return True
        else:
            return False

    def price_exist(self, price):
        if price is not None:
            return True
        else:
            return False

    def not_duplicate_book(self, isbn):
        for book in self.books:
            if isbn == book.isbn:
                print ('\nThis isbn already exsits in library')
                return False
        return True

    def valid_email(self, email):
        valid_root_domain = ['.com', '.edu', '.org']
        if ('@' in email) and (email[-4:] in valid_root_domain):
            return True
        print ('Invalid Email address, a valid address must have \'@\' and end with either \'.com\', \'.edu\', \'.org\'')
        return False
