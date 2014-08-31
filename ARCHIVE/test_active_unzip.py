from Intel_ICG_File_Construct.file_construct import active_fc

path_incoming_package = r'C:\Temp\tartest\Local\Incoming_packages'
local_path = r'C:\Temp\tartest\Local'

active_unzip_all = active_fc(
                             income_pkg = path_incoming_package,
                             delete_pkg = 'yes'
                             )

active_unzip_all.unzip_rename_move()