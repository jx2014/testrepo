# define each tarfile name pattern
# define each tarfile location
import os
import shutil
import tarfile
import re
import string

def print_func(fn):
    def wrapped(self):
        name = fn.__name__ + '()'
        print '{}\n{}\n{}'.format( '_'*125, name, fn(self))
    return wrapped

##################################################################################################################
#                                                                                                                #
#                                         F I L E   C O N S T R U C T                                            #
#                                                                                                                #
##################################################################################################################

class fc:
    def __init__(self, fw_sub_folder='', alt_package_name='',**kwarg):
        # list_of_variables will be automatically assigned values,
        # define their values when creating the class
        # These variables are mandatory

##########################################################################################################
#          begin of auto assign list of variables                                                        #
##########################################################################################################
        list_of_variables = [
                             "package_code",
                             "package_fn",
                             "package_extension",
                             "fw_name",
                             "package_date",
                             "daily_folder",
                             "package_hr",
                             'remote_path',
                             "irci",
                             "local_path",
                             ]

        for key in list_of_variables:
            skey = 'self.' + key
            print '{0:<30}{1:<20}'.format(skey, kwarg.get(key))
            exec('%s=%s' % (eval('skey'), 'kwarg.get(key)')) # Trick to auto assign a list of variables
##########################################################################################################
#           end of auto assign list of variables                                                         #
##########################################################################################################
        self._dt = self.package_date + '_' + self.package_hr
        #package_full_name  i.e. sh_css_sw_hive_isp_css_2400_system_irci_master_20140715_1500.windows.tar.gz
        self.package_full_name = self.package_fn + self._dt + self.package_extension
        #package folder full name i.e. irci_master_20140715_1500
        self.folder_irci_master = 'irci_master' + '_' + self._dt

        # this is used for skycam css_fw.bin, set fw_sub_folder = 'firmware.target\\firmware'
        self.fw_sub_folder = fw_sub_folder
        # also used for skycam, since zipped package name is different than folder package name.
        self.alt_package_name = alt_package_name
        self.full_alt_package_name = self.alt_package_name + self._dt

        self.remote_path_irci_master = self.remote_path + '\\' + self.folder_irci_master
        self.remote_path_css = self.remote_path_irci_master + '\\'+ 'ifw-ispfw'
        self.remote_path_hdr = self.remote_path_irci_master + '\\' + 'ispfw'
        self.remote_path_css_file = self.remote_path_css + '\\' + self.package_full_name

        self.daily_folder_path = self.local_path + '\\' + self.daily_folder + '\\' + self.irci
        self.local_path_file = self.daily_folder_path + '\\' + self.package_full_name

        if not os.path.exists(self.daily_folder_path):
            os.makedirs(self.daily_folder_path)

        self.local_package_folder_name = self.get_package_folder_name()

    def fcopy(self):
        if os.path.exists(self.remote_path_css_file):
            if os.path.exists(self.local_path_file):
                print '{0:25}{2:<100}\n{1:25}{3:<100}'.format('Warning:', 'already exists in:', self.package_full_name, self.daily_folder_path)
            else:
                shutil.copy(self.remote_path_css_file,self.local_path_file)

    # get tar extension of package_full_name
    #@print_func
    def get_tar_extension(self):
        # pattern to detect tar extensions: tar.gz tar.bz tar.bz2
        tar_ext = re.compile("(?<=\.)tar\..*")
        extension = tar_ext.search(self.package_full_name)
        if extension:
            #print '_'*125
            #print 'get_tar_extension()'
            print '{0:25}{1:<100}'.format('Extension is:', extension.group())
            return extension.group()
        else:
            return 'Got no match, dog'

    # get package_full_name minus tar extension, this is the extracted folder name, except for skycam
    #@print_func
    def get_folder_name(self):
        tar_ext = re.compile(".+(?=\.tar\..*)")
        folder_name = tar_ext.search(self.package_full_name)
        if folder_name:
            #print '_'*125
            #print 'get_folder_name()'
            #print '{0:<25}{1:<100}'.format('folder_name is:',folder_name.group())
            return folder_name.group()
        else:
            print 'It ain\'t got no folder, dog'

    #@print_func
    def extract_tar(self):
        if os.path.exists(self.local_path_file):
            with tarfile.open(self.local_path_file) as tf:
                tf.extractall(self.daily_folder_path)
                #print '_'*125
                #print 'extract_tar()'
                print '{0:25}{1:<100}\n{2:25}{3:<100}'.format('Extracted:', self.package_full_name, 'in local folder:', self.daily_folder_path)
        else:
            #print '_'*125
            #print 'extract_tar()'
            print '{0:25}{1:<100}\n{2:25}{3:<100}'.format('Warning:', self.package_full_name, 'does not exists in:', self.daily_folder_path)

    #give full path to extracted package folder, for skycam, package name is different
    def get_package_folder_name(self):
        # pre defined alt_package_name will be used here, mainly for skycam
        if self.alt_package_name:
            folder_name = self.full_alt_package_name
        else:
            folder_name = self.get_folder_name()
        full_package_folder_path = self.daily_folder_path + '\\' + folder_name
        #if os.path.exists(full_package_folder_path):
        print '{0:25}{1:<100}'.format('Local package directory:', full_package_folder_path)
        return full_package_folder_path

    def change_css_folder_name(self):
        full_css_folder_path = self.local_package_folder_name + '\\' + 'css'
        new_full_css_folder_path = self.local_package_folder_name + '\\' + self.fw_name
        if os.path.exists(full_css_folder_path):
            print '{0:25}{1:<100}'.format('Local css directory:', full_css_folder_path)
            print '{0:25}{1:<100}'.format('New css directory:', new_full_css_folder_path)
            try:
                os.rename(full_css_folder_path,new_full_css_folder_path)
                shutil.move(new_full_css_folder_path, self.daily_folder_path)
            except:
                print 'Can not rename or move, may be files and directory already exists'

    def change_css_file_name(self):
        # by fw_sub_folder is None, but for skycam, user will add sub folder to it, and as a result, full_css_file_name will change accordingly
        if self.fw_sub_folder:
            full_css_file_name = self.local_package_folder_name + '\\' + self.fw_sub_folder + '\\' + 'css_fw.bin'
            new_full_css_file_name = self.local_package_folder_name + '\\' + self.fw_sub_folder + '\\' + 'css_fw_' + self.fw_name + '.bin'
        else:
            full_css_file_name = self.local_package_folder_name + '\\' + 'css_fw.bin'
            new_full_css_file_name = self.local_package_folder_name + '\\' + 'css_fw_' + self.fw_name + '.bin'
        if os.path.exists(full_css_file_name):
            print '{0:25}{1:<100}'.format('Local css file name:', full_css_file_name)
            print '{0:25}{1:<100}'.format('New css file name:', new_full_css_file_name)
            try:
                os.rename(full_css_file_name, new_full_css_file_name)
                shutil.move(new_full_css_file_name, self.daily_folder_path)
                new_full_css_file_path = self.daily_folder_path + '\\' + 'css_fw_' + self.fw_name + '.bin'
                return new_full_css_file_path
            except:
                print 'Can not rename or move, may be file and directory already exists'

    def rename_move_css_folder_file(self):
        self.fcopy()
        self.get_tar_extension()
        self.extract_tar()
        self.change_css_folder_name()
        self.change_css_file_name()
        shutil.rmtree(self.local_package_folder_name)



##################################################################################################################
#                                                                                                                #
#                           A C T I V E   F I L E   C O N S T R U C T                                            #
#                                                                                                                #
##################################################################################################################

class active_fc():
    def __init__(self, income_pkg, delete_pkg='', **kwarg):
        self.inc_pkg_path = income_pkg
        self.owd = os.getcwd()
        os.chdir(self.inc_pkg_path)
        #incoming package date time to be determined by get_dt func
        self.pkg_date = ''
        self.pkg_time = ''
        self.delete_pkg = delete_pkg
        #self.pkg_dt = ''

    # use folder name to determine actual packages.
    def id_folders(self, fn):
        '''
            return the folder name and package code
            i.e.
                >>>fn, id = fc.id_folders('sh_css_sw_hive_isp_css_2400_system_irci_master_20140717.windows')
                >>>fn
                sh_css_sw_hive_isp_css_2400_system_irci_master_20140717.windows
                >>>id
                2400
        '''
        pkg_2400 = re.compile('^sh_css_sw_hive_isp_css_2400_system_irci_master_\d{8}_\d{4}\.windows$')
        pkg_2401 = re.compile('^sh_css_sw_hive_isp_css_2401_system_irci_master_\d{8}_\d{4}\.windows$')
        pkg_2401_csi2plus = re.compile('^sh_css_sw_csi2plus_hive_isp_css_2401_system_irci_master_\d{8}_\d{4}\.windows$')
        pkg_2500 = re.compile('^sh_css_sw_css_skycam_a0t_system_irci_master_\d{8}_\d{4}')

        if pkg_2400.search(fn): return fn, '2400'
        if pkg_2401.search(fn): return fn, '2401'
        if pkg_2401_csi2plus.search(fn): return fn, '2401_csi2plus'
        if pkg_2500.search(fn): return fn, '2500'

    def change_move_folder_fw(self,folder, css_id, css_fw_folder=''):
        css_folder = folder + '\\' + 'css'
        new_css_folder = folder + '\\' + css_id

        if css_fw_folder:
            css_fw = string.join([folder, css_fw_folder, 'css_fw.bin'],'\\')
            new_css_fw = string.join([folder, css_fw_folder, 'css_fw_' + css_id + '.bin'],'\\')
        else:
            css_fw = folder + '\\' + 'css_fw.bin'
            new_css_fw = folder + '\\' + 'css_fw_' + css_id + '.bin'

        print '_' * 100
        print 'renaming {} to {}'.format(css_folder, new_css_folder)
        print 'renaming {} to {}'.format(css_fw, new_css_fw)
        try:
            os.rename(css_folder, new_css_folder)
            os.rename(css_fw, new_css_fw)
        except:
            print 'unable to rename, something went wrong'

        print 'moving {} to {}'.format(new_css_folder, os.getcwd())
        print 'moving {} to {}'.format(new_css_fw, os.getcwd())
        try:
            shutil.move(new_css_folder, os.getcwd()) # getcwd should return self.inc_pkg_path
            shutil.move(new_css_fw,os.getcwd())
            if self.delete_pkg == 'yes':
                shutil.rmtree(folder)
        except:
            print 'unable to move css folder or css fw, something went wrong'

    #Used by unzip_pkgs()
    def get_pkgs(self):
        #regex to get all the tar files.
        tfsearch = re.compile('.*\.tar\.{0,1}.*')
        for root,dir,file in os.walk(os.getcwd()):
            for fn in file:
                tf_found = tfsearch.search(fn)
                if tf_found:
                    yield fn

    def get_folders(self):
        for root, dir, file in os.walk(os.getcwd()):
            return dir

    # unzip all the pkgs found in self.inc_pkg_path
    def unzip_pkgs(self):
        for pkg in self.get_pkgs():
            with tarfile.open(pkg) as tf:
                print 'unzipping...%s' % pkg
                tf.extractall(os.getcwd())

    #func to get date and time out of a package name
    def get_dt(self, fn):
        find_date = re.compile('\d{8}(?=_\d{4}\.)')
        find_time = re.compile('(?<=\d{8}_)\d{4}(?=\.)')
        find_dt = re.compile('\d{8}_\d{4}(?=\.)')
        date = find_date.search(fn)
        time = find_time.search(fn)
        dt = find_dt.search(fn)

        if date and time and dt:
            return date.group(),time.group(),dt.group()

    def unzip_rename_move(self):
        '''
            Final function to unzip, rename and move folder, fw
        '''
        self.unzip_pkgs()
        for flder in self.get_folders():
            fn, id = self.id_folders(flder)
            # used for skycam
            if id == '2500':
                css_fw_folder = 'firmware.target\\firmware'
            else:
                css_fw_folder = ''
            self.change_move_folder_fw(fn,id, css_fw_folder)



##################################################################################################################
#                                                                                                                #
#                           C S S    V E R S I O N     C H A N G E R                                             #
#                                                                                                                #
##################################################################################################################



class css_version_file():
    '''
        Example how to use it:

            from Intel_ICG_File_Construct.file_construct import css_version_file

            package_hr = '0200'
            daily_folder = '20140728'
            #css_version_path = r'C:\Users\ChilleeChillee\git\git\textfile.txt'
            css_version_path = r'E:\FamilyProject\TestProject\GUI\textfile.txt'

            cvfc = css_version_file(
                                    package_hr = package_hr,
                                    daily_folder = daily_folder,
                                    css_version_path = css_version_path,
                                    )

            # cvfc.read_write_file()
            # cvfc.change_date_from_css_version()
            # cvfc.read_write_file('shit','dick')
            cvfc.final_wrtie_new_date_css_version()
    '''
    def __init__(self,**kwargs):
        self.daily_folder = kwargs.get('daily_folder')
        self.package_hr = kwargs.get('package_hr')
        self.css_version_path = kwargs.get('css_version_path')
        self.new_css_date = '{}-{}-{}'.format(self.daily_folder[0:4],self.daily_folder[4:6],self.daily_folder[6:8])
        self.new_css_version = self.daily_folder + '_' + self.package_hr
        self.css_version_path_tmp = self.css_version_path + '.tmp'

    def read_write_file(self, new_date='', new_line=''):
        with open(self.css_version_path_tmp,'wb+') as css_file_tmp:
            css_file_tmp.write(new_date+'\n')
            css_file_tmp.write(new_line+'\n')
            with open(self.css_version_path) as css_file:
                for line in css_file:
                    css_file_tmp.write(line)

    def change_date_from_css_version(self):
        csv_regex = '\d{8}_\d{4}'
        self.old_css_version_string = open(self.css_version_path).readlines()[1]
        #print 'old date: ',self.old_css_version_string
        self.new_css_version_string = re.sub(csv_regex, self.new_css_version, self.old_css_version_string)
        #print self.new_css_date
        return self.new_css_version_string

    def final_wrtie_new_date_css_version(self):
        new_css_version = self.change_date_from_css_version()
        self.read_write_file(self.new_css_date,new_css_version)
        os.remove(self.css_version_path)
        os.rename(self.css_version_path_tmp, self.css_version_path)



##################################################################################################################
#                                                                                                                #
#                                   F O L D E R   C O M P A I R S O N                                            #
#                                                                                                                #
##################################################################################################################

class folder_compare():
    def __init__(self, **kwargs):
        pass
