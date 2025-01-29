import unittest
import pandas as pd
import os
import hashlib
from Authinactor import Authinactor


class TestAuthinactor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a dummy CSV file for testing
        cls.users_csv = "users.csv"
        pd.DataFrame({
            "name": ["Dvir", "Harel", "ETL"],
            "hashed_password": [
                hashlib.sha256("password".encode()).hexdigest(),
                hashlib.sha256("qwerty".encode()).hexdigest(),
                hashlib.sha256("abc123".encode()).hexdigest()
            ]
        }).to_csv(cls.users_csv, index=False)

    @classmethod
    def tearDownClass(cls):
        # Delete the dummy CSV file after tests
        os.remove(cls.users_csv)

    def setUp(self):
        # Recreate the CSV file before each test
        pd.DataFrame({
            "name": ["Dvir", "Harel", "ETL"],
            "hashed_password": [
                hashlib.sha256("password".encode()).hexdigest(),
                hashlib.sha256("qwerty".encode()).hexdigest(),
                hashlib.sha256("abc123".encode()).hexdigest()
            ]
        }).to_csv("users.csv", index=False)
        self.auth = Authinactor()

    def test_read_users_from_csv(self):
        self.assertEqual(len(self.auth.logged_users), 3)
        self.assertIn("Dvir", self.auth.logged_users)

    def test_register_new_user(self):
        self.auth.register("David", "newpassword")
        self.assertIn("David", self.auth.logged_users)
        self.assertEqual(
            self.auth.users["David"],
            self.auth.hash_password("newpassword")
        )

    def test_login_success(self):
        self.assertTrue(self.auth.login("Dvir", "password"))

    def test_login_failure(self):
        self.assertFalse(self.auth.login("Dvir", "wrongpassword"))

    def test_logout(self):
        self.auth.login("Dvir", "password")
        self.assertTrue(self.auth.logout("Dvir"))
        self.assertFalse(self.auth.isLoggedIn("Dvir"))

    def test_update_file(self):
        self.auth.register("David", "securepass")
        df = pd.read_csv("users.csv")
        self.assertIn("David", df["name"].tolist())


if __name__ == "__main__":
    unittest.main()
