from file_construct import active_fc
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('C:\Users\zjxuex\My Documents\LiClipse Workspace\work\path_config.ini')

path_incoming_package  = config.get('Incoming_packages', 'path_incoming_package')
local_path = config.get('Incoming_packages', 'local_path')


# path_incoming_package = r'F:\Incoming_packages'
# local_path = r'C:\Temp\tartest\Local' #not needed for now

active_unzip_all = active_fc(
                             income_pkg = path_incoming_package,
                             delete_pkg = 'no'
                             )

active_unzip_all.unzip_rename_move()