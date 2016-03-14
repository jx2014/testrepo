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
num_threads = 3

def real_task(q):
    while True:
        item = q.get()
        for i in xrange(2):
            time.sleep(1)
            print 'real_task() %d\n' % i
        q.task_done()
        print 'q.task_done() reached\n'


for i in range(num_threads):
    #worker = Thread(target=do_stuff, args=(qu,))
    worker = Thread(target=real_task, args=(qu,))
    worker.setDaemon(True)
    print "tread: ", i
    worker.start()

print ''

for x in range(5):
    qu.put(x)
    print 'qu.put(x): ', x

print ''

while not qu.empty():
    print "qu.get_nowait(): ", qu.get_nowait()
    qu.task_done()

print ''


#qu.join()


# for x in range(3):
#     qu.put(x)
#     print 'x: ', x
#     qu.join()
