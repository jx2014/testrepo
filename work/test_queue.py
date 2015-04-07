from Queue import Queue
from threading import Thread
import time

# my_queue = Queue(maxsize=0)
#
# my_queue.put(1)
# my_queue.put(2)
# my_queue.put(3)
#
# print my_queue.get()
#
# my_queue.task_done()

qu = Queue(maxsize=0)
num_threads = 2

def real_task(q):
    while True:
        item = q.get()
        for i in xrange(5):
            time.sleep(1)
            print 'real_task() %d\n' % i
        q.task_done()
        print 'q.task_done() reached'


for i in range(num_threads):
    #worker = Thread(target=do_stuff, args=(qu,))
    worker = Thread(target=real_task, args=(qu,))
    worker.setDaemon(True)
    worker.start()

for x in range(5):    
    qu.put(x)
    qu.join()
