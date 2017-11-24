#!/usr/bin/env python2

import urllib2
import urllib
from Tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.button = Button(frame, text="Quit", fg="red", command=frame.quit())
        self.button.pack(side=LEFT)
        self.slogan = Button(frame, text="Hello", fg="blue", command=self.write_slogan)
        self.slogan.pack(side=LEFT)
    def write_slogan(self):
        print "TkInter is easy!"


def main():
    mydata = [('user','bob'), ('pass', 'secret')]
    mydata = urllib.urlencode(mydata)
    path = "https://l.l.txq.se:5000/api"
    req = urllib2.Request(path, mydata)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    page=urllib2.urlopen(req).read()
    print page
    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
