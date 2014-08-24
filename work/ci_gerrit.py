from file_construct import fc
import ConfigParser
import string
import re

date_pattern = r'\d{8}(?=_\d{4}$)'
hr_pattern = r'\d{4}$'

config = ConfigParser.ConfigParser()
#config.read('C:\Users\zjxuex\My Documents\LiClipse Workspace\work\path_config.ini')
config.read('E:\FamilyProject\TestProject\GUI\work\path_config.ini')

build_folder = config.get('ci_gerrit', 'build_folder')
ci_agent = config.get('ci_gerrit', 'agent')
partial_remote_path = config.get('ci_gerrit', 'remote_path')
local_path = config.get('ci_gerrit', 'path_incoming_package')
full_remote_path = string.join([partial_remote_path,ci_agent,build_folder],'\\')
try:
    package_date = re.search(date_pattern, build_folder).group()
    package_hr = re.search(hr_pattern, build_folder).group()
except:
    print 'cant find shit mofo'

BYT_2400 = fc(
              package_code = '2400', #probably not needed
              package_fn = 'sh_css_sw_hive_isp_css_2400_system_irci_master_',
              package_extension = '.windows.tar.gz',
              fw_name = '2400', #css_fw_2400.bin blah blah
              #package_date = package_date,
              package_date = daily_folder, # for most of the time, package_date equal to daily_folder date
              daily_folder = daily_folder,
              package_hr = package_hr,
              remote_path = remote_path,
              irci = irci,
              local_path = local_path,
              )

# BYT_2401 = fc(
#               package_code = '2401', #probably not needed
#               package_fn = 'sh_css_sw_hive_isp_css_2401_system_irci_master_',
#               package_extension = '.windows.tar.gz',
#               fw_name = '2401', #css_fw_2400.bin blah blah
#               #package_date = package_date,
#               package_date = daily_folder, # for most of the time, package_date equal to daily_folder date
#               daily_folder = daily_folder,
#               package_hr = package_hr,
#               remote_path = remote_path,
#               irci = irci,
#               local_path = local_path,
#               )
#
# CHT_2401_csi2plus = fc(
#               package_code = '2401_csi2plus', #probably not needed
#               package_fn = 'sh_css_sw_csi2plus_hive_isp_css_2401_system_irci_master_',
#               package_extension = '.windows.tar.gz',
#               fw_name = '2401_csi2plus', #css_fw_2400.bin blah blah
#               #package_date = package_date,
#               package_date = daily_folder, # for most of the time, package_date equal to daily_folder date
#               daily_folder = daily_folder,
#               package_hr = package_hr,
#               remote_path = remote_path,
#               irci = irci,
#               local_path = local_path,
#               )
#
# SKC_2500 = fc(
#               package_code = '2500', #probably not needed
#               package_fn = 'css_pkg_css_skycam_a0t_system_irci_master_',
#               package_extension = '.tar.gz',
#               fw_name = '2500', #css_fw_2400.bin blah blah
#               #package_date = package_date,
#               package_date = daily_folder, # for most of the time, package_date equal to daily_folder date
#               daily_folder = daily_folder,
#               package_hr = package_hr,
#               remote_path = remote_path,
#               irci = irci,
#               local_path = local_path,
#               fw_sub_folder = 'firmware.target\\firmware', #required for skycam
#               alt_package_name = 'sh_css_sw_css_skycam_a0t_system_irci_master_' # get it from extracted folder and rid off date time, leave the underscore
#               )

BYT_2400.rename_move_css_folder_file()
BYT_2401.rename_move_css_folder_file()
CHT_2401_csi2plus.rename_move_css_folder_file()
SKC_2500.rename_move_css_folder_file()

# print '\nBYT_2400.irci: ', BYT_2400.irci
# print '\nBYT_2400.remote_path_irci_master:\n', BYT_2400.remote_path_irci_master
# print '\nBYT_2400.remote_path_css:\n', BYT_2400.remote_path_css
# print '\nBYT_2400.remote_path_hdr:\n', BYT_2400.remote_path_hdr
# print BYT_2400.local_path
# print BYT_2400.daily_folder_path
# print BYT_2400.remote_path_css_file
# print BYT_2400.local_path_file
#
# print os.path.exists(BYT_2400.remote_path_css_file)
# print os.path.exists(BYT_2400.local_path_file)

# BYT_2400.fcopy()
# BYT_2400.get_tar_extension()
# BYT_2400.extract_tar()
# BYT_2400.change_css_folder_name()
# BYT_2400.change_css_file_name()