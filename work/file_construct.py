# FW package download, unzip utility,
# 2400/2401/2401_CSI2PLUS css version modifier
# Patch FW unpack
# CSS Merger
# Author: Jeremy Xue
# Jeremy.xzm@gmail.com
# Last update: Feb 18, 2015

# define each tarfile name pattern
# define each tarfile location
import os
import shutil
import tarfile
import re
import string
import subprocess
from Queue import Queue
import time

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
                             "copy_acc",
                             ]

        for key in list_of_variables:
            skey = 'self.' + key
            print '{0:<30}{1:<20}'.format(skey, kwarg.get(key))
            exec('%s=%s' % (eval('skey'), 'kwarg.get(key)')) # Trick to auto assign a list of variables
##########################################################################################################
#           end of auto assign list of variables                                                         #
##########################################################################################################
        #print '{0:<30}{1:<20}'.format(self.copy_acc, copy_acc)
        #self.copy_acc = copy_acc

        self._dt = self.package_date + '_' + self.package_hr

        #package folder full name i.e. irci_master_20140715_1500
        self.folder_irci_master = 'irci_master' + '_' + self._dt

        # this is used for skycam css_fw.bin, set fw_sub_folder = 'firmware.target\\firmware'
        self.fw_sub_folder = fw_sub_folder
        # also used for skycam, since zipped package name is different than folder package name.
        self.alt_package_name = alt_package_name
        self.full_alt_package_name = self.alt_package_name + self._dt

        self.remote_path_irci_master = self.remote_path + '\\' + self.folder_irci_master
        self.remote_path_css = self.remote_path_irci_master + '\\'+ 'ifw-ispfw'
        self.remote_path_acc = self.remote_path_irci_master + '\\' + 'ispfw'

        re_remote_AIO_number = re.compile(r'(?<=ia_css_)([0-9]{1,3}\.){3}[0-9]{1,3}(?=_irci.*windows)')
        self.remote_AIO_number = ''
        if self.fw_name == 'AIO':
            for i in os.listdir(self.remote_path_css):
                find_AIO_number = re_remote_AIO_number.search(i)
                if find_AIO_number: #use new fn_package name
                    print '=' * 30
                    print 'old self.package_fn is ', self.package_fn
                    print find_AIO_number.group()
                    self.package_fn = re.sub(r'(?<=ia_css_)([0-9]{1,3}\.){3}[0-9]{1,3}(?=_irci)', find_AIO_number.group(), self.package_fn)
                    print 'new self.package_fn is ', self.package_fn
                    print '=' * 30
                    break

        #package_full_name  i.e. sh_css_sw_hive_isp_css_2400_system_irci_master_20140715_1500.windows.tar.gz
        self.package_full_name = self.package_fn + self._dt + self.package_extension

        self.remote_path_css_file = self.remote_path_css + '\\' + self.package_full_name

        self.daily_folder_path = self.local_path + '\\' + self.daily_folder + '\\' + self.irci
        self.acc_folder_path = self.daily_folder_path + '\\' + 'acc'
        self.local_path_file = self.daily_folder_path + '\\' + self.package_full_name



        if not os.path.exists(self.daily_folder_path):
            os.makedirs(self.daily_folder_path)

        self.local_package_folder_name = self.get_package_folder_name()

    def fcopy(self):
        if os.path.exists(self.remote_path_css_file):
            if os.path.exists(self.local_path_file):
                print '{0:25}{2:<100}\n{1:25}{3:<100}'.format('Warning:', 'already exists in:', self.package_full_name, self.daily_folder_path)
            else:
                #os.system('robocopy "%s" "%s" "%s" /NP' % (self.remote_path_css, self.daily_folder_path, self.package_full_name))
                subprocess.call('robocopy "%s" "%s" "%s" /NP' % (self.remote_path_css, self.daily_folder_path, self.package_full_name),shell = True, creationflags=0x08000000)
        else:
            print 'This file does not seem to exist: %s' % self.remote_path_css_file
        if self.copy_acc == 1:
            try:
                subprocess.call('robocopy "%s" "%s" * /NP' % (self.remote_path_acc, self.acc_folder_path),shell = True, creationflags=0x08000000)
            except:
                print 'Failed to copy %s to %s' % (self.remote_path_acc, self.acc_folder_path)

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
        try:
            if os.path.exists(self.local_path_file):
                with tarfile.open(self.local_path_file) as tf:
                    tf.extractall(self.daily_folder_path)
                    #print '_'*125
                    #print 'extract_tar()'
                    print '{0:25}{1:<100}\n{2:25}{3:<100}'.format('Extracted:', self.package_full_name, 'in local folder:', self.daily_folder_path)
            else:
                print '_'*125
                #print 'extract_tar()'
                print '{0:25}{1:<100}\n{2:25}{3:<100}, did you copy the package?'.format('Warning:', self.package_full_name, 'is no in this folder: ', self.daily_folder_path)
        except:
            print 'something went wrong with extract_tar()'

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
                time.sleep(2)
                shutil.move(new_full_css_folder_path, self.daily_folder_path)
            except:
                print 'Can not rename or move, may be files and directory already exists'

        if self.fw_name == '2500':
            extras_2500_folder_path = self.local_package_folder_name + '\\' + 'firmware.extras'
            new_extras_2500_folder_path = self.local_package_folder_name + '\\' + 'CSS_FW_2500_ExtraBinaries'
            if os.path.exists(extras_2500_folder_path):
                print '{0:25}{1:<100}'.format('2500 extra directory:', extras_2500_folder_path)
                print '{0:25}{1:<100}'.format('New 2500 extra directory:', new_extras_2500_folder_path)
                try:
                    os.rename(extras_2500_folder_path, new_extras_2500_folder_path)
                    time.sleep(2)
                    shutil.move(new_extras_2500_folder_path, self.daily_folder_path)
                except:
                    print 'Can not rename or move, may be files and directory already exists'

    def change_AIO_css_file_name(self):
        full_css_file_name_2400 = '\\'.join([self.local_package_folder_name,'bin','css_2400_system', 'css_fw.bin'])
        full_css_file_name_2401 = '\\'.join([self.local_package_folder_name,'bin','css_2401_system', 'css_fw.bin'])
        full_css_file_name_2401_csi2p = '\\'.join([self.local_package_folder_name,'bin','css_2401_csi2p_system', 'css_fw.bin'])

        new_full_css_file_name_2400 = '\\'.join([self.local_package_folder_name,'bin','css_2400_system', 'css_fw_2400.bin'])
        new_full_css_file_name_2401 = '\\'.join([self.local_package_folder_name,'bin','css_2401_system', 'css_fw_2401.bin'])
        new_full_css_file_name_2401_csi2p = '\\'.join([self.local_package_folder_name, 'bin', 'css_2401_csi2p_system', 'css_fw_2401_csi2plus.bin'])

        old_css_file_names = [full_css_file_name_2400,
                             full_css_file_name_2401,
                             full_css_file_name_2401_csi2p
                             ]

        new_css_file_names = [new_full_css_file_name_2400,
                             new_full_css_file_name_2401,
                             new_full_css_file_name_2401_csi2p
                             ]

        name_dict = dict(zip(old_css_file_names, new_css_file_names))

        for old_name, new_name in name_dict.iteritems():
            if os.path.exists(old_name):
                print '{0:25}{1:<100}'.format('\nLocal css file name:', old_name)
                print 'will be changed to:'
                print '{0:25}{1:<100}'.format('New css file name:', new_name)

                os.rename(old_name, new_name)
                shutil.move(new_name, self.daily_folder_path)
            else:
                print 'File not found: %s' % old_name


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

    #copy acc / HDR related
    def extract_tar_acc(self):
        #print self.copy_acc
        if self.copy_acc == 1:
            for root,dir,file in os.walk(self.acc_folder_path):
                for f in file:
                    try:
                        unzip = tarfile.open(root+'\\'+f,'r')
                        unzip.extractall(root)
                    except:
                        print 'unable to extract: ', f

    def rename_move_css_folder_file(self):
        Q = Queue()
        Q.put(self.fcopy())
        Q.put(self.get_tar_extension())
        Q.put(self.extract_tar())
        Q.put(self.extract_tar_acc())
        time.sleep(5) #make sure all tars are unzipped
        Q.put(self.change_css_folder_name())
        if self.fw_name == 'AIO': #for AIO only
            Q.put(self.change_AIO_css_file_name())
        else:
            Q.put(self.change_css_file_name())
        #shutil.rmtree(self.local_package_folder_name)


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
        pkg_2400 = re.compile('^sh_css_sw_hive_isp_css_2400_system_(()|irci_master_|ci_gerrit_)\d{1,8}_\d{1,4}\.windows$')#'^sh_css_sw_hive_isp_css_2400_system_(irci_master|ci_gerrit)_\d{1,8}_\d{1,4}\.windows$')
        pkg_2401 = re.compile('^sh_css_sw_hive_isp_css_2401_system_(()|irci_master_|ci_gerrit_)\d{1,8}_\d{1,4}\.windows$')#'^sh_css_sw_hive_isp_css_2401_system_(irci_master|ci_gerrit)_\d{1,8}_\d{1,4}\.windows$')
        pkg_2401_csi2plus = re.compile('^sh_css_sw_csi2plus_hive_isp_css_2401_system_(()|irci_master_|ci_gerrit_)\d{1,8}_\d{1,4}\.windows$')#'^sh_css_sw_csi2plus_hive_isp_css_2401_system_(.{0}|irci_master|ci_gerrit)_\d{1,8}_\d{1,4}\.windows$')
        pkg_2500 = re.compile('^sh_css_sw_css_skycam_c0_system_(()|irci_master_|ci_gerrit_)\d{1,8}_\d{1,4}')#'^sh_css_sw_css_skycam_a0t_system_(()|irci_master|ci_gerrit)_\d{1,8}_\d{1,4}')
        pkg_2600 = re.compile('tmp')


        if pkg_2400.search(fn): return fn, '2400'
        if pkg_2401.search(fn): return fn, '2401'
        if pkg_2401_csi2plus.search(fn): return fn, '2401_csi2plus'
        if pkg_2500.search(fn): return fn, '2500'
        if pkg_2600.search(fn): return fn, '2600'


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
        except Exception as e:
            print 'unable to rename: ', e

        print 'moving {} to {}'.format(new_css_folder, os.getcwd())
        print 'moving {} to {}'.format(new_css_fw, os.getcwd())
        try:
            shutil.move(new_css_folder, os.getcwd()) # getcwd should return self.inc_pkg_path
            shutil.move(new_css_fw,os.getcwd())
            if self.delete_pkg == 'yes':
                shutil.rmtree(folder)
        except Exception as e:
            print 'unable to move css folder or css fw: ', e

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
        try:
            for pkg in self.get_pkgs():
                with tarfile.open(pkg) as tf:
                    print 'unzipping...%s' % pkg
                    tf.extractall(os.getcwd())
        except:
            print 'Error unzipping: ', Exception

    #func to get date and time out of a package name
    def get_dt(self, fn):
        find_date = re.compile('_\d{1,8}(?=_\d{1,4}\.)')#('\d{8}(?=_\d{4}\.)')
        find_time = re.compile('(?<=\d_)\d{4}(?=\.)')#'(?<=\d{8}_)\d{4}(?=\.)')
        find_dt = re.compile('\d{1,8}_\d{1,4}(?=\.)')#'\d{8}_\d{4}(?=\.)')
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
        time.sleep(5) #make sure all unzips are completed
        for flder in self.get_folders():
            print flder
            try:
                fn, id = self.id_folders(flder)
                # used for skycam
                if id == '2500':
                    css_fw_folder = 'firmware.target\\firmware'
                else:
                    css_fw_folder = ''
                self.change_move_folder_fw(fn, id, css_fw_folder)
            except:
                print 'exception occured during unzip_rename_move ', flder

##################################################################################################################
#                                                                                                                #
#                                   C S S    V E R S I O N   C H A N G E                                         #
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
        self.new_css_date = '{}-{}-{}  integration:'.format(self.daily_folder[0:4],self.daily_folder[4:6],self.daily_folder[6:8])
        self.new_css_version = self.daily_folder + '_' + self.package_hr
        self.css_version_path_tmp = self.css_version_path + '.tmp'

    def read_write_file(self, new_date='', new_line=''):
        with open(self.css_version_path_tmp,'wb+') as css_file_tmp:
            css_file_tmp.write(new_date+'\n')
            css_file_tmp.write(new_line+'\n')
            print new_date
            print new_line
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
#                           C S S         M E R G E                                                              #
#                                                                                                                #
##################################################################################################################
class css_merge:
    def __init__(self, sha = 'master', **kwargs):
        self.Q = Queue()

        self.sha = sha
        self.source_folder = kwargs.get('source_folder') #C:\JX_Projects\vieddrv-trunk\camerasw\Source
        self.fw_name = kwargs.get('fw_name')
        self.local_path = kwargs.get('local_path')
        self.daily_folder = kwargs.get('daily_folder')
        self.irci = kwargs.get('irci')
        self.merge_acc = kwargs.get('merge_acc')
        self.cmd_exe = r'%systemroot%\system32\cmd.exe'
        #self.sh_exe = r'e:\git\bin\sh.exe'
        self.sh_exe = r'"C:\Program Files (x86)\Git\bin\sh.exe"'
        #self.git_bash_script = os.path.join(self.source_folder, 'git_bash.sh')
        self.git_bash_script = string.join([self.source_folder.split('\\')[0],self.source_folder.split('\\')[1],'git_bash.sh'],'\\') #C:\JX_Projects\git_bash.sh
        self.git_bash_log = string.join([self.source_folder.split('\\')[0],self.source_folder.split('\\')[1],'git_bash.log'],'\\') #C:\JX_Projects\git_bash.log

        if self.daily_folder == None:
            self.daily_folder_path = self.local_path
        else:
            self.daily_folder_path = self.local_path + '\\' + self.daily_folder + '\\' + self.irci

        self.source_package_path = self.source_folder +'\\' + 'camera\\isp\\css\\' + self.fw_name
        self.fw_package_path = self.daily_folder_path + '\\' + self.fw_name

        #if os.path.exists(self.source_package_path) == False or os.path.exists(self.fw_package_path) == False:
        #    print 'shit'

        if os.path.exists(self.git_bash_log): #start with a clean log
            os.remove(self.git_bash_log)

        self.otm_file_ignore_list = [self.source_package_path + '\\' + 'css_version.txt',
                                     self.source_package_path + '\\' + 'css_' + self.fw_name + '.vcxproj',
                                     self.source_package_path + '\\' + 'css_' + self.fw_name + '.vcxproj.filters',
                                     self.source_package_path + '\\' + 'css' + self.fw_name + '.props',
                                     self.source_package_path + '\\' + 'shcss.vcxproj']

        #C:\JX_Projects\vieddrv-trunk\camerasw\Source\Camera\ISP\css
        #C:\JX_Projects\vieddrv-trunk\camerasw\Source\Camera\ISP\firmware
        #C:\JX_Projects\vieddrv-trunk\camerasw\Source\Camera\ISP\firmware\CSS_FW_2500_ExtraBinaries
        #C:\JX_Projects\vieddrv-trunk\camerasw\Source\Camera\ISP\firmware\acc\hdr
        #
        #F:\daily_integration\20150126\1064\css_fw_2401_csi2plus.bin
        #F:\daily_integration\20150126\1064\sh_css_sw_css_skycam_c0_system_irci_master_20150126_1500\firmware.extras
        #F:\daily_integration\20150126\1064\acc\bin

    def __del__(self):
        print 'good bye!'

    def path_win_to_unix(self, win_path):
        unix_path = win_path.replace(':','') #c:\windows\system to /c/windows/system
        unix_path = unix_path.replace('\\','/')
        unix_path = '/' + unix_path
        return unix_path

    def git_bash_call(self, script_path): #call git bash script
        if os.path.exists(script_path) == True:
            final_script = self.cmd_exe + ' /c ' + self.sh_exe + ' --login -i -- ' + script_path
            print "Executing command: %s" % final_script
            p = subprocess.Popen(final_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            o, e = p.communicate()
            if o:
                print o
            if e:
                print "The command encountered an error: %s" % e

    def create_bash(self, bash_content): #create git bash script under C:\JX_Projects\git_bash.sh
        print '\n\nbash command to be created:'
        print bash_content
        print '\n'
        try:
            os.remove(self.git_bash_script) #remove current git bash before creating a new one
        except OSError as e:
            print "Creating %s" % self.git_bash_script

        with open(self.git_bash_script, 'w+') as bs:
            bs.write(bash_content)

        return self.git_bash_script


    def bs_git_checkout(self): #bash script for git checkout at source folder and return the path to such script
        bash_command = '''cd %s
git checkout %s
git pull -v
cd ..
git pull -v''' % (self.sha, self.path_win_to_unix(self.source_folder))

        self.git_bash_call(self.create_bash(bash_command))


    def bs_git_clean_source(self):
        bash_command = '''cd %s
git clean -xfd''' % self.path_win_to_unix(self.source_folder)

        self.git_bash_call(self.create_bash(bash_command))


    def bs_git_clean(self):
        bash_command = '''cd %s
git clean -xfd''' % self.path_win_to_unix(self.source_package_path)

        self.git_bash_call(self.create_bash(bash_command))

    def bs_git_log_10_lines(self):
        bash_command = '''cd %s
git log --oneline -n10''' % self.path_win_to_unix(self.source_package_path)

        self.git_bash_call(self.create_bash(bash_command))


    def check_unique_files(self): #main function: check unique files from OTM trunk and fw package and log them
        with open(self.git_bash_log, 'a+') as gbl:
            gbl.write('\nObsolete file(s) in otm trunk\n') #start with otm trunk, and they will get removed from the folder and vcxproj list
            print "\nObsolete file(s)"
            for unique_file, otm_path, fw_dir in self.unique_files(self.source_package_path, self.fw_package_path):

                ignore_this_file = False
                for i in self.otm_file_ignore_list:
                    if otm_path.lower() == i.lower():
                        ignore_this_file = True #if any one of the file in the list, then we ignore it
                        print "file ignored: %s" % otm_path.lower()

                if ignore_this_file == False:
                    print unique_file.lower()
                    print i.lower()
                    gbl.writelines(unique_file + '\n')
                    #os.remove(unique_file) #let's not remove them, yet

            gbl.write('\nNew file(s) in fw package\n') #new files from fw package, will move them to otm trunk
            print "\nNew file(s)"
            for new_file, new_file_path, dst_dir in self.unique_files(self.fw_package_path, self.source_package_path):
                gbl.write(new_file + '\n')
                print new_file
                if os.path.exists(dst_dir) == False:
                    os.mkdir(dst_dir)
                shutil.copy(new_file_path, dst_dir)

    def copy_modified_files(self):
        pass

    def unique_files(self, a, b): #verified  with beyond compare
        for rs, ds, fs in os.walk(a):
            for f in fs:
                a_path = string.join([rs,f],'\\')
                b_dir = rs.replace(a, b)
                b_path = a_path.replace(a, b)
                if os.path.exists(b_path) == False:
                    yield f, a_path, b_dir

    def common_files(self, a, b): # files with same name shared in both folders, verified  with beyond compare
        for rs, ds, fs in os.walk(a):
            for f in fs:
                a_path = string.join([rs,f],'\\')
                b_path = a_path.replace(a, b)
                if os.path.exists(b_path) == True:
                    yield a_path

    def remove_and_log_empty_folders(self): #main function to clean up empty folders from FW package.
        with open(self.git_bash_log, 'a+') as gbl:
            gbl.write('\nEmpty folders removed:\n')
            print "\nEmpty folders removed:"
            for empty_folder in self.remove_empty_folders(self.source_package_path):
                gbl.write(empty_folder + '\n')
                print empty_folder
            for empty_folder in self.remove_empty_folders(self.fw_package_path):
                gbl.write(empty_folder + '\n')
                print empty_folder

    def remove_empty_folders(self, folder_path):
        rerun = 1 #must have to start hte empty folder hunting
        while rerun > 0:
            rerun = 0 #assume we don't need to rerun it
            for r, d, f in os.walk(folder_path):
                if len(os.listdir(r)) < 1:
                    os.rmdir(r)
                    rerun = rerun + 1
                    yield r

    def compare_a_b(self, file_a, file_b): #single file comparison
        with open(file_a,'rU') as A:
            with open(file_b,'rU') as B:
                return [line for line in A.read().split('\n') if line.strip()] == [line for line in B.read().split('\n') if line.strip()]

    def diff_files(self, a, b): #compare files from two folders and yield the file path from folder 'a' if file is found to be different in content
        for rs, ds, fs in os.walk(a):
            for f in fs:
                a_path = string.join([rs,f],'\\')
                b_path = a_path.replace(a, b)
                if os.path.exists(b_path) == True:
                    #print a_path, b_path
                    if self.compare_a_b(a_path,b_path) == False:
                        yield a_path, b_path

    def test(self):
        print self.fw_name
        print self.daily_folder_path
        print self.source_package_path
        print self.fw_package_path
        print self.merge_acc

        self.Q.put(self.bs_git_clean())
        #self.Q.put(self.remove_and_log_empty_folders())
        self.Q.put(self.check_unique_files())



##################################################################################################################
#                                                                                                                #
#                           B U I L D             F I R M W A R E                                                #
#                                                                                                                #
##################################################################################################################

class BuildFW(css_merge):
    def __init__(self, sha = 'master', **kwargs):
        self.source_folder = kwargs.get('source_folder')
        pass
