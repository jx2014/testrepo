# Created by: Jeremy Zhiming Xue
# Zhimingx.j.Xue@intel.com
# Jeremy.xzm@gmail.com

import re
import sys
import subprocess

#log_file = "OV5693_VR_SOC_CAP.log"
#log_file = sys.argv[1]
log_file = str(raw_input('\nlog file name: ')) + '.log'

#print '\nInput Stream and Pin numbers, use space to enter more than one number'
#Stream_number = [int(x) for x in raw_input('Stream number: ').split()]
#Pin_number = [int(x) for x in raw_input('Pin number: ').split()]

Stream_number = [0, 1]
Pin_number = [0, 1, 2]

w,h,f = ['','','']

# print Pin_number
# print type(Pin_number)




for sn in Stream_number:
    for pn in Pin_number:

        FPS = 0

        if pn == 0: pins = 'Preview'
        if pn == 1: pins = 'Capture'
        if pn == 2: pins = 'Still'

        FPS_string_match_pattern = '(?<=\[iacamera\]===<FPS>=== Stream %s Pin %s: )\d*\.\d' % (int(sn), int(pn))
        CCpturePin_pattern = 'CCapturePin::DispatchSetFormat Filter'
        Format_pattern = '(?<=\().*(?=\))' #(640, 360, NV12)
        Pin_pattern = '%s(?= Pin )' % (pins) # Preview Pin, Capture Pin, Still Pin

        start_FPS = False

        with open(log_file) as logfile:
            for line in logfile.readlines():
                CCapturePin_Inline = re.findall(CCpturePin_pattern, line)
                #print CCapturePin_Inline
                if len(CCapturePin_Inline) > 0:
                    Pin = re.findall(Pin_pattern, line)
                    #print Pin
                    if len(Pin) > 0:
                        if start_FPS == False:
                            start_FPS = True
                            w,h,f = re.findall(Format_pattern, line)[0].replace(' ','').split(',')
                            i = 0
                            FPS = 0
                        if start_FPS == True and FPS == 0:
                            w,h,f = re.findall(Format_pattern, line)[0].replace(' ','').split(',')
                        if start_FPS == True and FPS > 0:
                            FPS = FPS / i
                            print '**FPS for %s pin, %sx%s %s Stream %s Pin %s is [%s], [%s] sample(s)' % (pins, w, h, f, sn, pn, FPS, i)
                            i = 0
                            FPS = 0
                            w,h,f = re.findall(Format_pattern, line)[0].replace(' ','').split(',')
                #print line
                #print w,h,f
                if start_FPS == True:
                    FPS_Inline = re.findall(FPS_string_match_pattern, line)
                    if len(FPS_Inline) > 0:
                        #print FPS_Inline[0]
                        FPS = FPS + float(FPS_Inline[0])
                        i = i + 1
        if FPS > 0:
            FPS = FPS / i
            print '**FPS for %s pin, %sx%s %s Stream %s Pin %s is [%s], [%s] sample(s)' % (pins, w, h, f, sn, pn, FPS, i)



#subprocess.call('pause',shell=True)
