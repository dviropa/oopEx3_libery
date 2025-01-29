import pandas as pd
from abc import ABC, abstractmethod

# ---------------- Strategy Interface ------------------
class SearchStrategy(ABC):
    @abstractmethod
    def apply(self, books_df, criteria):
        pass

# ---------------- Concrete Strategies ------------------
class FilterByCriteria(SearchStrategy):
    def apply(self, books_df, criteria):
        # לולאה דרך כל הקריטריונים וביצוע סינון
        for key, value in criteria.items():
            if key == "category":
                books_df = books_df[books_df[key].isin(value)]  # קטגוריות - רשימה
            else:
                books_df = books_df[books_df[key] == value]    # ערכים בודדים
        return books_df


class FilterByAuthor(SearchStrategy):
    def apply(self, books_df, author):
        if author:
            return books_df[books_df["author"]==author["author"]]
        return books_df
    
class FilterByYear(SearchStrategy):
    def apply(self, books_df, year):
        if year:
            return books_df[books_df["year"]==year["year"]]
        return books_df

class FilterByGenres(SearchStrategy):
    def apply(self, books_df, categories=None):
        if categories:
            return books_df[books_df["category"].isin(categories['categories'])]
        return books_df

class SortBy(SearchStrategy):
    def apply(self, books_df, key=None, reverse=False):
        if key:
            return books_df.sort_values(by=key, ascending=not reverse)
        return books_df

# ---------------- Search Class ------------------
class Search:
    def __init__(self, books_df: pd.DataFrame):
        """
        books_df: DataFrame שמכיל את המידע על הספרים.
        """
        self.books_df = books_df.copy()
        self.filtered_books_df = self.books_df

    def apply_strategy(self, strategy: SearchStrategy, **kwargs):
        # במקום לפרק את הקריטריונים, העבר אותם כפרמטר יחיד
        self.filtered_books_df = strategy.apply(self.filtered_books_df, kwargs)
        return self

    def get_results(self):
        """
        מחזיר את התוצאות המסוננות כ-DataFrame.
        """
        return self.filtered_books_df


# data = {
#     "title": ["Book A", "Book B", "Book C", "Book D"],
#     "author": ["Author 1", "Author 2", "Author 1", "Author 3"],
#     "genre": ["Fiction", "Science", "Fiction", "History"],
#     "year": [2000, 1999, 2005, 2010],
#     "copies": [3, 5, 2, 4]
# }

# books_df = pd.DataFrame(data)
# search = Search(books_df)
# results = (
#     search
#     .apply_strategy(FilterByAuthor(), author=["Author 1"])  # סינון לפי מחבר
#     .apply_strategy(FilterByGenres(), genres=["Fiction"])  # סינון לפי ז'אנר
#     .apply_strategy(SortBy(), key="year", reverse=False)  # מיון לפי שנה (בסדר עולה)
#     .get_results()
# )

# print(results)