import threading
import time
import os



class Logger(threading.Thread):
    def __init__(self, msg, of):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.message = msg
        self.outputFile = of
        self.stopFlag = False
        self.pausedFlag = 1
        self.resumeFlag = 0
        self.msg = None
        self.started = 0

    def run(self):
        n = 0
        if self.started == 1:
            print 'already started'
        if self.started == 0:
            self.started = 1
            while (self.stopFlag == False):
                if not self.event.is_set():
                    with open(self.outputFile, 'a') as ofile:
                        timestamp = time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
                        n += 1
                        if self.resumeFlag == 1:
                            ofile.write('%s %s\n' % (timestamp,self.msg))
                            print '%s %s' % (timestamp, self.msg)
                            self.resumeFlag = 0
                        ofile.write('%s %s %d\n' % (timestamp,self.message, n))
                        print '%s %s %d' % (timestamp, self.message, n)
                        time.sleep(1)
                        if self.event.is_set() == True:
                            ofile.write('%s %s\n' % (timestamp,self.msg))
                            print '%s %s' % (timestamp, self.msg)

    def unstop(self):
        self.stopFlag = False

    def stop(self):
        self.stopFlag = True

    def pause(self):
        self.event.set()
        self.msg = 'paused'
        self.pausedFlag = 1
        self.resumeFlag = 0

    def resume(self):
        self.event.clear()
        self.msg = 'resumed'
        self.resumeFlag = 1



class Test():
    def __init__(self, msg):
        print "This is inside Test"
        self.file = r'E:\FamilyProject\TestProject\testrepo\ThreadingTest\log.txt'
        try:
            os.remove(self.file)
        except WindowsError:
            pass
        except:
            raise
        self.msg = msg

    def startlogging(self):
        self.loggerFunc = Logger(msg = self.msg, of = self.file)
        self.loggerFunc.start()

    def stoplogging(self):
        self.loggerFunc.stop()

    def pauselogging(self):
        self.loggerFunc.pause()

    def resumelogging(self):
        self.loggerFunc.resume()

    def printCrap(self, crap):
        print 'printCrap to print %s' % crap

test1=Test('test1')
test2=Test('test2')








