from tkinter import *
from PIL import ImageTk, Image
import os

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)               
        self.master = master
        self.init_window ()

    def init_window (self):

    	self.master.title ('OKcountyrecords Scraper')

    	self.pack (fill=BOTH, expand=1)

    	quitButton = Button (self, text = "Quit", command = self.client_exit)

    	quitButton.place (x=0, y=0)

    	load = Image.open('OK.png')
    	render = ImageTk.PhotoImage(load)
    	img = Label(image=render)
    	img.image = render
    	img.pack(side=BOTTOM)

    	load = Image.open('GSM2.png')
    	render = ImageTk.PhotoImage(load)
    	img = Label(image=render)
    	img.image = render
    	img.pack(side=TOP)


    def client_exit (self):
    	exit ()


root = Tk ()
root.geometry ("400x300")

app = Window (root)
root.mainloop ()