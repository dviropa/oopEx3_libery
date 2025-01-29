import tkinter as tk
from tkinter import messagebox
from Controller import Controller
from LibraryIterator import LibraryIterator


class LibraryGUI:
    class BooksDisplay(tk.Toplevel):
        def __init__(self, parent, books):
            super().__init__(parent)
            self.title("Books")
            self.geometry("400x300")
            self.books_iter = LibraryIterator(books)

            # Labels for book details
            self.book_title = tk.Label(self, text="", font=("Arial", 14), width=30, anchor="center")
            self.book_author = tk.Label(self, text="", font=("Arial", 12), width=30, anchor="center")
            self.book_year = tk.Label(self, text="", font=("Arial", 12), width=30, anchor="center")
            self.book_category = tk.Label(self, text="", font=("Arial", 12), width=30, anchor="center")
            self.copies = tk.Label(self, text="", font=("Arial", 12), width=30, anchor="center")
            
            # Navigation buttons
            self.prev_button = tk.Button(self, text="←", command=self.prev_book, font=("Arial", 16))
            self.next_button = tk.Button(self, text="→", command=self.next_book, font=("Arial", 16))

            # Layout
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
            self.grid_columnconfigure(2, weight=1)

            self.book_title.grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
            self.book_author.grid(row=1, column=1, pady=5, sticky="nsew")
            self.book_year.grid(row=2, column=1, pady=5, sticky="nsew")
            self.book_category.grid(row=3, column=1, pady=5, sticky="nsew")
            self.copies.grid(row=4, column=1, pady=5, sticky="nsew")
            
            self.prev_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
            self.next_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

            self.display_books()

        def display_books(self):
            self.display_book(self.books_iter.__first__())
            self.update_buttons()

        def prev_book(self):
            book = self.books_iter.__prev__()
            self.display_book(book)
            self.update_buttons()

        def next_book(self):
            book = self.books_iter.__next__()
            self.display_book(book)
            self.update_buttons()

        def display_book(self, book):
            if book:
                self.book_title.config(text=f"Title: {book['title']}")
                self.book_author.config(text=f"Author: {book['author']}")
                self.book_year.config(text=f"Year: {book['year']}")
                self.book_category.config(text=f"Category: {book['category']}")
                self.copies.config(text=f"Copies: {book['copies']}")
            else:
                self.book_title.config(text="No Book Available")
                self.book_author.config(text="")
                self.book_year.config(text="")
                self.book_category.config(text="")
                self.copies.config(text="")

        def update_buttons(self):
            if self.books_iter.is_first():
                self.prev_button.config(state="disabled")
            else:
                self.prev_button.config(state="normal")

            if self.books_iter.is_last():
                self.next_button.config(state="disabled")
            else:
                self.next_button.config(state="normal")

    def __init__(self, root):  # תיקון שם הפונקציה
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")
        self.init_login()

    def set_controller(self, controller):
        if controller is None:
            raise ValueError("Controller cannot be None")
        self.controller: Controller = controller
        
    def create_button(self, text, command, x=None, y=None, relx=None, rely=None, anchor=None):
        button = tk.Button(self.root, text=text, command=command)
        if x is not None and y is not None:
            button.place(x=x, y=y)
        elif relx is not None and rely is not None:
            button.place(relx=relx, rely=rely, anchor=anchor)
        else:
            button.pack(pady=5)
        return button

    def init_login(self):
        self.clear_window()
        self.root.title("Login")

        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username = tk.Entry(self.root)
        self.username.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password = tk.Entry(self.root, show="*")
        self.password.pack(pady=5)

        self.create_button("Log In", self.login)
        self.create_button("Register", self.register)

    def init_main_menu(self):
        self.clear_window()
        self.root.title("Home")

        self.create_button("Add Book", self.add_book_page)
        self.create_button("Remove Book", self.remove_book_page)
        self.create_button("Search Book", self.search_book_page)
        self.create_button("View Books", self.view_books_page)
        self.create_button("Lend Book", self.lend_book_page)
        self.create_button("Return Book", self.return_book_page)
        self.create_button("Popular Book", self.popular_book_page)

        # הוספת כפתור Log Out בתחתית השמאלית
        self.create_button("Log Out", self.init_login, x=10, y=360)

    def Popular_Book(self):
        # מחיקת כל הלייבלים הקודמים
        self.clear_labels()

        # יצירת רשימת הספרים הפופולריים
        popular_books = self.controller.Popular_Book()

        # הצגת לייבל חדש
        self.previous_labels.append(tk.Label(self.root, text="Popular Books:"))
        self.previous_labels[-1].pack(pady=10)

        # הצגת הספרים
        self.display_books(popular_books)

    def whitinglist(self):
        # מחיקת כל הלייבלים הקודמים
        self.clear_labels()

        # יצירת רשימת ספרים ב-"waiting list"
        waiting_list_books = self.controller.whitinglist()

        # הצגת לייבל חדש
        self.previous_labels.append(tk.Label(self.root, text="Waiting List:"))
        self.previous_labels[-1].pack(pady=10)

        # הצגת הספרים
        self.display_books(waiting_list_books)

    def Popular_Book_and_whitinglist(self):
        # מחיקת כל הלייבלים הקודמים
        self.clear_labels()

        # יצירת רשימת ספרים פופולריים ורשימת "waiting list"
        combined_books = self.controller.Popular_Book_and_whitinglist()

        # הצגת לייבל חדש
        self.previous_labels.append(tk.Label(self.root, text="Popular Books and Waiting List:"))
        self.previous_labels[-1].pack(pady=10)

        # הצגת הספרים
        self.display_books(combined_books)

    def display_books(self, books):
        # יצירת לייבל לכל ספר
        if books:
            for book in books:
                label = tk.Label(self.root, text=book)
                label.pack()
                self.previous_labels.append(label)
        else:
            messagebox.showerror("Error", "No books to display!")

    def clear_labels(self):
        # מחיקת כל הלייבלים שהוצגו
        if hasattr(self, 'previous_labels'):
            for label in self.previous_labels:
                label.destroy()
        self.previous_labels = []

    # אתחול רשימת הלייבלים בהתחלה
    def popular_book_page(self):
        self.clear_window()
        self.root.title("Popular Books")
        self.previous_labels = []  # אתחול הרשימה
        self.create_button("Popular Book", self.Popular_Book)
        self.create_button("Waiting List", self.whitinglist)
        self.create_button("Popular Books and Waiting List", self.Popular_Book_and_whitinglist)
        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")

    def return_book_page(self):
        self.clear_window()
        self.root.title("Return Book")

        tk.Label(self.root, text="Book Name:").pack(pady=10)
        self.book_name_entry = tk.Entry(self.root)
        self.book_name_entry.pack(pady=5)

        self.create_button("Enter", self.return_book, relx=0.1, rely=0.9, anchor="center")
        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")

    def return_book(self):
        book_name = self.book_name_entry.get()
        if  self.controller.Return_Book(book_name):
            messagebox.showinfo("Success", "Book returned successfully")
        else:
            messagebox.showerror("Error", "Book return failed")

    def lend_book_page(self):
        self.clear_window()
        self.root.title("Lend Book")

        tk.Label(self.root, text="Book Name:").pack(pady=10)
        self.book_name_entry = tk.Entry(self.root)
        self.book_name_entry.pack(pady=5)

        self.create_button("Enter", self.lend_book, relx=0.1, rely=0.9, anchor="center")
        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")

    def lend_book(self):
        book_name = self.book_name_entry.get()
        if self.controller.Lend_Book(book_name):
            messagebox.showinfo("Success", "Borrowed book successfully")
        else:
            messagebox.showerror("Error", "Borrowed book fail")

    def view_books_page(self):
        self.clear_window()
        self.root.title("View Books")

        tk.Label(self.root, text="View Books By:").pack(pady=10)

        self.create_button("All Books", lambda: self.view_books())
        self.create_button("Available Books", lambda: self.view_available_books())
        self.create_button("Borrowed Books", lambda: self.view_borrowed_books())

        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")

    def view_books_by_category(self):
        self.clear_window()
        self.root.title("View Books By Category")

        tk.Label(self.root, text="Enter Category:").pack(pady=10)
        self.category_field = tk.Entry(self.root)
        self.category_field.pack(pady=5)

        self.create_button("Enter", self.display_books_by_category, relx=0.1, rely=0.9, anchor="center")
        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")

    def display_books_by_category(self):
        category = self.category_field.get()
        if category:
            messagebox.showinfo("Success", "Displayed all books by category you chose successfully")
        else:
            messagebox.showerror("Error", "Displayed all books by category you chose fail")

    def display_books_action(self, book_type, success_msg, fail_msg):
        if book_type:
            messagebox.showinfo("Success", success_msg)
        else:
            messagebox.showerror("Error", fail_msg)
            
            
    def view_books(self):
        books_amunt = self.controller.get_books()
        self.BooksDisplay(self.root, books_amunt).display_books()

    def view_available_books(self):
        books = self.controller.get_available_books()
        self.BooksDisplay(self.root, books).display_books()
    def view_borrowed_books(self):
        books = self.controller.get_borrowed_books()
        self.BooksDisplay(self.root, books).display_books()

        
        
    def add_book_page(self):
        self.clear_window()
        self.root.title("Add Book")

        tk.Label(self.root, text="Name:").pack(pady=5)
        self.book_name = tk.Entry(self.root)
        self.book_name.pack(pady=5)

        tk.Label(self.root, text="Author:").pack(pady=5)
        self.book_author = tk.Entry(self.root)
        self.book_author.pack(pady=5)

        tk.Label(self.root, text="Year:").pack(pady=5)
        self.book_year = tk.Entry(self.root)
        self.book_year.pack(pady=5)

        tk.Label(self.root, text="Category:").pack(pady=5)
        self.book_category = tk.Entry(self.root)
        self.book_category.pack(pady=5)

        tk.Label(self.root, text="Number of Copies:").pack(pady=5)
        self.book_copies = tk.Entry(self.root)
        self.book_copies.pack(pady=5)

        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")
        self.create_button("Enter", self.add_book, relx=0.1, rely=0.9, anchor="center")

    def remove_book_page(self):
        self.clear_window()
        self.root.title("Remove Book")

        tk.Label(self.root, text="Book Name:").pack(pady=5)
        self.book_to_remove = tk.Entry(self.root)
        self.book_to_remove.pack(pady=5)

        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")
        self.create_button("Enter", self.remove_book, relx=0.1, rely=0.9, anchor="center")

    def remove_book(self):
        if self.controller.remove_book(str(self.book_to_remove.get())):
            messagebox.showinfo("Success", "Book removed successfully")
        else:
            messagebox.showerror("Error", "Book removed fail")


    def search_book_page(self):
        self.clear_window()
        self.root.title("Search Book")

        tk.Label(self.root, text="Search By:").grid(row=0)

        
        # create input boxes for the search and buttons for the search options 
        
        ## create a grid layout or a form layout for the search options
        
        self.author_label = tk.Label(self.root, text="Author Name:")
        self.author_name = tk.Entry(self.root)
        self.year_label = tk.Label(self.root, text="Year:")
        self.year = tk.Entry(self.root)
        self.category_label = tk.Label(self.root, text="Category:")
        self.category = tk.Entry(self.root)
        
        #position elements in the grid and center the grid
        self.author_label.grid(row=1, column=0, pady=5)
        self.author_name.grid(row=1, column=1, pady=5)
        self.year_label.grid(row=2, column=0, pady=5)
        self.year.grid(row=2, column=1, pady=5)
        self.category_label.grid(row=3, column=0, pady=5)
        self.category.grid(row=3, column=1, pady=5)
        
        
        self.create_button("Search", self.new_search, relx=0.1, rely=0.9, anchor="center")  
        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")

    def new_search(self):
        author = self.author_name.get()
        year = self.year.get()
        category = self.category.get()
        
        criteria = {}
        
        if author:
            criteria['author'] = author
        if year:
            criteria['year'] = int(year)
        if category:
            criteria['category'] = category.split(' ')
            
        books = self.controller.search(criteria)
        
        if books:
            self.BooksDisplay(self.root, books).display_books()
        else:
            messagebox.showerror("Error", "No books found")
            
    def search_by_book_name(self):
        self.search_action("Book Name", "Search book by book name successfully", "Search book by book name fail")

    def search_by_author_name(self):
        self.search_action("Author Name", "Search book by author name successfully", "Search book by author name fail")

    def search_by_category(self):
        self.search_action("Category", "Search book by category successfully", "Search book by category fail")

    def search_by_year(self):
        self.search_action("Year", "Search book by year successfully", "Search book by year fail")

    def search_action(self, field_name, success_msg, fail_msg):
        self.clear_window()
        self.root.title(f"Search By {field_name}")

        tk.Label(self.root, text=f"Enter {field_name}:").pack(pady=10)
        self.search_field = tk.Entry(self.root)
        self.search_field.pack(pady=5)

        self.create_button("Enter", lambda: self.perform_search(success_msg, fail_msg), relx=0.1, rely=0.9, anchor="center")
        self.create_button("Home", self.init_main_menu, relx=0.9, rely=0.9, anchor="center")

    def perform_search(self, success_msg, fail_msg):
        if self.search_field.get():
            messagebox.showinfo("Success", success_msg)
        else:
            messagebox.showerror("Error", fail_msg)

    def add_book(self):
        try:
            int(self.book_year.get())
            int(self.book_copies.get())
        except:
            messagebox.showerror("Error", "year and copies most be numbers only")

        if self.book_name.get() and self.book_author.get()and self.book_year.get() and self.book_category.get() and self.book_copies.get():
            if self.controller.add_book(self.book_name.get(),self.book_author.get(),self.book_year.get(),self.book_category.get(),self.book_copies.get()):
                messagebox.showinfo("Success", "Book added successfully")
            else:
                messagebox.showerror("Error", "Book added fail")
        else:
            messagebox.showerror("Error", "fill al boxsez")

    def login(self):
        if self.username.get() and self.password.get():
            if self.controller.login(self.username.get(), self.password.get()):
                self.init_main_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Username and password are required")
            

    def register(self):
        if self.username.get() and self.password.get():
            self.controller.register(self.username.get(), self.password.get())
        else:
            messagebox.showerror("Error", "Username and password are required")
            
                
    def not_implemented(self):
        messagebox.showinfo("Info", "This feature is not implemented yet.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_error(self, message):
        messagebox.showerror("Error", message)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
