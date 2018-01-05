# automatically increase trial serial #
#
#
import time
import re
import fileinput
import sys

class TrialIncrease(object):
    def __init__(self, input_folder):        
        file_name = 'application.xml'
        self.input_file = "\\".join([input_folder, file_name])
    
    def search_replace(self):        
        with open(self.input_file, 'r') as infile:
            old_xml = infile.read()            
            
        sn = re.search("(?<=TrialSerialNumber\">)\d*", old_xml)
        if sn is not None:
            sn_new = str(int(sn.group()) + 1)
            try:
                new_xml = old_xml.replace(sn.group(), sn_new)
            except Exception:
                raise Exception
        
            with open(self.input_file, 'w') as ofile:
                ofile.write(new_xml)
        
        print('file:', self.input_file)
        print('old sn:', sn.group())
        print('new sn:', sn_new)

if __name__ == '__main__':
    lr = TrialIncrease('C:\Program Files\Adobe\Adobe Lightroom Classic CC\AMT')
    lr.search_replace()
    ps = TrialIncrease('C:\Program Files\Adobe\Adobe Photoshop CC 2018\AMT')
    ps.search_replace()
    input("Press any key to continue.")
    #time.sleep(3)
    sys.exit(0)
                    

                    
        
        
    