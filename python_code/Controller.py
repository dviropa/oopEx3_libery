import Library
# from gui import LibraryGUI
from Book import BorrowedBook
    
class Controller:
    def __init__(self, library : Library.Library, gui):
        self.library : Library.Library  = library
        self.gui = gui
        self.username = None
        self.gui.set_controller(self)
        
    def login(self, user, password):
        try:
            if self.library.user_login(user, password):
                self.username = user
                return True
            else:
                return False
                
        except Exception as e:
            self.gui.show_error(str(e))
            
    def register(self, user, password):
        try:
            return self.library.register_new_user(user, password)
        except Exception as e:
            self.gui.show_error(str(e))
            
    def add_book(self, title, author, year, category, copies): ## Example of a method that is called from the GUI
        try:
            # if not self.library.is_logged_in(user):
            #     raise Exception("You need to be logged in to add a book")
            self.library.add_book(title, author, int(year), category, int(copies))
            return True
            # self.gui.update_books(self.library.get_books())
        except Exception as e:
            self.gui.show_error(str(e))
            return False
        
    def remove_book(self, book_name):
        try:
            self.library.remove_books(book_name)
            return True
            # self.gui.update_books(self.library.get_books())
        except Exception as e:
            self.gui.show_error(str(e))
            return False
    
    def get_books(self):
        return self.library.get_books()
    def get_available_books(self):
        return self.library.get_available_books()
    def get_borrowed_books(self):
        return self.library.get_borrowed_books()

    def Lend_Book(self,title):
        try:
            return self.library.loan_book(title, self.username)
        except Exception as e:
            return False
            # self.gui.show_error(str(e))

    def Return_Book(self,title):
        try:
            return self.library.return_book(title, self.username)
        except Exception as e:
            return False
            #self.gui.show_error(str(e))

    def Popular_Book(self):
        return self.library.top10_popular_books()
    def whitinglist(self):
        return self.library.get_books_in_waiting_list()
    def Popular_Book_and_whitinglist(self):
        return self.library.top10_and_waiting_list()


    def search(self, criteria):
        
        return self.dataframe_to_dict(self.library.search(criteria))

    def dataframe_to_dict(self, df):
        if df is None or df.empty:
            self.gui.show_error("No results found!")
            return {}
        result = {}
        for _, row in df.iterrows():
            book_obj = BorrowedBook(
                title=row["title"],
                author=row["author"],
                year=row["year"],
                category=row["category"],
                borrower=row.get("borrowed", 0)  # ברירת מחדל אם borrowed לא קיים
            )
            copies_dict = {i: (False, None) for i in range(row["copies"])}
            result[row["title"]] = (book_obj, copies_dict)
        return result

