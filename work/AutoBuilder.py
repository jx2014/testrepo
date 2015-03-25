# GUI for:
#  Auto Builder
#  User past a list of git sha commit ids
#  Click build
#  Scripts will checkout to first commit id, git clean -xfd, then build
#  when build is done, rename bins to project.shaID,
#  then check build log for error(s), if no error, move project.shaID folder to share drive.
# Author: Jeremy Xue
# Jeremy.xzm@gmail.com
# Last update: Mar 17, 2015

import re
import Tkinter as tk
import ConfigParser
from file_construct import fc, css_version_file, active_fc, css_merge, BuildFW
from test_gui2 import controlPanel, StdError_redirector, Std_redirector
import subprocess
import sys
import os
from Queue import Queue
from sets import Set

class AutoBuildPanel(controlPanel):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ConfigFile = os.getcwd() + '\\' + 'path_config.ini'
        self.config = ConfigParser.ConfigParser()
        self.File2Memory()
        self.ConstructUI()
        self.parent = parent

    def File2Memory(self):#from file to memory AutoBuilder version
        with open(self.ConfigFile) as dcf:
            self.config.readfp(dcf)

            #[auto_builder]
            #share_path = \\winterfell.sc.intel.com\winterfell-shared
            #source_path = C:\JX_Projects\vieddrv-trunk\camerasw\Source
            #binary_path = C:\JX_Projects\vieddrv-trunk\camerasw\bins

            self.share_path = self.config.get('auto_builder', 'share_path')
            self.source_path = self.config.get('auto_builder', 'source_path')
            self.binary_path = self.config.get('auto_builder', 'binary_path')

    def Memory2File(self):#from memory to file
        #self.config.read(self.ConfigFile)

        auto_builder_info = {
                           'share_path':self.share_path,
                            'source_path':self.source_path,
                            'binary_path':self.binary_path,
                            }

        self.add_section('auto_builder', auto_builder_info, self.config)

        with open(self.ConfigFile,'w+') as cfs:
            self.config.write(cfs)

    def UI2Memory(self):#from UI to memory
        self.share_path = self.e_SharePath.get()
        self.source_path = self.e_SourcePath.get()
        self.binary_path = self.e_BinaryPath.get()

    def Memory2UI(self):#from memory to UI
       self.e_SharePath.delete(0, 'end')
       self.e_SourcePath.delete(0, 'end')
       self.e_BinaryPath.delete(0, 'end')

       self.e_SharePath.insert(0, self.share_path)
       self.e_SourcePath.insert(0, self.source_path)
       self.e_BinaryPath.insert(0, self.binary_path)

    def GetShas(self): #get SHAs from input box
        shas = self.t_shas.get(1.0, 'end')
        shas = shas.split('\n')
        sha_only = re.compile('([0-9]|[a-f]){7}')
        self.drv_shas = Set()
        for line in shas:
            sha_string = sha_only.match(line)
            if sha_string:
                self.drv_shas.add(sha_string.group(0))
                #print sha_string.group(0)

    def GetFW(self):
        self.buildFWs = Set()
        if self.var_2400.get() == 1:
            self.buildFWs.add('BYT')
        if self.var_2401c2p.get() == 1:
            self.buildFWs.add('CHT')
        if self.var_2500.get() == 1:
            self.buildFWs.add('SKC')
        if self.var_2600.get() == 1:
            self.buildFWs.add('BXT')

    def Checkout(self, sha):
        checkout = css_merge(
              #package_code = fw, #probably not needed
              sha = sha,
              fw_name = '',
              daily_folder = '',
              irci = '',
              local_path = '',
              source_folder = self.source_path,
              merge_acc = ''
              )

        checkout.bs_git_checkout()
        checkout.bs_git_clean_source()
        checkout.bs_git_log_1_lines()

    def CheckoutMaster(self):
        print 'you pressed CheckoutMaster button'
        #self.Checkout('master')

    def CleanBuilds(self):
        pass

    def BuildScript(self):
        pass


    def Build(self):
        #text = self.t_shas.get();
        self.t_outputBox.delete(1.0, 'end')
        self.GetShas()
        self.GetFW()

        if len(self.buildFWs) > 0:
            #print '\nFW to be built: ', self.buildFWs
            #print '\nDRV SHAs: ', self.drv_shas
            for sha in self.drv_shas:
                #self.Checkout(sha)
                for fw in self.buildFWs:
                    folderName = '.'.join([fw, sha])
                    buildScript = self.config.get('build_scripts', fw)
                    build = BuildFW(source_folder = self.source_path, build_script = buildScript, folder_name = folderName)
                    build.Build()
        else:
            print '\nNo FW selected.\nPlease check at least one FW to build'


    def ConstructUI(self):#initialize from File to UI
        self.pack()
        self.pack(side = 'right')
        self.pack(fill='both')
        self.pack(expand=1)

        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(15,weight=1)
        self.grid_columnconfigure(2,weight=1)

        # Those columns are used to set column width
        l_column0 = tk.Label(self, text='', width=10).grid(row=0, column=0)
        l_column1 = tk.Label(self, text='', width=10).grid(row=0, column=1)
        l_column2 = tk.Label(self, text='', width=30).grid(row=0, column=2)
        #l_column3 = tk.Label(self, text='', width=30).grid(row=0, column=3)


        #shas text box related stuff
        self.t_shas = tk.Text(self)

        welcomeText = r'''******************** WELCOME ***********************
Copy and Paste a list of Driver commit SHAs into this text box,
check FW package box, then Click Build (i.e)

b0e8be5a6f6c8ea033afc5ddbae856c76930df2e Merge 'Add auto format C:'
a06f9fad6ffd0a78c4c674c380ed78f7eff5870a Merge 'Doomsday deadman switch'
a666f3d Merge 'More regression from Driver team'

When build is done, drivers will be copied to: (i.e
\\winterfell\winterfell-shared\20150318
\CHT.b0e8be5
\CHT.a06f9fa
\CHt.a666f3d
\SKC.b0e8be5
\SKC.a06f9fa
\SKC.a666f3d'''

        l_shas = tk.Label(self,
                          text='''Copy Paste
driver SHAs
to here:''',
                          width=10,
                          justify='left',
                          )
        l_shas.grid(row=2, column=0, sticky='w')

        self.sb_shas_y = tk.Scrollbar(self)
        self.sb_shas_y.config(command=self.t_shas.yview)
        self.sb_shas_y.grid(row=2, column=3, sticky='wns')

        self.sb_shas_x = tk.Scrollbar(self)
        self.sb_shas_x.config(command=self.t_shas.xview, orient='horizontal', relief='flat')
        self.sb_shas_x.grid(row=13, column=1, columnspan=2, sticky='we')

        self.t_shas.config(yscrollcommand=self.sb_shas_y.set, xscrollcommand=self.sb_shas_x.set, wrap='none')
        self.t_shas.grid(row=2, column=1, columnspan=2, sticky='we')
        self.t_shas.insert('insert', welcomeText)
        #end of sha box related stuff, end row shall be row 13.


        l_row14 = tk.Label(self, text='', width=10).grid(row=14, column=0)


        #output text box related
        self.t_outputBox = tk.Text(self)

        l_output = tk.Label(self,
                          text='''Output:''',
                          width=10,
                          justify='left',
                          )
        l_output.grid(row=15, column=0, sticky='w')

        self.sb_outputBox_y = tk.Scrollbar(self)
        self.sb_outputBox_y.config(command=self.t_outputBox.yview)
        self.sb_outputBox_y.grid(row=15, column=3, sticky='wns')

        self.sb_outputBox_x = tk.Scrollbar(self)
        self.sb_outputBox_x.config(command=self.t_outputBox.xview, orient='horizontal', relief='flat')
        self.sb_outputBox_x.grid(row=20, column=1, columnspan=2, sticky='we')

        self.t_outputBox.config(yscrollcommand=self.sb_outputBox_y.set, xscrollcommand=self.sb_outputBox_x.set, wrap='none')
        self.t_outputBox.grid(row=15, column=1, columnspan=2, sticky='nswe')
        #end of output text box


        l_row21 = tk.Label(self, text='', width=10).grid(row=22, column=0)

        self.var_2400 = tk.IntVar()
        self.var_2401c2p = tk.IntVar()
        self.var_2500 = tk.IntVar()
        self.var_2600 = tk.IntVar()
        self.var_win8 = tk.IntVar()
        self.var_win10 = tk.IntVar()
        self.var_x86 = tk.IntVar()
        self.var_x64 = tk.IntVar()

        self.c_2400 = tk.Checkbutton(self, text='2400', variable=self.var_2400).grid(row=23, column=1, sticky='w')
        self.c_2401C2P = tk.Checkbutton(self, text='2401C2P', variable=self.var_2401c2p).grid(row=23, column=2, sticky='w')
        self.c_2500 = tk.Checkbutton(self, text='2500', variable=self.var_2500).grid(row=24, column=1, sticky='w')
        self.c_2600 = tk.Checkbutton(self, text='2600', variable=self.var_2600).grid(row=24, column=2, sticky='w')

        self.c_win8 = tk.Checkbutton(self, text='Win8', variable=self.var_win8).grid(row=21, column=1, sticky='w')
        self.c_win10 = tk.Checkbutton(self, text='Win10', variable=self.var_win10).grid(row=22, column=1, sticky='w')
        self.c_x86 = tk.Checkbutton(self, text='x86', variable=self.var_x86).grid(row=21, column=2, sticky='w')
        self.c_x64 = tk.Checkbutton(self, text='x64', variable=self.var_x64).grid(row=22, column=2, sticky='w')

        l_SourcePath = tk.Label(self, text='Source path')
        l_SourcePath.grid(row=25, column=0, sticky='w')
        self.e_SourcePath = tk.Entry(self)
        self.e_SourcePath.insert(0, self.source_path)
        self.e_SourcePath.grid(row=25, column=1, columnspan=2, sticky='we')

        l_BinaryPath = tk.Label(self, text='Binary Path')
        l_BinaryPath.grid(row=26, column=0, sticky='w')
        self.e_BinaryPath = tk.Entry(self)
        self.e_BinaryPath.insert(0, self.binary_path)
        self.e_BinaryPath.grid(row=26, column=1, columnspan=2, sticky='we')

        l_SharePath = tk.Label(self, text='Share Path')
        l_SharePath.grid(row=27, column=0, sticky='w')
        self.e_SharePath = tk.Entry(self)
        self.e_SharePath.insert(0, self.share_path)
        self.e_SharePath.grid(row=27, column=1, columnspan=2, sticky='we')

        self.e_configFile = tk.Entry(self)
        self.e_configFile.insert(0, self.ConfigFile)
        self.e_configFile.grid(row=28, column=1, columnspan=2,sticky='we')

        self.b_load = tk.Button(self, text='load', command=self.Load, width=10).grid(row=28, column=0, sticky='w')
        self.b_save = tk.Button(self, text='save', command=self.Save, width=10).grid(row=29, column=0, sticky='w')
        self.b_checkoutMaster = tk.Button(self, text='Checkout\nMaster', command=self.CheckoutMaster, width=10, height=3, bg='yellow')
        self.b_checkoutMaster.grid(row=29, column=1, rowspan=2, sticky='w')
        self.b_build = tk.Button(self, text='build', command=self.Build, width=10, bg='dark green', fg='ivory1').grid(row=30, column=0, sticky='w')

        sys.stderr = StdError_redirector(self.t_outputBox)
        sys.stdout = Std_redirector(self.t_outputBox)

def main():
    root = tk.Tk()
    root.geometry('600x600+5+5')
    root.title('Windows AutoBuilder')
    app = AutoBuildPanel(root)
    root.mainloop()

if __name__ == '__main__':
    main()


#
# import re
# name = re.compile(r'(?<=<tr><td>)[a-z0-9]*(?=</td>)')
# name_list = []
#
# def html2list(row):
#     trtd = '<tr><td>|</td></tr>|<td>'
#     #oneRow = r'<tr><td>salamat123</td><td>column2</td><td>column3</td><td>column4</td></tr>'
#     listFromRow = re.sub(trtd, '', row).split('</td>')
#     return listFromRow
#
#
#
# msgbody = [r'<tr><td>salamat123</td><td>column2</td><td>column3</td><td>column4</td></tr>',
#            r'<tr><td>brandon</td><td>column2</td><td>column3</td><td></td></tr>',
#            r'<tr><td>zjerex</td><td>column2</td><td>column3</td><td>column4</td></tr>']
#
#
# for msg in msgbody:
#     name_found = name.search(msg)
#     print html2list(msg)
#     if name_found is not None:
#         name_list.append('@'.join([name_found.group(), 'brandon.com']))





