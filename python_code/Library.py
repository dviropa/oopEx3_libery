from Book import Book
import pandas as pd
from Observable import Observable
from Authinactor import Authinactor
from User import User
from log import Log
import json
from Search import Search , FilterByYear , FilterByAuthor , FilterByGenres , SortBy , FilterByCriteria , FilterByAuthor
from Book import BorrowedBook

class Library(Observable):

    def __init__(self):
        super().__init__()
        self.lib_books: dict = {}  # dict{title : (book,dict{book_id,(bool,user)})}
        self.wait_list: dict = {}
        self.auth_system: Authinactor = Authinactor()
        self.logger = Log()
        self.init_books()

    def parse_books_df(self, books_df):
        try:
            for _, row in books_df.iterrows():
                # book = Book(row["title"], row["author"], row["year"], row["category"])
                book_a=BorrowedBook(row["title"], row["author"], row["year"], row["category"],row["borrowed"])
                self.lib_books[row["title"]] = (book_a,{i: (False, None) for i in range(row["copies"])})
                # self.lib_books[row["title"]] = (book, row["borrowed"], {i: (False, None) for i in range(row["copies"])})
            self.logger.log(f"load book list succcessfully")
            return self.lib_books
        except:
            self.logger.log(f"load book failed")
            return None

    def parse_loaned_df(self, loaned_books_file):
        try:
            i = 0
            for _, row in loaned_books_file.iterrows():
                title = row["title"]
                if title in self.lib_books.keys():
                    user_name = row["user_name"]
                    # self.lib_books[title][2][i] = (True, user_name)
                    self.lib_books[title][1][i] = (True, user_name)

                    i += 1
            self.logger.log(f"load loaned book list succcessfully")
        except:
            self.logger.log(f"load loaned book failed")



    # def parse_wait_list_df(self, wait_list_file):
    #     try:
    #         for _, row in wait_list_file.iterrows():
    #             title = row["title"]
    #             if title not in self.wait_list:
    #                 self.wait_list[title] = []
    #             # user_name = row["user_name"]
    #             user_name = str(row["user_name"])
    #             self.wait_list[title].append(user_name)
    #         self.logger.log(f"load whiting list succcessfully")
    #     except:
    #         self.logger.log(f"load whiting list failed")
    def parse_wait_list_df(self, wait_list_file):
        try:
            if "title" not in wait_list_file.columns or "user_list" not in wait_list_file.columns:
                raise ValueError("Invalid DataFrame structure. Required columns: 'title', 'user_list'.")

            self.wait_list = {}

            for _, row in wait_list_file.iterrows():
                title = row["title"]
                user_list = row["user_list"]


                if isinstance(user_list, str):
                    user_list = eval(user_list)
                elif not isinstance(user_list, list):
                    raise ValueError(f"Invalid user_list format for title '{title}'.")


                self.wait_list[title] = user_list

            self.logger.log("Waiting list loaded successfully.")
        except ValueError as e:
            self.logger.log(f"Waiting list parsing failed: {e}")
        except Exception as e:
            self.logger.log(f"Unexpected error while loading waiting list: {e}")

    def init_books(self, books_file="books.csv", loaned_books_file="loanded_books.csv",
                   available_books_file="available_books.csv", wait_list_file="wait_list.csv"):
        self.books_file = books_file
        self.loaned_books_file = loaned_books_file
        self.available_books_file = available_books_file
        self.wait_list_file = wait_list_file

        books_df = self.__load_csv(books_file)

        self.lib_books = self.parse_books_df(books_df)

        loaned_books_df = self.__load_csv(loaned_books_file)

        self.parse_loaned_df(loaned_books_df)

        wait_list_df = self.__load_csv(wait_list_file)

        self.parse_wait_list_df(wait_list_df)

    def __update_books_csv(self, title, author=None, year=None, category=None, filename="books.csv"):
        try:
            df : pd.DataFrame = self.__load_csv(filename)
            print("__________________________")
            # dict{title,(book,sum_borowd_amunt,dict{book_id,(bool,user)})}
            if author==None or year==None or category==None:
                # df.loc[df["title"] == title, "copies"] = len(self.lib_books[title][2])
                df.loc[df["title"] == title, "copies"] = len(self.lib_books[title][1])
                df.loc[df["title"] == title, "borrowed"] = self.lib_books[title][0].get_borrowed_times()

                print("IFFFFFFFF")
            elif title not in df["title"].values:
                print("ELSE")
                new_row = {
                    "title": title,
                    "author": author if author else "Unknown",
                    "year": year if year else "Unknown",
                    "category": category if category else "Unknown",
                    # "copies": len(self.lib_books[title][2]) if title in self.lib_books else 0,
                    "copies": len(self.lib_books[title][1]) if title in self.lib_books else 0,
                    "borrowed":0
                }
                print(new_row)
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            else:
                df.loc[df["title"] == title, "borrowed"] = self.lib_books[title][0].get_borrowed_times()
                df.loc[df["title"] == title, "copies"] = len(self.lib_books[title][1])

    
            
            df.to_csv(filename, index=False)
            self.logger.log(f"updated {filename} successfully")

        except:
            print("Error")
            self.logger.log(f"updating {filename} has failed")


    def __update_available_csv(self, title, amount, filename="available_books.csv"):
        try:
            df = self.__load_csv(filename)
            if title in df["title"].values:
                if df.loc[df["title"] == title, "amount"] ==0 and amount < 0:
                    raise RuntimeError("No available copies to remove")
                df.loc[df["title"] == title, "amount"] += amount
            else:
                if amount > 0:
                    new_row = {"title": title, "amount": amount}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    raise RuntimeError("No available copies to remove")
            df.to_csv(filename, index=False)
            self.logger.log(f"apdete {filename} succcessfully")

        except:
            self.logger.log(f"updating {filename}  has failed")

    def __update_loaned_csv(self, title, user_name, amount, filename="loanded_books.csv"):
        try:
            df = self.__load_csv(filename)

            if amount > 0:  # הוספת רשומה חדשה
                new_row = pd.DataFrame([{"title": title, "user_name": user_name}])
                df = pd.concat([df, new_row], ignore_index=True)
                # print(df)
            else:  # הסרת רשומה קיימת
                if ((df["title"] == title) & (df["user_name"] == user_name)).any():
                    index_to_drop = df[(df["title"] == title) & (df["user_name"] == user_name)].index[0]
                    df = df.drop(index_to_drop)
                else:
                    raise RuntimeError("No available copies to remove")

            df.to_csv(filename, index=False)
            self.logger.log(f"apdete {filename} succcessfully")
        except:
            self.logger.log(f"apdete {filename} failed loading")

    # def __update_waiting_list_csv(self, title, user_name, action, filename="wait_list.csv"):
    #     df = self.__load_csv(filename)
    #     if action == "remove":
    #         if (((df["title"].astype(str) == title) & (df["user_name"].astype(str) == user_name)).any()):
    #             df = df.drop(df[(df["title"].astype(str) == title) & (df["user_name"].astype(str) == user_name)].index)
    #         else:
    #             raise RuntimeError("No available copies to remove from whiting list")
    #     else:
    #         new_row = pd.DataFrame([{"title": title, "user_name": user_name}])
    #         df = pd.concat([df, new_row], ignore_index=True)
    #     df.to_csv(filename, index=False)

    def __update_waiting_list_csv(self, title, user_name, action, filename="wait_list.csv"):
        try:
            df = self.__load_csv(filename)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["title", "user_list"])

        # הפיכת עמודת user_list למבנה של רשימה
        if not df.empty:
            df["user_list"] = df["user_list"].apply(lambda x: eval(x) if isinstance(x, str) else x)

        # טיפול בפעולה
        if action == "remove":
            # בדיקה אם הספר קיים
            if title in df["title"].values:
                index = df[df["title"] == title].index[0]
                users = df.at[index, "user_list"]
                if user_name in users:
                    # הסרת המשתמש מהרשימה
                    users.remove(user_name)
                    if not users:
                        df = df.drop(index)
                    else:
                        df.at[index, "user_list"] = users
                else:
                    raise RuntimeError(f"User '{user_name}' not found in the waiting list for book '{title}'.")
            else:
                raise RuntimeError(f"Book '{title}' not found in the waiting list.")
        else:
            if title in df["title"].values:
                index = df[df["title"] == title].index[0]
                users = df.at[index, "user_list"]
                if user_name not in users:
                    users.append(user_name)
                    df.at[index, "user_list"] = users
            else:
                new_row = {"title": title, "user_list": [user_name]}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df["user_list"] = df["user_list"].apply(str)  # המרה למחרוזת לשמירה בקובץ
        df.to_csv(filename, index=False)

    def __load_csv(self, filename):
        try:
            _=pd.read_csv(filename)
            self.logger.log(f"open {filename} succcessfully loaded")
            return _
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.logger.log(f"not abele to open {filename}")
            return pd.DataFrame()

    def add_book(self, title, author, year, category, copies=1):

        if title in self.lib_books:
            book_a = self.lib_books[title][0]
            try:
                assert book_a.get_author() == author, "book added fail, Author mismatch"
                assert book_a.get_year() == year, "book added fail, Year mismatch"
                assert book_a.get_categories() == category, "book added fail, Category mismatch"
            except AssertionError as e:
                self.logger.log(str(e))
            if copies < 0:
                self.logger.log(f"add book fail")
                raise RuntimeError("No copies to add copies is smoler then 0")
            while copies != 0:
                copies -= 1
                self.add_book_copy(title)
        else:
            # book = Book(title, author, year, category)
            book_a=BorrowedBook(title, author, year, category,copies)
            self.lib_books[title] = (
                book_a, {i: (False, None) for i in range(copies)})  # book and empty dictionary for borrowed books
            self.logger.log(f"a new book {title} has been added")
            # self.lib_books[title] = (
            #     book, 0, {i: (False, None) for i in range(copies)})  # book and empty dictionary for borrowed books
            # self.logger.log(f"a new book {title} has been added")
            # self.notify(f"book added successfully")
            # עדכון קובץ ספרים וספרים פנויים
        self.__update_books_csv(title, author, year, category)
        self.__update_available_csv(title, copies)

    def remove_books(self, title):
        # if book is not borrowd
        try:
            if not self.is_book_valid(title):
                raise RuntimeError("Book not found")
            num_copis = len(self.lib_books[title][1])
            for i in range(len(self.lib_books[title][1])):
                num_copis -= 1
                self.remove_book_copy(title)
            if num_copis == 0:
                self.__delete_book(title,"books.csv")
                if title in self.lib_books:
                    del self.lib_books[title]
                self.__delete_book(title,"available_books.csv")
                self.logger.log(f"book removed successfully")
            else:

                self.logger.log(f"book removed fail - ther ar sum books that ar boroed")
        except RuntimeError:
            self.logger.log(f"book removed fail")
            return False

    def __delete_book(self, title, file_name):
        df = self.__load_csv(file_name)
        df = df[df["title"] != title]

        df.to_csv(file_name, index=False)
    def remove_book_copy(self, title):
        index = self.first_available_copy(title)
        if index is not None:
            del self.lib_books[title][1][index]
            self.logger.log(f"removing one copy of {title} copy number {index} successfully ")

            self.__update_books_csv(title)
            self.__update_available_csv(title, -1)

        else:
            self.logger.log("Eror: No available copies")
            raise RuntimeError("No available copies to remove")

    def add_book_copy(self, title):
        index = len(self.lib_books[title][1])
        self.lib_books[title][1][index] = (False, None)
        self.logger.log(f"aded a new copy of {title}  copy number {index}")

        # עדכון קובץ ספרים וספרים פנויים
        self.__update_books_csv(title)
        self.__update_available_csv(title, 1)

    def loan_book(self, title, user_name):
        try:

            index = self.first_available_copy(title)
            if index is None:
                if user_name not in self.wait_list[title]:
                    self.add_to_waitlist( title, user_name)
                    self.logger.log(f"add user :{user_name} to {title} waiting list")
                    self.__update_waiting_list_csv(title, user_name, "append")
                self.logger.log(f"book borrowed fail - there are no available copies")
                return False
            if title in self.wait_list and isinstance(self.wait_list[title], list) and len(
                    self.wait_list[title]) > 0 and user_name in self.wait_list[title]:
                self.wait_list[title].remove(user_name)
                if len(self.wait_list[title]) == 0:
                    del self.wait_list[title]
                self.logger.log(f"User '{user_name}' removed from waiting list of book '{title}'.")
                self.__update_waiting_list_csv(title, user_name, "remove")
            self.lib_books[title][1][index] = (True, user_name)

            self.lib_books[title][0].increment_borrowed_times()

            self.lib_books[title] = (self.lib_books[title][0], self.lib_books[title][1])

            self.logger.log(f"book borrowed successfully - user :{user_name} borrowed {title}")

            self.__update_books_csv(title)
            self.__update_available_csv(title, -1)
            self.__update_loaned_csv(title, user_name, 1)
            return True

        except ValueError as e:
            self.logger.log(f"book borrowed fail")
            print(e.args[0])
            return False

    def return_book(self, title, user_name):
        try:
            index = self.user_borrowed_book(title, user_name)
            print(index)
            if index is None:
                raise ValueError("book returned fail - User has not borrowed this book")
            self.logger.log(f"book returned successfully - user:{user_name} returned {title}")
            self.lib_books[title][1][index] = (False, None)

            # עדכון קובץ ספרים וספרים פנויים וספרים מושאלים
            self.__update_books_csv(title)
            self.__update_available_csv(title, 1)
            self.__update_loaned_csv(title, user_name, -1)  # הוספת שם המשתמש וערך הכמות הנכון
            # self.__update_waiting_list_csv(title, user_name, "remove")
            self.notify_waitlist(title)

            return True
        except ValueError as e:
            print(e.args[0])
            return False

    # def notify_waitlist(self, title):
    #     if title in self.wait_list and self.wait_list[title]:
    #         self.logger.log(f"Notify all waiting list clients for '{title}' that the book is available.")
    #         for user in self.wait_list[title]:
    #             user.update(f"Book '{title}' is available now.")
    #     else:
    #         self.logger.log(f"No clients on the waiting list for '{title}'.")
    def add_to_waitlist(self, title, user_name: str):
        """Add a username (string) to the waitlist for a specific title."""
        if title not in self.wait_list:
            self.wait_list[title] = []
        if user_name not in self.wait_list[title]:  # לוודא שאין כפילויות
            self.wait_list[title].append(user_name)

    def notify_waitlist(self, title):
        """Notify users (strings) waiting for a specific title."""
        if title in self.wait_list and self.wait_list[title]:
            self.logger.log(f"Notify all waiting list clients for '{title}' that the book is available.")
            for user_name in self.wait_list[title]:  # משתמשים כ-strings
                # כאן ניתן להחליף את ההודעה ללוג או מערכת אחרת
                print(f"Notification sent to {user_name}: Book '{title}' is available now.")
            # Clear the waitlist after notification
            self.wait_list[title] = []
        else:
            self.logger.log(f"No clients on the waiting list for '{title}'.")

    def first_available_copy(self, title):
        if title not in self.lib_books:
            raise ValueError("Book not found")
        for i in range(len(self.lib_books[title][1])-1,-1,-1):
            if not self.lib_books[title][1][i][0]:
                return i
        return None

    def update_book(self, title, new_title, author, year, category):
        df = self.__load_csv("books.csv")
        if title not in df["title"].values and title not in self.lib_books:
            self.logger.log(f"Error: Book '{title}' not found. cenot updete it")
            raise ValueError(f"Book '{title}' not found in the library. cenot updete it")

        df.loc[df["title"] == title, "author"] = author
        df.loc[df["title"] == title, "year"] = year
        df.loc[df["title"] == title, "category"] = category
        df.loc[df["title"] == title, "title"] = new_title
        df.to_csv("books.csv", index=False)

        book = self.lib_books.pop(title)
        book[0].title = new_title
        book[0].author = author
        book[0].year = year
        book[0].category = category
        self.lib_books[new_title] = book

        self.logger.log(
            f"Updated book '{title}' to '{new_title}' with author='{author}', year={year}, category='{category}'.")


    def register_new_user(self, user_name, password):
        try:
            self.auth_system.register( user_name, password)
            self.logger.log(f"register new user:{user_name} ")
            return True
        except ValueError as e:
            self.logger.log(f"user:{user_name} alredy regesterd")
            return False


    def user_login(self, user_name, password):
        if self.auth_system.login(user_name, password):
            self.logger.log(f"----------------------------")
            self.logger.log(f"user:{user_name} login successful")
            return True

        else:
            self.logger.log(f"user:{user_name}failde to login")
            return False


    def user_logout(self, user_name):
        if self.auth_system.logout(user_name):
            self.logger.log(f"user:{user_name} logout")
            self.logger.log(f"----------------------------")
        else:
            self.logger.log(f"user:{user_name}failde to logout")


    def is_book_valid(self, title):
        if title in self.lib_books.keys():
            return True

        return False


    def user_borrowed_book(self, title, user_name):
        print("        user_borrowed_book        ",self.lib_books[title][1])
        if not self.is_book_valid(title):
            raise ValueError("Book not found")
        for i in range(len(self.lib_books[title][1])):
            if self.lib_books[title][1][i] ==(True, user_name):
                return i
        print("     should not get here")
        return None

    def top10_popular_books(self):
        try:
            books_df = self.__load_csv("books.csv")

            if "sum_borowd_amunt" not in books_df.columns:
                books_df["sum_borowd_amunt"] = 0  # הוספת העמודה החסרה

            books_df = books_df.sort_values(by="sum_borowd_amunt", ascending=False).head(10)
            popular_titles = books_df["title"].tolist()
            self.logger.log(f"Display top 10 popular books")
            return popular_titles
        except:
            self.logger.log(f"failed to Display top 10 popular books")
            return None



    def get_books_in_waiting_list(self):
        try:
            seen = set()  # לשמירת שמות שכבר נמצאו
            wait_list_titles = []
            for title in self.wait_list.keys():
                if title not in seen:
                    wait_list_titles.append(title)
                    seen.add(title)

            # לוג על הצלחה
            self.logger.log(f"Display waiting list")
            return wait_list_titles
        except:
            self.logger.log(f"failed to Display waiting list")
            return None

    def top10_and_waiting_list(self):
        try:
            combined_titles = self.top10_popular_books() + [
                title for title in self.get_books_in_waiting_list()
                if title not in self.top10_popular_books()
            ]
            self.logger.log(f"Display top 10 popular books and waiting list")
            return combined_titles
        except:
            self.logger.log(f"failed to top 10 popular books and waiting list")
            return None


    def get_books(self):# dict{title,(book,sum_borowd_amunt,dict{book_id,(bool,user)})}
        self.logger.log(f"Display all books")
        return {title: (book_data[0],len(book_data[1])) for title, book_data in self.lib_books.items()}
    # dict{title: (book,len(books)}

    def get_available_books(self):# dict{title,(book,sum_borowd_amunt,dict{book_id,(bool,user)})}
        self.logger.log(f"Display available books")
        return {title: (book_data[0], copies) for title, book_data in self.lib_books.items() if (copies := sum(1 for _ , val in book_data[1].items() if val[0] == False)) > 0}

    def get_borrowed_books(self):# dict{title,(book,sum_borowd_amunt,dict{book_id,(bool,user)})}
        self.logger.log(f"Display borrowed books")
        return {title: (book_data[0], copies) for title, book_data in self.lib_books.items() if (copies := sum(1 for _ , val in book_data[1].items() if val[0] == True)) > 0}

    def search(self, criteria):
        # טוען את DataFrame
        books_df = pd.read_csv("books.csv")
        search_obj = Search(books_df)

        if len(criteria) > 1:
            # אסטרטגיית חיפוש לפי מספר פרמטרים
            search_obj.apply_strategy(FilterByCriteria(), **criteria)
        elif len(criteria) == 1:
            # אסטרטגיית חיפוש לפי פרמטר יחיד
            key = list(criteria.keys())[0]
            value = criteria[key]
            print(f"Key: {key}, Value: {value}")
            if key == "year":
                print("Applied FilterByYear")
                search_obj.apply_strategy(FilterByYear(), year=value)
            elif key == "author":
                search_obj.apply_strategy(FilterByAuthor(), author=value)
            elif key == "category":
                search_obj.apply_strategy(FilterByGenres(), categories=value)
            else:
                self.logger.log(f"Unknown search key: {key}")
                return pd.DataFrame()  # מחזיר DataFrame ריק במקרה של מפתח לא ידוע
        else:
            # במקרה של קריאה ללא פרמטרים
            self.logger.log("No search criteria provided.")
            return pd.DataFrame()

        # החזרת תוצאות
        results = search_obj.get_results()
        if results.empty:
            self.logger.log("No matching books found.")
        return results

# TODO - Read available books from available_books.csv
# TODO - Check connection to controller for MVC pattern.
