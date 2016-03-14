import threading
import time



class Logger(threading.Thread):
    def __init__(self, msg, of):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.message = msg
        self.outputFile = of

    def run(self):
        n = 0
        while (not self.stop_event.is_set()):
            with open(self.outputFile, 'a') as ofile:
                timestamp = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
                n += 1
                ofile.write('%s self.message %d\n' % (timestamp, n))
                print '%s self.message %d' % (timestamp, n)
                time.sleep(1)

    def stop(self):
        self.stop_event.set()



class Test():
    def __init__(self):
        print "This is inside Test"
        self.file = r'E:\FamilyProject\TestProject\testrepo\ThreadingTest\log.txt'

    def startlogging(self, msg):
        self.loggerFunc = Logger(msg, self.file)
        self.loggerFunc.start()

    def stoplogging(self):
        self.loggerFunc.stop()

    def printCrap(self, crap):
        print 'printCrap to print %s' % crap









