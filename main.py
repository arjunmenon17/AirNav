"""CSC111 Winter 2023 Course Project: AirNav 

Module Information: main.py
=============================== 
 
This Python module contains the data parsing functions for building dataframes of
the flight network's data and export functions for this data to be used in other
parts of the program such as the GUI and the network module.

Copyright and Usage Information 
=============================== 
 
This file is provided solely for the submission of the CSC111 Course Project and to be
used by instructors and TAs while marking and assessing this project.
 
This file is Copyright (c) 2023 Arjun Menon, Azlan Naeem, Hadi Naqvi, and Rohan Regi. 
"""
from __future__ import annotations
from tkinter import *
from typing import Any
import data as dt
import network


def update(data):
    """""
    Handler function that updates first list box on event
    """
    my_list.delete(0, END)

    for item in data:
        my_list.insert(END, str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + ", " + str(item[3]))

def update2(data):
    """""
    Handler function that updates second list box on event
    """
    my_list2.delete(0, END)

    for item in data:
        my_list2.insert(END, str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + ", " + str(item[3]))
    

def fillout(e):
    """
    Handler function to update first entry box with every listbox click
    """
    my_entry.delete(0, END)
    my_entry.insert(0, my_list.get(ANCHOR))

def fillout2(e):
    """
    Handler function to update second entry box with every listbox click
    """
    my_entry2.delete(0, END)
    my_entry2.insert(0, my_list2.get(ANCHOR))

def check(e, airports):
    """
    Handler function to check entry in first textbox vs listbox
    """
    typed = my_entry.get()
    if typed == '':
        data = airports
    else:
        data = []
        for item in airports:
            if typed.lower() in item[0].lower() or typed.lower() in item[1].lower() or typed.lower() in item[2].lower() or typed.lower() in item[3].lower():
                data.append(item)

    update(data)

def check2(e, airports):
    """
    Handler function to check entry in second textbox vs listbox
    """
    typed = my_entry2.get()
    if typed == '':
        data = airports
    else:
        data = []
        for item in airports:
            if typed.lower() in item[0].lower() or typed.lower() in item[1].lower() or typed.lower() in item[2].lower() or typed.lower() in item[3].lower():
                data.append(item)

    update2(data)

def find_path(my_entry, my_entry2):
    """
    Shows the shortest route based on the source airport entered and destination airport entered in GUI. Uses find_shortest_route() from network.py to compute the shortest route.
    """
    paths = flight_network.find_shortest_route(my_entry.get()[:3], my_entry2.get()[:3])
    if paths == []:
        my_route_label = Label(root, text='No connections', fg="white", bg='#163959')
    else:
        my_route_label = Label(root, text=''.join([airport.code + ", " + airport.name + '\n' for airport in paths]), font=("Helvetica, 14"), fg="white", bg='#163959')
    my_route_label.grid(row = 7, column = 0, sticky = W, padx=30, pady = 50)
    mainloop()

if __name__ == '__main__':
    flight_network = network.FlightNetwork()
    root = Tk()
    root.title("Air Nav")
    root.resizable(width=False, height=False)
    root.configure(bg="#0B1823")

    titleLabel = Label(root, bg="#0B1823", text="Air Nav", font=("Harlow Solid Italic", 50))
    titleLabel.grid(row=0, column=0, padx=30)
    authorLabel = Label(root, bg="#0B1823", text="Designed by Arjun, Rohan, Hadi & Azlan", font=("Dubai Light", 20))
    authorLabel.grid(row=1, column=0, padx=50)

    my_label = Label(root, text="Search Source Airport...", font=("Helvetica, 14"), fg="white", bg='#163959')
    my_label.grid(row = 3, column = 0, sticky = W, padx=30, pady = 50)

    my_label2 = Label(root, text="Search Destination Airport...", font=("Helvetica, 14"), fg="white", bg='#163959')
    my_label2.grid(row = 3, column = 1, sticky = W, padx=30, pady = 50)
   
    my_entry = Entry(root, font=("Helvetica", 20), bg='#163959')
    my_entry.grid(row = 4, column = 0, sticky = W, padx=30, pady = 2)

    my_entry2 = Entry(root, font=("Helvetica", 20), bg='#163959')
    my_entry2.grid(row = 4, column = 1, sticky = W, padx=30, pady = 2)

    var1 = Variable(value=[str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + ", " + str(item[3]) for item in dt.get_airports()])
    my_list = Listbox(root, listvariable=var1, height=6, selectmode=EXTENDED, bg='#163959')
    my_list.grid(row=5, column=0)

    var2 = Variable(value=[str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + ", " + str(item[3]) for item in dt.get_airports()])
    my_list2 = Listbox(root, listvariable=var2, height=6, selectmode=EXTENDED, bg='#163959')
    my_list2.grid(row=5, column=1, padx=30)

    my_list.bind("<<ListboxSelect>>", func=lambda e: fillout(e))
    my_entry.bind("<KeyRelease>", func=lambda e, arg=dt.get_airports(): check(e, arg))
    
    my_list2.bind("<<ListboxSelect>>", func=lambda e: fillout2(e))
    my_entry2.bind("<KeyRelease>", func=lambda e, arg=dt.get_airports(): check2(e, arg))

    computeButton = Button(root, text="Find shortest path...", borderwidth=2, bg="#e56637", width=15, font=("Helvetica", 16, "bold"), command=lambda: find_path(my_entry, my_entry2))
    computeButton.grid(row=6, column=0, pady = 30)

    mainloop()

