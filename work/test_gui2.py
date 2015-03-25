# GUI for:
#   FW package download, unzip utility,
#   2400/2401/2401_CSI2PLUS css version modifier
#   Patch FW unpack
#   CSS Merger
# Author: Jeremy Xue
# Jeremy.xzm@gmail.com
# Last update: Feb 18, 2015


import Tkinter as tk
import ConfigParser
from file_construct import fc, css_version_file, active_fc, css_merge
import subprocess
import sys
import os
from Queue import Queue

class StdError_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        self.widget.config(fg='red')
        self.widget.insert(tk.END,string)
        self.widget.see(tk.END)

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        self.widget.config(fg='blue')
        self.widget.insert(tk.END,string)
        self.widget.see(tk.END)

class controlPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ConfigFile = os.getcwd() + '\\' + 'path_config.ini'
        self.config = ConfigParser.ConfigParser()
        self.File2Memory()
        self.ConstructUI()
        self.parent = parent

    def UI2Memory(self):#from UI to memory
        self.daily_folder = self.e_date.get()
        self.irci = self.e_irci.get()
        self.package_hr = self.e_hour.get()
        self.OTMlocal_path = self.e_OTMlocalPath.get()
        self.OTMremote_path = self.e_OTMremotePath.get()
        self.OTMsource_path = self.e_OTMsourcePath.get()
        self.PTagent = self.e_agent.get()
        self.PTbulidLabel = self.e_buildLabel.get()
        self.PTlocal_path = self.e_PTlocalPath.get()
        self.PTremote_path = self.e_PTremotePath.get()
        self.PTsource_path = self.e_PTsourcePath.get()

    def Memory2File(self):#from memory to file
        #self.config.read(self.ConfigFile)

        DailyPatch_info = {
                           'daily_folder':self.daily_folder,
                            'irci':self.irci,
                            'package_hr':self.package_hr,
                            'remote_path':self.OTMremote_path,
                            'local_path':self.OTMlocal_path,
                            'source_path':self.OTMsource_path,
                            'winterfell':self.winterfell_path,
                            'windows_build':self.windowsbuild_path
                            }

        ci_gerrit_info = {
                            'remote_path':self.PTremote_path,
                            'local_path':self.PTlocal_path,
                            'source_path':self.PTsource_path,
                            'agent':self.PTagent,
                            'build_label':self.PTbulidLabel
                            }

        self.add_section('DailyPatch', DailyPatch_info, self.config)
        self.add_section('ci_gerrit', ci_gerrit_info, self.config)

        with open(self.ConfigFile,'w+') as cfs:
            self.config.write(cfs)


    def add_section(self, sectionName, optInfo, config):
        for key in optInfo.keys():
            config.set(sectionName, key, optInfo.get(key))


    def File2Memory(self):#from file to memory
        with open(self.ConfigFile) as dcf:
            self.config.readfp(dcf)

            self.user = self.config.get('path_config', 'user')

            self.daily_folder = self.config.get('DailyPatch', 'daily_folder') #aka package date
            self.irci = self.config.get('DailyPatch', 'irci')
            #self.package_date = self.config.get('DailyPatch', 'package_date')
            self.package_hr = self.config.get('DailyPatch', 'package_hr')

            self.OTMremote_path = self.config.get('DailyPatch', 'remote_path')
            self.OTMlocal_path = self.config.get('DailyPatch', 'local_path')
            self.OTMsource_path = self.config.get('DailyPatch', 'source_path')
            self.winterfell_path = self.config.get('DailyPatch', 'winterfell')
            self.windowsbuild_path = self.config.get('DailyPatch', 'windows_build')

            self.PTremote_path = self.config.get('ci_gerrit', 'remote_path')
            self.PTlocal_path = self.config.get('ci_gerrit', 'local_path')
            self.PTsource_path = self.config.get('ci_gerrit', 'source_path')
            self.PTagent = self.config.get('ci_gerrit', 'agent')
            self.PTbulidLabel = self.config.get('ci_gerrit', 'build_label')

#             self.cssVersion_2400 = self.config.get('css_versions', 'css_2400')
#             self.cssVersion_2401 = self.config.get('css_versions', 'css_2401')
#             self.cssVersion_2401_csi2plus = self.config.get('css_versions', 'css_2401_csi2plus')
#             self.cssVersion_2500 = self.config.get('css_versions', 'css_2500')



    #AutoConfigReader is not used, manually assigning variable names is simpler and safer
    def AutoConfigReader(self,section_name, config):
        '''
            Automatically reads Section Name and it's options then create variables for it in the format of:

                self.SectionName_options

            A list of options for this Section is saved in:

                self.list_SectionName

            To add new Section and Options, add to the end of File2Memory func

                self.AutoConfigReader(self, 'Section Name', config)
        '''
        listOpts = 'self.list_' + section_name
        exec('%s = []' % eval('listOpts'))

        for opt in config.options(section_name):
            varName = 'self.' + section_name + '_' + opt
            exec('%s=config.get(section_name, opt)' % eval('varName'))
            exec('%s.append(%s)' % (eval('listOpts'), 'varName'))

        #print 'listOpts is', listOpts

        for varName in eval(listOpts):
            print varName
            exec('print %s' % (varName))

    def Memory2UI(self):#from memory to UI
        self.e_date.delete(0, 'end')
        self.e_hour.delete(0, 'end')
        self.e_irci.delete(0, 'end')
        self.e_agent.delete(0, 'end')
        self.e_buildLabel.delete(0, 'end')
        self.e_OTMremotePath.delete(0, 'end')
        self.e_OTMlocalPath.delete(0, 'end')
        self.e_OTMsourcePath.delete(0, 'end')
        self.e_PTremotePath.delete(0, 'end')
        self.e_PTlocalPath.delete(0, 'end')
        self.e_PTsourcePath.delete(0, 'end')

        self.e_date.insert(0, self.daily_folder)
        self.e_hour.insert(0, self.package_hr)
        self.e_irci.insert(0, self.irci)
        self.e_agent.insert(0, self.PTagent)
        self.e_buildLabel.insert(0, self.PTbulidLabel)
        self.e_OTMremotePath.insert(0, self.OTMremote_path)
        self.e_OTMlocalPath.insert(0, self.OTMlocal_path)
        self.e_OTMsourcePath.insert(0, self.OTMsource_path)
        self.e_PTremotePath.insert(0, self.PTremote_path)
        self.e_PTlocalPath.insert(0, self.PTlocal_path)
        self.e_PTsourcePath.insert(0, self.PTsource_path)

    def ConstructUI(self):#initialize from File to UI
        self.pack(fill='both', expand=1)
        for i in range(11,24):
            self.grid_rowconfigure(i,pad=1)
        self.grid_rowconfigure(20,weight=1)
        self.grid_rowconfigure(21,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(4,weight=1)

        self.var_2400 = tk.IntVar()
        self.var_2401c2p = tk.IntVar()
        self.var_2500 = tk.IntVar()
        self.var_2600 = tk.IntVar()

        self.var_ACC = tk.IntVar()
        self.var_buildAIO = tk.IntVar()
        self.var_buildBYT = tk.IntVar()
        self.var_buildBXT = tk.IntVar()
        self.var_buildCHTC2P = tk.IntVar()
        self.var_buildSKC = tk.IntVar()

        l_dailyIntegration = tk.Label(self, text = 'Daily Integration',font=(24)).grid(row=1,column=0, columnspan=2,sticky='w')
        l_patchTesting = tk.Label(self, text = 'Patch Testing',font=(24)).grid(row=1,column=3, columnspan=2,sticky='w')
        l_columnSpacer = tk.Label(self, text = ' ').grid(row=1,column=2)

        l_rowSpacer1 = tk.Label(self, text = ' ').grid(row=2,column=0,columnspan=5)
        l_date = tk.Label(self, text='Date')
        l_date.grid(row=3, column=0, sticky='w')
        l_hour = tk.Label(self, text='Hour').grid(row=4, column=0, sticky='w')
        l_irci = tk.Label(self, text='Irci').grid(row=5, column=0, sticky='w')
        l_agent = tk.Label(self, text='Agent').grid(row=3, column=3, sticky='w')
        l_buildLabel = tk.Label(self, text='Build Label').grid(row=4, column=3, sticky='w')

        l_rowSpacer2  = tk.Label(self, text=' ').grid(row=6,column=0, columnspan=4)
        l_OTMremotePath = tk.Label(self, text='Remote path').grid(row=7, column=0, sticky='w')
        l_OTMlocalPath = tk.Label(self, text='Local path').grid(row=8, column=0, sticky='w')
        l_PTremotePath = tk.Label(self, text='Remote path').grid(row=7, column=3, sticky='w')
        l_PTlocalPath = tk.Label(self, text='Local path').grid(row=8, column=3, sticky='w')
        l_OTMsourcePath  = tk.Label(self, text='Source path').grid(row=9, column=0, sticky='w')
        l_PTsourcePath  = tk.Label(self, text='Source path').grid(row=9, column=3, sticky='w')

        l_rowSpacer3  = tk.Label(self, text=' ').grid(row=10, column=0, columnspan=5)
        l_packages2build = tk.Label(self, text='Package(s) to be downloaded and built').grid(row=11, column=3, columnspan=2, sticky='w')


        #l_rowSpacer4  = tk.Label(self, text=' ').grid(row=18, column=0, columnspan=5)

        self.e_date = tk.Entry(self)
        self.e_date.insert(0, self.daily_folder)
        self.e_date.grid(row=3, column=1, sticky='w')

        self.e_hour = tk.Entry(self)
        self.e_hour.insert(0, self.package_hr)
        self.e_hour.grid(row=4, column=1, sticky='w')

        self.e_irci = tk.Entry(self)
        self.e_irci.insert(0, self.irci)
        self.e_irci.grid(row=5, column=1, sticky='w')

        self.e_agent = tk.Entry(self)
        self.e_agent.insert(0, self.PTagent)
        self.e_agent.grid(row=3, column=4, sticky='w')

        self.e_buildLabel = tk.Entry(self)
        self.e_buildLabel.insert(0, self.PTbulidLabel)
        self.e_buildLabel.grid(row=4, column=4, sticky='w')

        self.e_OTMremotePath = tk.Entry(self)
        self.e_OTMremotePath.insert(0, self.OTMremote_path)
        self.e_OTMremotePath.grid(row=7, column=1, sticky='we')

        self.e_OTMlocalPath = tk.Entry(self)
        self.e_OTMlocalPath.insert(0, self.OTMlocal_path)
        self.e_OTMlocalPath.grid(row=8, column=1, sticky='we')

        self.e_OTMsourcePath = tk.Entry(self)
        self.e_OTMsourcePath.insert(0, self.OTMsource_path)
        self.e_OTMsourcePath.grid(row=9, column=1, sticky='we')

        self.e_PTremotePath = tk.Entry(self)
        self.e_PTremotePath.insert(0, self.PTremote_path)
        self.e_PTremotePath.grid(row=7, column=4, sticky='we')

        self.e_PTlocalPath = tk.Entry(self)
        self.e_PTlocalPath.insert(0, self.PTlocal_path)
        self.e_PTlocalPath.grid(row=8, column=4, sticky='we')

        self.e_PTsourcePath = tk.Entry(self)
        self.e_PTsourcePath.insert(0, self.PTsource_path)
        self.e_PTsourcePath.grid(row=9, column=4, sticky='we')

        self.t_outputBox = tk.Text(self,height=1)
        self.t_outputBox.grid(row=20, rowspan=2, column=0, columnspan=5, sticky='nsew')
        #self.t_outputBoxError = tk.Text(self,height=1)
        #self.t_outputBoxError.grid(row=21, column=0, columnspan=5, sticky='nsew')

        self.e_configFile = tk.Entry(self)
        self.e_configFile.insert(0, self.ConfigFile)
        self.e_configFile.grid(row=22, column=1, columnspan=4,sticky='we')

        self.b_GURP = tk.Button(self, text='GURP', command=self.GURP, width=10).grid(row=14, column=0, sticky='w')
        self.b_Checkout = tk.Button(self, text='Checkout', command=self.Checkout, width=15, bg='yellow').grid(row=14, column=1, sticky='w')
        self.b_movePackages = tk.Button(self, text='Merge CSS', command=self.movePackages, width=10).grid(row=15, column=0, columnspan=2, sticky='w')
        self.b_CSSversions = tk.Button(self, text='Version txt', command=self.cssVersions, width=15).grid(row=15, column=1, sticky='w')
        self.b_ShowGitCommands = tk.Button(self, text='Show Git', command=self.ShowGitCommands, width=15).grid(row=16, column=1, sticky='w')
        self.b_build4packages = tk.Button(self, text='Build', command=self.build4packages, width=10).grid(row=16, column=0, sticky='w')

        self.b_getPackages = tk.Button(self, text='Get Packages', command=self.getPackages, width=15).grid(row=14, column=3, columnspan=2, sticky='w')
        self.b_activeUnzip = tk.Button(self, text='Active Unzip', command=self.activeUnzip, width=15).grid(row=15, column=3, columnspan=2, sticky='w')
        self.b_mergeCSS2 = tk.Button(self, text='Merge CSS', command=self.mergeCSS2, width=15).grid(row=15, column=4, sticky='w')
        self.b_buildPackages2 = tk.Button(self, text='Build Package(s)', command=self.buildPackages2, width=15).grid(row=16, column=3, columnspan=2, sticky='w')

        #self.b_buildBYT = tk.Button(self, text='Build BYT', command=self.buildBYT).grid(row=16, column=0, columnspan=2, sticky='we')
        #self.b_buildBXT = tk.Button(self, text='Build BXT', command=self.buildBXT).grid(row=17, column=0, columnspan=2, sticky='we')
        #self.b_buildCHTC2P = tk.Button(self, text='Build CHT CSI2PLUS', command=self.buildCHTC2P).grid(row=18, column=0, columnspan=2, sticky='we')
        #self.b_buildSKC = tk.Button(self, text='Build SKC', command=self.buildSKC).grid(row=19, column=0, columnspan=2, sticky='we')
        self.b_load = tk.Button(self, text='load', command=self.Load, width=10).grid(row=22, column=0, sticky='w')
        self.b_save = tk.Button(self, text='save', command=self.Save, width=10).grid(row=23, column=0, sticky='w')
        self.b_folderDaily = tk.Button(self, text='Daily', command=self.openOTMlocalFolder, width=15).grid(row=23, column=3, sticky='w')
        self.b_folderSource = tk.Button(self, text='Source', command=self.openOTMsourceFolder, width=10).grid(row=23, column=4, sticky='w')
        self.b_folderIncoming = tk.Button(self, text='Incoming', command=self.openPTlocalFolder, width=15).grid(row=24, column=3, sticky='w')
        self.b_folderWinterfell = tk.Button(self, text='Winterfell', command=self.openWinterfellFolder, width=10).grid(row=24, column=4, sticky='w')
        self.b_folderWindowsBuild = tk.Button(self, text='WindowsBuild', command=self.openWindowsbuildFolder, width=15).grid(row=24, column=1, sticky='w')
        self.b_exit = tk.Button(self, text='Exit', command=self.Exit, width=10).grid(row=24, column=0, sticky='w')

        self.c_2400 = tk.Checkbutton(self, text='2400', variable=self.var_2400).grid(row=12, column=3, sticky='w')
        self.c_2401C2P = tk.Checkbutton(self, text='2401C2P', variable=self.var_2401c2p).grid(row=13, column=3, sticky='w')
        self.c_2500 = tk.Checkbutton(self, text='2500', variable=self.var_2500).grid(row=12, column=4, sticky='w')
        self.c_2600 = tk.Checkbutton(self, text='2600', variable=self.var_2600).grid(row=13, column=4, sticky='w')

        self.c_ACC = tk.Checkbutton(self, text='ACC', variable=self.var_ACC)
        self.c_ACC.select()
        self.c_ACC.grid(row=11, column=0, sticky='w')

        self.c_buildAIO = tk.Checkbutton(self, text='All In One', variable=self.var_buildAIO)
        self.c_buildAIO.select()
        self.c_buildAIO.grid(row=11, column=1, sticky='w')

        self.c_buildBYT = tk.Checkbutton(self, text='2400', variable=self.var_buildBYT)
        #self.c_buildBYT.select()
        self.c_buildBYT.grid(row=12, column=0, sticky='w')

        self.c_buildSKC = tk.Checkbutton(self, text='2500', variable=self.var_buildSKC)
        self.c_buildSKC.select()
        self.c_buildSKC.grid(row=13, column=1, sticky='w')

        self.c_buildBXT = tk.Checkbutton(self, text='2600', variable=self.var_buildBXT)
        self.c_buildBXT.grid(row=12, column=1, sticky='w')

        self.c_buildCHTC2P = tk.Checkbutton(self, text='2401C2P', variable=self.var_buildCHTC2P)
        #self.c_buildCHTC2P.select()
        self.c_buildCHTC2P.grid(row=13, column=0, sticky='w')

        #self.c_ACC.grid(row=10, column=0, columnspan=5)
        #self.c_ACC.grid(row=10, column=0, sticky='w')

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.config(command=self.t_outputBox.yview)
        self.scrollbar.grid(row=20, rowspan=2, column=5, sticky='ns')
        #self.scrollbarError = tk.Scrollbar(self)
        #self.scrollbarError.config(command=self.t_outputBoxError.yview)
        #self.scrollbarError.grid(row=21, column=5, sticky='ns')
        self.t_outputBox.config(yscrollcommand=self.scrollbar.set)
        #self.t_outputBoxError.config(yscrollcommand=self.scrollbarError.set)

        #sys.stderr = StdError_redirector(self.t_outputBoxError)
        sys.stderr = StdError_redirector(self.t_outputBox)
        sys.stdout = Std_redirector(self.t_outputBox)

    def openFolder(self, path):
        #os.system('start %s' % path)
        #subprocess.call("start %s" % path, creationflags=0x08000000, shell=True)
        subprocess.call("start %s" % path, shell=True)

    def openOTMsourceFolder(self):
        self.openFolder(self.OTMsource_path)

    def openOTMlocalFolder(self):
        self.openFolder(self.OTMlocal_path)

    def openPTlocalFolder(self):
        self.openFolder(self.PTlocal_path)

    def openWinterfellFolder(self):
        self.openFolder(self.winterfell_path)

    def openWindowsbuildFolder(self):
        self.openFolder(self.windowsbuild_path)

    def Checkout(self):
        checkout = css_merge(
              #package_code = fw, #probably not needed
              fw_name = '',
              daily_folder = self.daily_folder,
              irci = self.irci,
              local_path = self.PTlocal_path,
              source_folder = self.PTsource_path,
              merge_acc = ''
              )

        checkout.bs_git_checkout()
        checkout.bs_git_clean_source()
        checkout.bs_git_log_10_lines()


    def GURP(self):
        self.UI2Memory()

        try:
            BYT_2400 = fc(
                          package_code = '2400', #probably not needed
                          package_fn = 'sh_css_sw_hive_isp_css_2400_system_irci_master_',
                          package_extension = '.windows.tar.gz',
                          fw_name = '2400', #css_fw_2400.bin blah blah
                          #package_date = package_date,
                          package_date = self.daily_folder, # for most of the time, package_date equal to daily_folder date
                          daily_folder = self.daily_folder,
                          package_hr = self.package_hr,
                          remote_path = self.OTMremote_path,
                          irci = self.irci,
                          local_path = self.OTMlocal_path,
                          copy_acc = self.var_ACC.get()
                          )

            BYT_2401 = fc(
                          package_code = '2401', #probably not needed
                          package_fn = 'sh_css_sw_hive_isp_css_2401_system_irci_master_',
                          package_extension = '.windows.tar.gz',
                          fw_name = '2401', #css_fw_2400.bin blah blah
                          #package_date = package_date,
                          package_date = self.daily_folder, # for most of the time, package_date equal to daily_folder date
                          daily_folder = self.daily_folder,
                          package_hr = self.package_hr,
                          remote_path = self.OTMremote_path,
                          irci = self.irci,
                          local_path = self.OTMlocal_path,
                          )

            CHT_2401_csi2plus = fc(
                          package_code = '2401_csi2plus', #probably not needed
                          package_fn = 'sh_css_sw_csi2plus_hive_isp_css_2401_system_irci_master_',
                          package_extension = '.windows.tar.gz',
                          fw_name = '2401_csi2plus', #css_fw_2400.bin blah blah
                          #package_date = package_date,
                          package_date = self.daily_folder, # for most of the time, package_date equal to daily_folder date
                          daily_folder = self.daily_folder,
                          package_hr = self.package_hr,
                          remote_path = self.OTMremote_path,
                          irci = self.irci,
                          local_path = self.OTMlocal_path,
                          )

            AIO = fc(
                          package_code = 'AIO', #probably not needed
                          package_fn = 'ia_css_2.1.14.19_irci_master_',
                          package_extension = '.windows.tar.gz',
                          fw_name = 'AIO', #css_fw_2400.bin blah blah
                          #package_date = package_date,
                          package_date = self.daily_folder, # for most of the time, package_date equal to daily_folder date
                          daily_folder = self.daily_folder,
                          package_hr = self.package_hr,
                          remote_path = self.OTMremote_path,
                          irci = self.irci,
                          local_path = self.OTMlocal_path,
                          copy_acc = self.var_ACC.get()
                          )

            SKC_2500 = fc(
                          package_code = '2500', #probably not needed
                          package_fn = 'css_pkg_css_skycam_c0_system_irci_master_',
                          package_extension = '.tar.gz',
                          fw_name = '2500', #css_fw_2400.bin blah blah
                          #package_date = package_date,
                          package_date = self.daily_folder, # for most of the time, package_date equal to daily_folder date
                          daily_folder = self.daily_folder,
                          package_hr = self.package_hr,
                          remote_path = self.OTMremote_path,
                          irci = self.irci,
                          local_path = self.OTMlocal_path,
                          fw_sub_folder = 'firmware.target\\firmware', #required for skycam
                          alt_package_name = 'sh_css_sw_css_skycam_c0_system_irci_master_' # get it from extracted folder and rid off date time, leave the underscore
                          )

#             BXT_2600_isys = fc(
#                           package_code = '2600', #probably not needed
#                           package_fn = 'css_pkg_bxt_isys_irci_master_',
#                           package_extension = '.windows.tar.gz',
#                           fw_name = '2600', #css_fw_2400.bin blah blah
#                           #package_date = package_date,
#                           package_date = self.daily_folder, # for most of the time, package_date equal to daily_folder date
#                           daily_folder = self.daily_folder,
#                           package_hr = self.package_hr,
#                           remote_path = self.OTMremote_path,
#                           irci = self.irci,
#                           local_path = self.OTMlocal_path,
#                           )
#
#             BXT_2600_psys = fc(
#                           package_code = '2600', #probably not needed
#                           package_fn = 'css_pkg_bxt_psys_irci_master_',
#                           package_extension = '.windows.tar.gz',
#                           fw_name = '2600', #css_fw_2400.bin blah blah
#                           #package_date = package_date,
#                           package_date = self.daily_folder, # for most of the time, package_date equal to daily_folder date
#                           daily_folder = self.daily_folder,
#                           package_hr = self.package_hr,
#                           remote_path = self.OTMremote_path,
#                           irci = self.irci,
#                           local_path = self.OTMlocal_path,
#                           )
        except:
            print 'Something went wrong with GURP function in test_gui2.pyw'

        Q = Queue()

        if self.var_buildBYT.get() == 1:
            Q.put(BYT_2400.rename_move_css_folder_file())
            Q.put(BYT_2401.rename_move_css_folder_file())

        if self.var_buildCHTC2P.get() == 1:
            Q.put(CHT_2401_csi2plus.rename_move_css_folder_file())

        if self.var_buildSKC.get() == 1:
            Q.put(SKC_2500.rename_move_css_folder_file())

        if self.var_buildBXT.get() == 1:
            Q.put(BXT_2600_psys.rename_move_css_folder_file())
            Q.put(BXT_2600_isys.rename_move_css_folder_file())

        if self.var_buildAIO.get() == 1:
            Q.put(AIO.rename_move_css_folder_file())

        self.ShowGitCommands()

    def ShowGitCommands(self):

        print "\nexport MY_INTEGRATION=CP_irci_master_%s_%s" % (self.daily_folder, self.package_hr) #CP_Integration_irci_master_20150202_0457
        print "export MY_INTEGRATION=irci_master_%s_%s_%s" % (self.daily_folder, self.package_hr, self.irci) #20150202_0457_1081
        print "".join(["export USER=", self.user])
        print "git checkout -b remotes/origin/master/${MY_INTEGRATION}"
        print "\ngit commit -s"
        print "CP_Integrated_irci_master_%s_%s" % (self.daily_folder, self.package_hr) #20150202_0457_1081
        print "Integrated_CSSIFW_irci_master_%s_%s_%s[BYT][CHT]" % (self.daily_folder, self.package_hr, self.irci) #20150202_0457_1081
        print "Integrated_CSSIFW_irci_master_%s_%s_%s[SKC]" % (self.daily_folder, self.package_hr, self.irci) #20150202_0457_1081
        print "\ngit push origin HEAD:refs/for/master/${MY_INTEGRATION}"
        print "\ngit branch -m remotes/origin/master/irci_master_%s_%s_%sBYT_CHT" % (self.daily_folder, self.package_hr, self.irci)
        print "git branch -m remotes/origin/master/irci_master_%s_%s_%sSKC\n" % (self.daily_folder, self.package_hr, self.irci)

    def cssVersions(self):
        self.UI2Memory()
        for opt in self.config.options('css_versions'):
            #print opt, self.config.get('css_versions', opt)
            version_file = self.config.get('css_versions', opt)
            exec('%s = css_version_file(package_hr = self.package_hr, daily_folder = self.daily_folder, css_version_path = r"%s")'
                 % (opt, version_file))
            exec('%s.final_wrtie_new_date_css_version()' % opt)

        print 'head Camera/ISP/css/2400/lib/css_version.txt'
        print 'head Camera/ISP/css/2401/lib/css_version.txt'
        print 'head Camera/ISP/css/2401_csi2plus/lib/css_version.txt'
        #print 'head Camera/ISP/css/2500/lib/css_version.txt'

    def movePackages(self):
        fw_names = []
        merge_acc =  0

        if self.var_buildBYT.get() == 1:
            fw_names.append('2400')
            fw_names.append('2401')
        if self.var_buildCHTC2P.get() == 1:
            fw_names.append('2401_csi2plus')
        if self.var_buildSKC.get() == 1:
            fw_names.append('2500')
        if self.var_buildBXT.get() == 1:
            fw_names.append('2600')
        if self.var_ACC.get() == 1:
            merge_acc = 1

        for fw in fw_names:
            print fw
            merge = css_merge(
                          #package_code = fw, #probably not needed
                          fw_name = fw,
                          daily_folder = self.daily_folder,
                          irci = self.irci,
                          local_path = self.OTMlocal_path,
                          source_folder = self.OTMsource_path,
                          merge_acc = merge_acc
                          )

            merge.test()


    def getPackages(self):
        print 'insert','Selected packages to be built'
        if self.var_2400.get() == 1:
            print '2400'
        if self.var_2401c2p.get() == 1:
            print '2401_csi2plus'
        if self.var_2500.get() == 1:
            print '2500'
        if self.var_2600.get() == 1:
            print '2600'
        if self.var_ACC.get() == 1:
            print 'ACC'
        self.t_outputBox.yview('end')

    def activeUnzip(self):
        self.UI2Memory()
        active_unzip_all = active_fc(
                             income_pkg = self.PTlocal_path,
                             delete_pkg = 'no'
                             )
        active_unzip_all.unzip_rename_move()

    def mergeCSS2(self):
        fw_names = []
        merge_acc =  0

        if self.var_2400.get() == 1:
            fw_names.append('2400')
            fw_names.append('2401')
        if self.var_2401c2p.get() == 1:
            fw_names.append('2401_csi2plus')
        if self.var_2500.get() == 1:
            fw_names.append('2500')
        if self.var_2600.get() == 1:
            fw_names.append('2600')
        if self.var_ACC.get() == 1:
            merge_acc = 1

        for fw in fw_names:
            print fw
            merge = css_merge(
                          #package_code = fw, #probably not needed
                          fw_name = fw,
                          daily_folder = self.daily_folder,
                          irci = self.irci,
                          local_path = self.PTlocal_path,
                          source_folder = self.PTsource_path,
                          merge_acc = merge_acc
                          )

            merge.test()

    def buildPackages2(self):
        print 'buildPackages2'

    def build4packages(self):
        print 'build 4 packages'

    def buildBYT(self):
        pass

    def buildBXT(self):
        pass

    def buildCHTC2P(self):
        pass

    def buildSKC(self):
        pass

    def Load(self):
        try:
            self.ConfigFile = self.e_configFile.get()
            self.File2Memory()
            self.Memory2UI()
            print 'loaded from ' + self.ConfigFile
        except:
            print 'Unable to load from {}'.format(self.ConfigFile)

    def Save(self):
        try:
            self.ConfigFile = self.e_configFile.get()
            self.UI2Memory()
            self.Memory2File()
            print 'saved to ' + self.ConfigFile
        except:
            raise Exception
            print 'Unable to save to {}'.format(self.ConfigFile)

    def Exit(self):
        self.parent.destroy()


def main():
    root = tk.Tk()
    root.geometry('600x600+5+5')
    root.title('Windows OTM/Patch build Control Panel II')
    app = controlPanel(root)
    root.mainloop()


if __name__ == '__main__':
    main()