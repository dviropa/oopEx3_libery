import hashlib
import uuid

import pandas as pd
from User import User


class Authinactor:
    def __init__(self):
        self.logged_users = {}
        self.users = {}
        self.read_users_from_csv()


    def __load_csv(self):
        try:
            return pd.read_csv("users.csv")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=[ "name", "hashed_password"])
            return df

    def read_users_from_csv(self):
        df = self.__load_csv()
        if not df.empty:
            self.logged_users = {user_name: False for user_name in df["name"].tolist()}
            self.users = {
                user_name: hashed_password
                for user_name, hashed_password in zip(df["name"].tolist(), df["hashed_password"].tolist())
            }

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self ,user_name, password: str):
        if user_name in self.logged_users:
            raise ValueError("User already exists")
        self.logged_users[user_name] = False
        self.users[user_name] = self.hash_password(password)
        self.update_file(user_name, password)

    def update_file(self, user_name, password):
        df = self.__load_csv()
        new_row = {"name": user_name, "hashed_password": self.hash_password(password)}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("users.csv", index=False)




    def login(self, user_name, password: str):
        if user_name not in self.users or user_name not in self.logged_users:
            return False
        if self.hash_password(password) == self.users[user_name]:
            self.logged_users[user_name] = True
            return True
        return False


    def logout(self, user_name):
        if self.logged_users[user_name]:
            self.logged_users[user_name] = False
            return True
        return False



    def isLoggedIn(self, user_name):
        return self.logged_users[user_name]
