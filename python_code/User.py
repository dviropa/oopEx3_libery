from Observer import Observer


class User(Observer):
    def __init__(self, name):
        super().__init__()

        self.name = name

    def get_name(self):
        return self.name