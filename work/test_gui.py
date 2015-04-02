# Testing Tkinter GUI
# Author: Jeremy Xue
# Jeremy.xzm@gmail.com
# Last update: Apr 01, 2015

import Tkinter as tk
import subprocess
from threading import Thread
from Queue import Queue, Empty
import time

class TestGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ConstructUI()

    def ConstructUI(self):
        self.text1 = tk.Text(self)
        self.text1.config(height=100, width=100)
        self.text1.pack()
        self.pack()

        t = Thread(target=self.dir)
        t.start()



#         for n in [5, 11]:
#             t = Thread(target=self.ForLoop, args=(n,))
#             t.start()

    def dir(self):
        self.process = subprocess.Popen('dir /s',
                                      cwd = 'c:\\',
                                      shell = True,
                                      stdout = subprocess.PIPE,
                                      stdin = subprocess.PIPE,
                                      stderr = subprocess.PIPE)

        for i in self.process.stdout.readlines():
            self.text1.insert(tk.END, i)


    def ForLoop(self, n):
        for i in xrange(n):
            print '\nn is %d : %d\n' % (n, i)
            time.sleep(1)

    def SomeProcess(self):
        self.process = subprocess.Popen('cd c:\\ && dir',
                                        stdout = subprocess.PIPE,
                                        stdin = subprocess.PIPE,
                                        stderr = subprocess.PIPE)
        self.queue = Queue()
        self.thread = Thread(target=self.readlines, args=(self.SomeProcess, self.queue))
        self.thread.start()
        self.after(100, self.updateLines)

    def updateLines(self):
        try:
            line = self.queue.get(False)
            self.text1.config(state=tkinter.NORMAL)
            self.text1.insert(tkinter.END, line)
            self.text1.config(state=tkinter.DISABLED)
        except Empty:
            pass

        if self.process.poll() is None:
            self.after(100, self.updateLines())

    def ReadLines(self, process, queue):
        while process.poll() is None:
            queue.put(process.stdout.readline())


def main():
    root = tk.Tk()
    root.geometry('600x600+5+5')
    root.title('Tkinter GUI')
    app = TestGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()