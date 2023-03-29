from tkinter import *


class RunSimulation:
    def __init__(self, root):
        self.canvas = Canvas(root, width=798, height=462)
        self.canvas.config(background="snow2")
        self.canvas.place(x=512, y=288, anchor="center")
        self.canvas.focus_set()

def startGraphics():
    root = Tk()
    root.title("Air Nav")
    root.geometry("1024x576")
    root.resizable(width=False, height=False)
    root.configure(bg="gold")

    titleLabel = Label(root, bg="gold", text="Air Nav", font=("Harlow Solid Italic", 100))
    titleLabel.place(x=512, y=150, anchor="center")
    authorLabel = Label(root, bg="gold", text="Designed by Arjun, Rohan, Hadi & Azlan", font=("Dubai Light", 28))
    authorLabel.place(x=512, y=250, anchor="center")

    startButton = Button(root, text="Start", borderwidth=10, bg="gold", width=15, font=("Helvetica", 16, "bold"), command=lambda: RunSimulation(root))
    startButton.place(x=367, y=420, anchor="center")

    quitButton = Button(root, text="Quit", borderwidth=10, bg="gold",  width=15, font=("Helvetica", 16, "bold"), command=lambda: root.destroy())
    quitButton.place(x=642, y=420, anchor="center")

    mainloop()


if __name__ == '__main__':
    startGraphics()
