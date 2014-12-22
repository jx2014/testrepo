import sys, getopt
import subprocess as subp
import os

try:
	if os.path.exists(sys.argv[1]):
		print sys.argv[1]
	else:
		print 'shit'
except:
	print 'shit'
	
#print sys.argv[1]

#if folder.find(sys.argv[1]): 
#	print 'found folder!'

#print '*'*10,'wtf'
subp.call('pause',shell=True)