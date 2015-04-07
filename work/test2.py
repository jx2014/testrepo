#!/usr/bin/python
"""
- read output from a subprocess in a background thread
- show the output in the GUI
- stop subprocess using a Tkinter button
"""
#from __future__ import print_function
from collections import deque
from itertools import islice
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk # Python 3

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty # Python 3

#info = print

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

class StopProcessDemo:
    def __init__(self, root):
        self.root = root

        # start dummy subprocess to generate some output
        self.proc = Popen(["dir", "/s"], cwd = 'c:\\windows', shell=True, stdout=PIPE, stderr=STDOUT)

        # launch thread to read the subprocess output
        #   (put the subprocess output into the queue in a background thread,
        #    get output from the queue in the GUI thread.
        #    Output chain: proc.readline -> queue -> stringvar -> label)
        q = Queue()
        t = Thread(target=self.reader_thread, args=[q]).start()

        # show subprocess' stdout in GUI
        self._var = tk.StringVar() # put subprocess output here
        tk.Label(root, textvariable=self._var).pack()
        self.update(q) # start update loop
        self.text1 = tk.Text()
        self.text1.config(height=100, width=100)
        self.text1.pack()
        # stop subprocess using a button
        tk.Button(root, text="Stop subprocess", command=self.stop).pack()

    def reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        for line in iter(self.proc.stdout.readline, b''):
            q.put(line)
        print 'done reading'

    def update(self, q):
        """Update GUI with items from the queue."""
        # read no more than 10000 lines, use deque to discard lines except the last one,
        for line in deque(islice(iter_except(q.get_nowait, Empty), 100000), maxlen=1):
        #for line in iter_except(q.get_nowait, Empty):
            if line is None:
                return # stop updating
            else:
                #self._var.set(line) # update GUI
                self.text1.insert(tk.END, line)
                self.text1.see(tk.END)
        self.root.after(1, self.update, q) # schedule next update

    def stop(self):
        """Stop subprocess and quit GUI."""
        print 'stoping'
        self.proc.terminate() # tell the subprocess to exit

        # kill subprocess if it hasn't exited after a countdown
        def kill_after(countdown):
            if self.proc.poll() is None: # subprocess hasn't exited yet
                countdown -= 1
                if countdown < 0: # do kill
                    print 'killing'
                    self.proc.kill() # more likely to kill on *nix
                else:
                    self.root.after(1000, kill_after, countdown)
                    return # continue countdown in a second
            # clean up
            self.proc.stdout.close()  # close fd
            self.proc.wait()          # wait for the subprocess' exit
            self.root.destroy()       # exit GUI
        kill_after(countdown=5)

root = tk.Tk()
app = StopProcessDemo(root)
root.protocol("WM_DELETE_WINDOW", app.stop) # exit subprocess if GUI is closed
root.mainloop()
print 'exited'



for item in islice('abcdefghijk', 2, None, 2):
    print '...', item