from __future__ import annotations
from tkinter import *
from typing import Any
import data as dt


def update(data):
    my_list.delete(0, END)

    for item in data:
        my_list.insert(END, str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + ", " + str(item[3]))
    

def fillout(event):
    my_entry.delete(0, END)
    my_entry.insert(0, my_list.get(ANCHOR))

def check(event, airports):
    typed = my_entry.get()
    if typed == '':
        data = airports
    else:
        data = []
        for item in airports:
            if typed.lower() in item[0].lower() or typed.lower() in item[1].lower() or typed.lower() in item[2].lower() or typed.lower() in item[3].lower():
                data.append(item)

    update(data)

# if __name__ == '__main__':
root = Tk()
my_label = Label(root, text="Search Airport...", font=("Helvetica, 14"), fg="grey")
my_label.pack(pady=20)
my_entry = Entry(root, font=("Helvetica", 20))
my_entry.pack()

airports = dt.get_airports()

var = Variable(value=[str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + ", " + str(item[3]) for item in dt.get_airports()])
my_list = Listbox(root, listvariable=var, height=6, selectmode=EXTENDED)
my_list.pack(fill=BOTH, expand=True)

my_list.bind("<<ListboxSelect>>", func=lambda e: fillout(e))
my_entry.bind("<KeyRelease>", func=lambda e, arg=dt.get_airports(): check(e, arg))

