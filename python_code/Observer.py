class Observer:
    def __init__(self):
        self.notification = []

    def update(self, msg):
        self.notification.append(msg)
        print(f"Notification added: {msg}")
