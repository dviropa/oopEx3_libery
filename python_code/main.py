import tkinter as tk
from Controller import Controller
from Library import Library
from gui import LibraryGUI

if __name__ == "__main__":
    library = Library()
    root = tk.Tk()
    gui = LibraryGUI(root)
    controller = Controller(library, gui)
    root.mainloop()