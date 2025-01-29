class Log:
    def __init__(self):
        # אפשר להשאיר ריק אם אין צורך באתחול משתנים
        pass

    def log(self,content, file_name="log.txt"):
        """
        כותב תוכן לקובץ לוג.
        :param file_name: str - שם קובץ הלוג (ברירת מחדל "log.txt")
        :param content: str - התוכן לכתיבה
        """
        try:
            with open(file_name, "a", encoding="utf-8") as file:
                file.write(content + "\n")  # הוספת תוכן עם שורה חדשה
            print(f"Successfully wrote to {file_name}")
        except Exception as e:
            print(f"Failed to write to {file_name}: {e}")
