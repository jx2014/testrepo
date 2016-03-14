def TestFunc():
    print "This is TestFunc()"
    return 0
    for i in [1,2,3]:
        print i
        TestFunc()

import time, sys, traceback

rowFromList = [1,2,3,4,5]
a = []
a.append(rowFromList[2])



for i in xrange(9):
    print i
    try:
        print 'a'
        a.append(rowFromList[i])
        print 'b'
        b       
        print 'c'        
    except IndexError, msg:
        print "WARNING: %s" % msg
        print "rowFromList Content %s" % rowFromList        
    except Exception as e:
        print "WARNING, an error occurred: %s" % e.message
    time.sleep(0.1)




