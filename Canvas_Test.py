#import tkinter as tk

#def test(event):
#    print("clicked Label")
#    print(event.widget)


#if __name__ == "__main__":

#    root = tk.Tk()
#    root.minsize(width=200, height=200)
#    app = tk.Frame(root)
#    app.pack(expand=1, fill=tk.BOTH)
#    app.rowconfigure(0, weight=1)
#    app.columnconfigure(0, weight=1)
#    canvas = tk.Canvas(app, width=1, height=1)
#    canvas.grid(row=0, column=0, sticky="nesw")

#    label = tk.Label(canvas, text="Hallo", bg="blue", fg="white")

#    label_save = canvas.create_window(100,100, window=label)
#    print(label_save)
#    canvas.addtag_withtag("TestTag", label_save)
#    print(canvas.find_withtag, "TestTag")
#    canvas.tag_bind(1, sequence="<1>", func=test)

#  root.mainloop()

#from tkinter import *


#def onObjectClick(event):
#    print('Got object click', event.x, event.y)
#    print(event.widget.find_closest(event.x, event.y))


#root = Tk()
#canv = Canvas(root, width=100, height=100)
#obj1Id = canv.create_line(0, 30, 100, 30, width=5, tags="obj1Tag")
#obj2Id = canv.create_text(50, 70, text='Click', tags='obj2Tag')

#canv.tag_bind(obj1Id, '<ButtonPress-1>', onObjectClick)
#canv.tag_bind('obj2Tag', '<ButtonPress-1>', onObjectClick)
#print('obj1Id: ', obj1Id)
#print('obj2Id: ', obj2Id)
#canv.pack()
#root.mainloop()

import tkinter as tk
import numpy


def test(event):
    print("clicked Label")
    print(event.widget)


def main():
    root = tk.Tk()
    root.minsize(width=200, height=200)
    app = tk.Frame(root)
    app.pack(expand=1, fill=tk.BOTH)
    app.rowconfigure(0, weight=1)
    app.columnconfigure(0, weight=1)
    canvas = tk.Canvas(app, width=200, height=200)
    canvas.grid(row=0, column=0, sticky="nsew")

    label = tk.Label(canvas, text="Hallo", bg="blue", fg="white")
    label.bind("<Button-1>", test)


    label_save = canvas.create_window(100, 100, window=label)
    canvas.addtag_withtag("TestTag", label_save)

    root.mainloop()

if __name__ == "__main__":
    print(numpy.version.version)
    #main()