class LibraryIterator:
    def __init__(self, lib_books):
        self.lib_books = lib_books
        self.titles = list(lib_books.keys())
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.titles) - 1:
            self.index += 1
        elif self.index == len(self.titles) - 1:
            self.index += 1  # Move out of bounds
            return None
        return self.__current__()

    def __prev__(self):
        if self.index > 0:
            self.index -= 1
        return self.__current__()

    def __current__(self):
        if 0 <= self.index < len(self.titles):
            title = self.titles[self.index]
            book_dict = self.lib_books[title][0].__dict__()
            book_dict['copies'] = self.lib_books[title][1] if type(self.lib_books[title][1]) == int else len(self.lib_books[title][1])
            return book_dict
        return None
   
    def __first__(self):
        self.index = 0
        return self.__current__()

    def __last__(self):
        self.index = len(self.titles) - 1
        return self.__current__()

    def is_first(self):
        return self.index == 0

    def is_last(self):
        return self.index == len(self.titles) - 1
