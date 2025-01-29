class Book:
    def __init__(self, title, author, year, category, copies=1):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__category = category

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def get_categories(self):
        return self.__category

    def __str__(self):
        return f"Title: {self.__title}, Author: {self.__author}, Year: {self.__year}, Category: {self.__category}"

    def __dict__(self):
        return {
            "title": self.__title,
            "author": self.__author,
            "year": self.__year,
            "category": self.__category,
        }


class BorrowedBook(Book):
    def __init__(self, title, author, year, category, copies=1, borrower=0):
        super().__init__(title, author, year, category, copies)
        self.borrowed = borrower

    def get_borrowed_times(self):
        return self.borrowed

    def increment_borrowed_times(self):
        self.borrowed += 1

    def __str__(self):
        return super().__str__() + f", Borrowed Times: {self.borrowed}"

    def __dict__(self):
        book_dict = super().__dict__()
        book_dict["borrowed"] = self.borrowed
        return book_dict
