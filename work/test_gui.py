# Testing Tkinter GUI
# Author: Jeremy Xue
# Jeremy.xzm@gmail.com
# Last update: Apr 01, 2015

import Tkinter as tk
import subprocess
from threading import Thread
from Queue import Queue, Empty
import time
from test_gui2 import controlPanel, StdError_redirector, Std_redirector

class TestGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ConstructUI()

    def ConstructUI(self):
        self.text1 = tk.Text(self)
        self.text1.config(height=20, width=100)
        #b = tk.Button(self, text='dir', command=self.Dir, width=10)
        b = tk.Button(self, text='dir', command=self.Dir, width=10)
        p = tk.Button(self, text='print', command=self.PrintHi, width=10)
        c = tk.Button(self, text='3rd button', command=self.Pressing3rdButton, width=20)
        b.pack()
        p.pack()
        c.pack()
        self.text1.pack()
        self.pack()
        for i in range(3):
            print i
            time.sleep(0.5)

#         for n in [5, 11]:
#             t = Thread(target=self.ForLoop, args=(n,))
#             t.start()

    def Pressing3rdButton(self):
        self.text1.insert(tk.END, 'how are you\n')


    def TDir(self):
#         t = Thread(target=self.Dir)
#         r = Thread(target=self.Reader)
#         t.start()
#         r.start()
        for i in xrange(10):
            self.text1.insert(tk.END, '..working...\n')
            self.text1.see(tk.END)
            time.sleep(1)


    def PrintHi(self):
        self.text1.insert(tk.END, '... HI ...\n')
        self.text1.see(tk.END)
        print '... Hi ...'

    def Reader(self, q):
        for i in q.stdout.readlines():
            self.text1.insert(tk.END, i)

    def Dir(self):
        self.process = subprocess.Popen('dir /s',
                                      #cwd = 'c:\\JX_Projects\\vied-viedifw\\',
                                      cwd = 'c:\\windows\\',
                                      shell = True,
                                      stdout = subprocess.PIPE,
                                      stdin = subprocess.PIPE,
                                      stderr = subprocess.STDOUT)

#         self.process = subprocess.Popen('dir',
#                                       cwd = 'c:\\JX_Projects\\vied-viedifw\\',
#                                       #cwd = 'c:\\windows\\',
#                                       shell = True,
#                                       )

#         o, e = self.process.communicate()
#         print o
        #self.text1.insert(tk.END, o)

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

    def reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        for line in iter(self.proc.stdout.readline, b''):
            q.put(line)
        info('done reading')

    def update(self, q):
        """Update GUI with items from the queue."""
        # read no more than 10000 lines, use deque to discard lines except the last one,
        for line in deque(islice(iter_except(q.get_nowait, Empty), 10000), maxlen=1):
            if line is None:
                return # stop updating
            else:
                self._var.set(line) # update GUI
        self.root.after(40, self.update, q) # schedule next update


def main():
    root = tk.Tk()
    root.geometry('600x600+5+5')
    root.title('Tkinter GUI')
    app = TestGUI(root)
    print 'hello world'
    root.mainloop()

if __name__ == '__main__':
    main()