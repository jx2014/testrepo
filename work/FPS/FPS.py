# Created by: Jeremy Zhiming Xue
# Zhimingx.j.Xue@intel.com
# Jeremy.xzm@gmail.com

import re
import sys
import subprocess

#log_file = "CameraLog_19-36-17_12-16-2014.log"
#log_file = sys.argv[1]
log_file = str(raw_input('\nlog file name: ')) + ".log"

print '\nInput Stream and Pin numbers, use space to enter more than one number'
Stream_number = raw_input('Stream number: ').split()
Pin_number = raw_input('Pin number: ').split()

for sn in Stream_number:
	for pn in Pin_number:
		FPS_string_match_pattern = '(?<=\[iacamera\]===<FPS>=== Stream %s Pin %s: )\d*\.\d' % (int(sn), int(pn))
		i = 1
		FPS = 0

		with open(log_file) as logfile:
			for line in logfile.readlines():
				FPS_Inline = re.findall(FPS_string_match_pattern, line)
				if len(FPS_Inline) > 0:
					FPS = FPS + float(FPS_Inline[0])			
					i = i + 1

		FPS = FPS / i		
		print '***average FPS for Stream %s Pin %s is [%s] over [%s] entries' % (sn, pn, FPS, i)

subprocess.call('pause',shell=True)
