import ConfigParser
import re
import subprocess
import sys, getopt
import os

hwids = {}
infs = {}
oems = {}
pnputil = 'c:\windows\sysnative\pnputil.exe '
inf = re.compile(r"oem\d*\.inf")

config = ConfigParser.ConfigParser()
config.read('uniDrv.ini')
devcon = config.get('Default', 'devcon')
debug = config.getboolean('Default', 'debug')
driverInstall = config.getboolean('Default', 'drvInstall')
driverFolder = config.get('Default', 'drvFolder')

subprocess.call([devcon, "rescan"])


try:
	if os.path.exists(sys.argv[1]):
		if debug: print '{0:10}'.format(sys.argv[1])
		driverFolder = sys.argv[1]
	if '-i' in sys.argv:
		driverInstall = True		
	if '-d' in sys.argv:
		debug = True
	if '-noinstall' in sys.argv:
		driverInstall = False
except:
	print 'wrong argument'
	sys.exit(2)

for i in config.items('HWIDS'):
	hwids[i[0]] = i[1]

for i in config.items('INF'):
	infs[i[0]] = i[1]

for key in hwids.keys():
	hwid = hwids.get(key)
	if debug: print '{0:10} {1:10}'.format(key, hwid)
	p = subprocess.check_output("%s driverfiles %s" % (devcon, hwid))	
	oeminf = inf.search(p)
	if oeminf is not None:
		oems[key] = oeminf.group(0)
		print '\n\nRemove device {0:10} {1:10}\n'.format(key, hwid)
		subprocess.call("%s remove %s" % (devcon, hwid))

for key in oems.keys():
	oem = oems.get(key)	
	if debug: print '{0:10} {1:10}'.format(key, oem)
	print '\n\nRemove driver file for {0:10} {1:10}\n'.format(key, hwid)
	subprocess.call([pnputil, "-d", oem])

subprocess.call([devcon, "rescan"])
	
if driverInstall:
	for key in hwids.keys():
		hwid = hwids.get(key)
		inf = infs.get(key)
		print '\n\nInstalling driver for {0:10} {1:10}\n'.format(key, hwid)
		subprocess.call("%s update %s %s" % (devcon, driverFolder+'\\'+inf, hwid))
		
	
subprocess.call([devcon, "rescan"])