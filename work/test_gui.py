# Testing Tkinter GUI
# Author: Jeremy Xue
# Jeremy.xzm@gmail.com
# Last update: Apr 01, 2015

import Tkinter as tk
import subprocess
from threading import Thread
from Queue import Queue, Empty

class TestGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ConstructUI()

    def ConstructUI(self):
        text1 = tk.Text(self)
        text1.config(height=4, width=10)
        text1.pack()

        self.pack()


def main():
    root = tk.Tk()
    root.geometry('600x600+5+5')
    root.title('Tkinter GUI')
    app = TestGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()