from tkinter import *
from typing import Any


class RunSimulation:
    """
    To Do: Class Description
    Instance Attributes:
        - root:
    """
    def __init__(self, root: Any) -> None:
    	"""
    	To Do: Docstring
    	"""
        # self.canvas = Canvas(root, width=798, height=462)
        # self.canvas.config(background="snow2")
        # self.canvas.place(x=512, y=288, anchor="center")
        # self.canvas.focus_set()

def startGraphics() -> None:
    """
    To Do: Docstring
    """
    root = Tk()
    root.title("Air Nav")
    root.geometry("1024x576")
    root.resizable(width=False, height=False)
    root.configure(bg="gold")

    title_label = Label(root, bg="gold", text="Air Nav", font=("Harlow Solid Italic", 100))
    title_label.place(x=512, y=150, anchor="center")
    author_label = Label(root, bg="gold", text="Designed by Arjun, Rohan, Hadi & Azlan", font=("Dubai Light", 28))
    author_label.place(x=512, y=250, anchor="center")

    start_button = Button(root, text="Start", borderwidth=10, bg="gold", width=15, font=("Helvetica", 16, "bold"), command=lambda: RunSimulation(root))
    start_button.place(x=367, y=420, anchor="center")

    quit_button = Button(root, text="Quit", borderwidth=10, bg="gold",  width=15, font=("Helvetica", 16, "bold"), command=lambda: root.destroy())
    quit_button.place(x=642, y=420, anchor="center")

    mainloop()


if __name__ == '__main__':
    startGraphics()
