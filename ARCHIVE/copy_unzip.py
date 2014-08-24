import time
import os
import datetime
import string
import re
import shutil

filelist_real = []
filelist_assume = []
filelist_daily = []

#need to be user inputs:
daily_folder = '20140709'
irci = '473'
_date = "20140709"
_time = "0627"

_dt = _date + '_' + _time


#source remote path and folder names
remote_path = '\\\\irsapp002-smb.ir.intel.com\\nfs\site\\disks\\iir_viedpkgs.0400\\viedifw\\day'
folder_irci_master = 'irci_master' + '_' + _dt
remote_path_irci_master = remote_path + '\\' + folder_irci_master
remote_path_css = remote_path_irci_master + '\\'+ 'ifw-ispfw'
remote_path_hdr = remote_path_irci_master + '\\' + 'ispfw'


#target local path and folder names (will be self generated)
local_path = 'F:\\daily_integration\\'
folder_daily = local_path + '\\' + daily_folder + '\\' + irci
#create folder if necessary:
if not os.path.exists(folder_daily):
    os.makedirs(folder_daily)


#ifw-ispfw folder
#css_pkg_css_skycam_a0t_system_irci_master_20140702_0200.tar.gz
#sh_css_sw_hive_isp_css_2400_system_irci_master_20140702_0200.windows.tar.gz
css_assume = {"2400": remote_path_css + '\\' + "sh_css_sw_hive_isp_css_2400_system_irci_master_" + _dt + ".windows.tar.gz",
       "2401": remote_path_css + '\\' + "sh_css_sw_hive_isp_css_2401_system_irci_master_" + _dt + ".windows.tar.gz",
       "2401_csi2plus": remote_path_css + '\\' + "sh_css_sw_csi2plus_hive_isp_css_2401_system_irci_master_" + _dt + ".windows.tar.gz",
       "2500": remote_path_css + '\\' + "css_pkg_css_skycam_a0t_system_irci_master_" + _dt + ".tar.gz"
       }

#ispfw folder
#isp_acc_css21_2400b0_20140702_0406.tar.bz
#isp_acc_css21_2401_20140702_0406.tar.bz
hdr_assume = {"2400b0":["isp_acc_css21_2400b0"],
       "2401":["isp_acc_css21_2401"],
       }

class file_construct:
    def __init__(self,proj,_dir):
        self.dir = _dir
        self.fl = self.list_file()

    def list_file(self):
        fl = []
        for r,d,p in os.walk(self.dir):
            for f in p:
                fl.append(r + '\\' + f)
        return fl

    def list_filter(self):
        pass

hdr_real = file_construct('hdr',remote_path_hdr)
css_real = file_construct('css',remote_path_css)

filelist_real = css_real.fl


for key in css_assume.viewkeys():
    filelist_assume.append(css_assume.get(key))

for _file in hdr_real.fl:
    filelist_assume.append(_file)


for _file in filelist_assume:
    print _file
    if os.path.exists(_file):
        shutil.copy2(_file,folder_daily)

for r,d,p in os.walk(folder_daily):
    for f in p:
        print r + '\\' + f
        filelist_daily.append(r + '\\' + f)