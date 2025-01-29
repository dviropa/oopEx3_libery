from  log import Log
class Observable:
    def __init__(self):
        self.observers = []  # רשימת ה-observers
        self.wait_list = {}  # רשימת המתנה לפי title
        self.logger = Log()  # מחלקה שתגדיר את הלוגים

    def subscribe(self, observer):
        """Add an observer to the subscription list."""
        self.observers.append(observer)

    def unsubscribe(self, observer):
        """Remove an observer from the subscription list."""
        self.observers.remove(observer)

    def notify(self, msg):
        """Notify all subscribed observers."""
        for obs in self.observers:
            obs.update(msg)

    def add_to_waitlist(self, title, observer):
        """Add an observer to the waitlist for a specific title."""
        if title not in self.wait_list:
            self.wait_list[title] = []
        self.wait_list[title].append(observer)

    def notify_waitlist(self, title):
        """Notify observers waiting for a specific title."""
        if title in self.wait_list and self.wait_list[title]:
            self.logger.log(f"Notify all waiting list clients for '{title}' that the book is available.")
            for user in self.wait_list[title]:
                user.update(f"Book '{title}' is available now.")
            # Clear the waitlist for the title
            self.wait_list[title] = []
        else:
            self.logger.log(f"No clients on the waiting list for '{title}'.")
