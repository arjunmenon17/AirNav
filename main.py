from tkinter import *
from typing import Any
import data as dt
from network import FlightNetwork

def create_frame(self, root: Any, network) -> None:
    """
    To Do: Docstring
    """
    root.destroy()
    root = Tk()
    root.title("Air Nav")
    root.geometry("1024x576")
    root.resizable(width=False, height=False)
    root.configure(bg="gold")
    e1 = Entry(root, width=15, font=("Helvetica", 16, "bold"))
    e1.place(x=512, y=150, anchor="center")
    l1 = Label(root, bg="gold", text="Origin Airport", font=("Helvetica", 16, "bold"))
    l1.place(x=512, y=100, anchor="center")

    e2 = Entry(root, width=15, font=("Helvetica", 16, "bold"))
    e2.place(x=512, y=350, anchor="center")
    l2 = Label(root, bg="gold", text="Destination Airport", font=("Helvetica", 16, "bold"))
    l2.place(x=512, y=250, anchor="center")

    start_button = Button(root, text="Start", borderwidth=10, bg="gold", width=15, font=("Helvetica", 16, "bold"), command=lambda: network.find_shortest_route(e1.get(), e2.get()))
    start_button.place(x=367, y=420, anchor="center")



    mainloop()

def start_graphics(network) -> None:
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

    start_button = Button(root, text="Start", borderwidth=10, bg="gold", width=15, font=("Helvetica", 16, "bold"), command=lambda: create_frame(root, network))
    start_button.place(x=367, y=420, anchor="center")

    quit_button = Button(root, text="Quit", borderwidth=10, bg="gold",  width=15, font=("Helvetica", 16, "bold"), command=lambda: root.destroy())
    quit_button.place(x=642, y=420, anchor="center")

    mainloop()


if __name__ == '__main__':
    network = FlightNetwork()
    start_graphics(network)
