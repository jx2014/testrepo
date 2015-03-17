#Created by Jeremy Xue
#2015-01-09
#v5 support drag n drop of multiple driver folders
#v6 corrected noinstall logic
#v7 add auto reboot and logging driver install

import time
import ConfigParser
import re
import subprocess
import sys, getopt
import os
import platform
from collections import OrderedDict

print os.getcwd()

hwids = OrderedDict()
infs = OrderedDict()
oems = OrderedDict()
all_dirs = []

failNum = 0

if os.path.exists('driverInstall.log'):
    os.remove('driverInstall.log')

if '64' in platform.machine():
    pnputil = 'c:\windows\sysnative\pnputil.exe '
else:
    pnputil = 'pnputil.exe'
    
inf = re.compile(r"oem\d*\.inf")
#inf = re.compile(r"[a-zA-Z]:\\.*oem\d*\.inf")

rootcompare = 0
config = ConfigParser.ConfigParser()

if '-c' in sys.argv:
    config.read(sys.argv[sys.argv.index('-c')+1])
else:
    config.read(r'.\config_files\uniDrv.ini')

devcon = config.get('Default', 'devcon')
debug = config.getboolean('Default', 'debug')
driverInstall = config.getboolean('Default', 'drvInstall')
driverFolder = config.get('Default', 'drvFolder')
drv_id = config.get('Default', 'drv_id')

subprocess.call([devcon, "rescan"])

for i in config.items('HWIDS'):
    hwids[i[0]] = i[1]

for i in config.items('INF'):
    infs[i[0]] = i[1]


if os.path.exists(sys.argv[1]):
    if debug: print '{0:10}'.format(sys.argv[1])
    drv_path = sys.argv[1]      
    for inf_name in infs.keys():
        if debug: print inf_name
        driver_name = infs.get(inf_name)
        list_of_dirs = []
        for root, dirs, files in os.walk(drv_path):
            if driver_name in files:# and drv_id in root:
                #print driver_name, root
                list_of_dirs.append(root)
        if len(list_of_dirs) > 0:
            all_dirs.append(list_of_dirs)
else:
    print 'If not using drag n drop, then ignore this error:'
    print 'path:', sys.argv[1], ' doesn\'t exist'

driverInstall = True        

if '-d' in sys.argv:
    debug = True
if '-noinstall' in sys.argv:
    driverInstall = False



pa = None
for i in all_dirs:
    if pa is None:
        pa = set(i)
    pa.intersection_update(set(i))

'''
try:
    for i in pa:
        print '*' * 3
        print i
except:
    pass
'''

if driverInstall == True:
    if pa == None:
        sys.exit('No drver found')
    elif len(pa) > 1: 
        print '\nMultiple driver folder found:'
        for index, item in enumerate(pa):
            print index+1, item
            inx = index+1   
        selection = 0
        while True:
            try:        
                selection = int(raw_input('Select from above list[1 - %d]: ' % inx))
            except:            
                continue
            if selection < 1 or selection > inx:
                continue
            else:
                break               
        driverFolder = list(pa)[selection - 1]
    elif len(pa) == 1:
        driverFolder = list(pa)[0]
    else:   
        sys.exit('No drver found')

for key in hwids.keys():
    hwid = hwids.get(key)
    if debug: print '\n\n{0:10} {1:10}'.format(key, hwid)
    p = subprocess.check_output("%s driverfiles %s" % (devcon, hwid))
    with open('driverInstall.log', 'a') as log:
            log.write(p) 
    oeminf = inf.search(p)
    if oeminf is not None:
        oems[key] = oeminf.group(0)
        if debug: print '***', oems.get(key)
        print '\n\nRemove device {0:10} {1:10}\n'.format(key, hwid)
        output = subprocess.check_output("%s remove %s" % (devcon, hwid))
        with open('driverInstall.log', 'a') as log:
            log.write(output)
        print output

for key in oems.keys():
    oem = oems.get(key)
    hwid = hwids.get(key)
    if debug: print '\n{0:10} {1:10}'.format(key, oem)
    print '\nRemove driver file for {0:10} {1:10}'.format(key, hwid)
    print 'pnputil -d %s' % oem
    try:
        output = subprocess.check_output([pnputil, "-d", oem],shell=True)
        with open('driverInstall.log', 'a') as log:
            log.write(output) 
        print output
    except Exception, error:
        print '****WARNING****'
        print 'System encountered a problem removing %s' % oem
        print str(error)
        #print 'We can still update the driver without running the following command'
        #print 'pnputil -d %s\n\n' % oem

subprocess.call([devcon, "rescan"])
    
if driverInstall:
    print '\n\nDriver Folder is:\n %s\n\n' % driverFolder    
    for key in hwids.keys():
        hwid = hwids.get(key)
        inf = infs.get(key)
        print '\n\nInstalling driver for {0:10} {1:10}\n'.format(key, hwid)
        if debug: print '**', driverFolder+'\\'+inf
#        subprocess.call("%s update %s %s" % (devcon, driverFolder+'\\'+inf, hwid))
        output = subprocess.check_output([devcon, "update", driverFolder+'\\'+inf, hwid])        
        with open('driverInstall.log', 'a') as log:
            log.write(output)        
        print output
        if 'failed' in output:
            failNum = failNum + 1
    if failNum == 0:
        print "Reboot in "
        for i in reversed(range(1,6)):
            time.sleep(1)
            print i
        subprocess.call('shutdown -r -f -t 3', shell=True)
        
subprocess.call([devcon, "rescan"])