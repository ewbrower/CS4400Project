from access import Accessor
from tkinter import *

class Tester:
    """This is just for testing the functions"""
    def __init__(self, root):
        self.access = Accessor("That", "Those")
        root.wm_title("Test")
        ##
        testButt = Button(root, text = "Test", command = self.changeRet)
        testButt.grid(row = 0, column = 0)
        self.item = StringVar()
        self.output = Label(root, textvariable = self.item)
        self.output.grid(row = 1, column = 0)

    def changeRet(self):
        self.item.set(self.access.test("this"))

win = Tk()
w = Tester(win)
win.mainloop()