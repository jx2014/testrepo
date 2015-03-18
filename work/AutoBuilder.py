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

import Tkinter as tk
import ConfigParser
from file_construct import fc, css_version_file, active_fc, css_merge
from test_gui2 import controlPanel
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

class AutoBuildPanel(controlPanel):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ConfigFile = os.getcwd() + '\\' + 'path_config.ini'
        self.config = ConfigParser.ConfigParser()
        self.File2Memory()
        self.constructUI()
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

    def load(self):
        #try:
        self.ConfigFile = self.e_configFile.get()
        self.File2Memory()
        self.Memory2UI()
        print 'loaded from ' + self.ConfigFile
        #except:
        #    print 'Unable to load from {}'.format(self.ConfigFile)

    def save(self):
        #try:
        self.ConfigFile = self.e_configFile.get()
        self.UI2Memory()
        self.Memory2File()
        print 'saved to ' + self.ConfigFile
        #except:
#            raise Exception
#            print 'Unable to save to {}'.format(self.ConfigFile)

    def constructUI(self):#initialize from File to UI
        self.pack()
        self.pack(side = 'right')
        self.pack(fill='both')
        self.pack(expand=1)

        # Those columns are used to set column width
        l_column0 = tk.Label(self, text='', width=10).grid(row=0, column=0)
        l_column1 = tk.Label(self, text='', width=30).grid(row=0, column=1)
        l_column2 = tk.Label(self, text='', width=30).grid(row=0, column=2)
        l_column3 = tk.Label(self, text='', width=30).grid(row=0, column=3)

        l_SourcePath = tk.Label(self, text='Source path')
        l_SourcePath.grid(row=22, column=0, sticky='w')
        self.e_SourcePath = tk.Entry(self)
        self.e_SourcePath.insert(0, self.source_path)
        self.e_SourcePath.grid(row=22, column=1, columnspan=2, sticky='we')

        l_BinaryPath = tk.Label(self, text='Binary Path')
        l_BinaryPath.grid(row=23, column=0, sticky='w')
        self.e_BinaryPath = tk.Entry(self)
        self.e_BinaryPath.insert(0, self.binary_path)
        self.e_BinaryPath.grid(row=23, column=1, columnspan=2, sticky='we')

        l_SharePath = tk.Label(self, text='Share Path')
        l_SharePath.grid(row=24, column=0, sticky='w')
        self.e_SharePath = tk.Entry(self)
        self.e_SharePath.insert(0, self.share_path)
        self.e_SharePath.grid(row=24, column=1, columnspan=2, sticky='we')

        self.e_configFile = tk.Entry(self)
        self.e_configFile.insert(0, self.ConfigFile)
        self.e_configFile.grid(row=25, column=1, columnspan=2,sticky='we')

        self.b_load = tk.Button(self, text='load', command=self.load, width=10).grid(row=25, column=0, sticky='w')
        self.b_save = tk.Button(self, text='save', command=self.save, width=10).grid(row=26, column=0, sticky='w')

        #self.t_outputBox = tk.Text(self,height=1)
        #self.t_outputBox.grid(row=20, rowspan=2, column=0, columnspan=2, sticky='nsew')


       # self.scrollbar = tk.Scrollbar(self)
       # self.scrollbar.config(command=self.t_outputBox.yview)
       # self.scrollbar.grid(row=20, rowspan=2, column=4, sticky='ns')
        #self.scrollbarError = tk.Scrollbar(self)
        #self.scrollbarError.config(command=self.t_outputBoxError.yview)
        #self.scrollbarError.grid(row=21, column=5, sticky='ns')
       # self.t_outputBox.config(yscrollcommand=self.scrollbar.set)
        #self.t_outputBoxError.config(yscrollcommand=self.scrollbarError.set)

        #sys.stderr = StdError_redirector(self.t_outputBoxError)
       # sys.stderr = StdError_redirector(self.t_outputBox)
        #sys.stdout = Std_redirector(self.t_outputBox)

def main():
    root = tk.Tk()
    root.geometry('600x600+5+5')
    root.title('Windows AutoBuilder')
    app = AutoBuildPanel(root)
    root.mainloop()

if __name__ == '__main__':
    main()