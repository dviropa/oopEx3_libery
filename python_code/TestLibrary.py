import unittest
import os
import pandas as pd
from Library import Library
from User import User


class TestLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.books_csv = "books.csv"
        cls.available_books_csv = "available_books.csv"
        cls.loaned_books_csv = "loaned_books.csv"
        cls.wait_list_csv = "wait_list.csv"

        # יצירת קובץ ספרים לדוגמה
        pd.DataFrame({
            "title": ["Book1", "Book2", "Book3"],
            "author": ["Author1", "Author2", "Author3"],
            "year": [2020, 2021, 2022],
            "category": ["Fiction", "Sci-Fi", "Fantasy"],
            "borrowed": [1, 2, 3],
            "copies": [3, 2, 5],
            "sum_borowd_amunt": [10, 5, 7]
        }).to_csv(cls.books_csv, index=False)
        # יצירת קובץ ספרים פנויים לדוגמה
        pd.DataFrame({
            "title": ["Book1", "Book2","Book3"],
            "amount": [2, 1, 5]
        }).to_csv(cls.available_books_csv, index=False)
        # יצירת קובץ ספרים מושאלים לדוגמה
        pd.DataFrame({
            "title": ["Book1", "Book2"],
            "user_name": ["User1", "User2"]
        }).to_csv(cls.loaned_books_csv, index=False)

        # יצירת קובץ רשימת המתנה לדוגמה
        pd.DataFrame({
            "title": ["Book3"],
            "user_name": ["User3"]
        }).to_csv(cls.wait_list_csv, index=False)
        cls.library = Library()
        cls.library.init_books(
            cls.books_csv,
            cls.loaned_books_csv,
            cls.available_books_csv,
            cls.wait_list_csv
        )



    @classmethod
    def tearDownClass(cls):
        # מחיקת קבצים לאחר הבדיקות
        os.remove(cls.books_csv)
        os.remove(cls.available_books_csv)
        os.remove(cls.loaned_books_csv)
        os.remove(cls.wait_list_csv)

    def setUp(self):
        self.library = Library()
        self.library.init_books(
            self.books_csv,
            self.loaned_books_csv,
            self.available_books_csv,
            self.wait_list_csv
        )
    def test_return_book(self):

        user = User("User1")
        self.library.add_book("Book4", "Author4", 2023, "Drama", 2)
        self.library.loan_book("Book4", user)
        result = self.library.return_book("Book4", user)
        self.assertTrue(result)
    def test_add_book(self):
        self.library.add_book("Book4", "Author4", 2023, "Drama", 2)
        self.assertIn("Book4", self.library.lib_books)

    def test_remove_book_copy(self):
        self.library.add_book("Book1", "Author1", 2020, "Fiction", 1)
        self.library.remove_book_copy("Book1")
        self.assertEqual(len(self.library.lib_books["Book1"][2]), 3)

    def test_loan_book(self):
        user = User("User1")
        result = self.library.loan_book("Book1", user)
        self.assertTrue(result)



    def test_top10_popular_books(self):
        popular_books = self.library.top10_popular_books()
        self.assertEqual(len(popular_books), 3)
        self.assertEqual(popular_books[0], "Book1")

    def test_top10_and_waiting_list(self):
        combined = self.library.top10_and_waiting_list()
        self.assertIn("Book3", combined)
        self.assertIn("Book1", combined)

    def test_update_book(self):
        self.library.update_book("Book1", "UpdatedBook1", "NewAuthor", 2025, "Drama")
        self.assertIn("UpdatedBook1", self.library.lib_books)
        updated_book = self.library.lib_books["UpdatedBook1"][0]
        self.assertEqual(updated_book.author, "NewAuthor")
        self.assertEqual(updated_book.year, 2025)
        self.assertEqual(updated_book.category, "Drama")

    def test_waiting_list(self):
        user = User("User3")
        self.library.loan_book("Book3", user)
        self.assertIn("Book3", self.library.wait_list)


if __name__ == "__main__":
    unittest.main()
