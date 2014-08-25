import Tkinter as tk
import ConfigParser
import sys
import os

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
        self.getPara()
        self.constructUI()
        self.parent = parent

    def getPara(self):
        with open(self.ConfigFile) as dcf:
            config = ConfigParser.ConfigParser()
            config.readfp(dcf)
            self.daily_folder = config.get('DailyPatch', 'daily_folder') #aka package date
            self.irci = config.get('DailyPatch', 'irci')
            #self.package_date = config.get('DailyPatch', 'package_date')
            self.package_hr = config.get('DailyPatch', 'package_hr')

            self.OTMremote_path = config.get('DailyPatch', 'remote_path')
            self.OTMlocal_path = config.get('DailyPatch', 'local_path')
            self.OTMsource_path = config.get('DailyPatch', 'source_path')

            self.PTremote_path = config.get('ci_gerrit', 'remote_path')
            self.PTlocal_path = config.get('ci_gerrit', 'local_path')
            self.PTsource_path = config.get('ci_gerrit', 'source_path')
            self.PTagent = config.get('ci_gerrit', 'agent')
            self.PTbulidLabel = config.get('ci_gerrit', 'build_label')

    def writePara(self):
        config = ConfigParser.ConfigParser()
        pass

    def constructUI(self):
        self.pack(fill='both', expand=1)
        for i in range(10,23):
            self.grid_rowconfigure(i,pad=1)
        self.grid_rowconfigure(19,weight=1)
        self.grid_rowconfigure(20,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(4,weight=1)
#
        self.var_2400 = tk.IntVar()
        self.var_2401c2p = tk.IntVar()
        self.var_2500 = tk.IntVar()
        self.var_2600 = tk.IntVar()

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

        self.t_date = tk.Text(self, height=1)
        self.t_date.insert('insert', self.daily_folder)
        self.t_date.grid(row=3, column=1, sticky='w')

        self.t_hour = tk.Text(self, height=1)
        self.t_hour.insert('insert', self.package_hr)
        self.t_hour.grid(row=4, column=1, sticky='w')

        self.t_irci = tk.Text(self, height=1)
        self.t_irci.insert('insert', self.irci)
        self.t_irci.grid(row=5, column=1, sticky='w')

        self.t_agent = tk.Text(self, height=1)
        self.t_agent.insert('insert', self.PTagent)
        self.t_agent.grid(row=3, column=4, sticky='w')

        self.t_buildLabel = tk.Text(self, height=1)
        self.t_buildLabel.insert('insert', self.PTbulidLabel)
        self.t_buildLabel.grid(row=4, column=4, sticky='w')

        self.t_OTMremotePath = tk.Text(self, height=1)
        self.t_OTMremotePath.insert('insert', self.OTMremote_path)
        self.t_OTMremotePath.grid(row=7, column=1, sticky='we')

        self.t_OTMlocalPath = tk.Text(self, height=1)
        self.t_OTMlocalPath.insert('insert', self.OTMlocal_path)
        self.t_OTMlocalPath.grid(row=8, column=1, sticky='we')

        self.t_OTMsourcePath = tk.Text(self, height=1)
        self.t_OTMsourcePath.insert('insert', self.OTMsource_path)
        self.t_OTMsourcePath.grid(row=9, column=1, sticky='we')

        self.t_PTremotePath = tk.Text(self, height=1)
        self.t_PTremotePath.insert('insert', self.PTremote_path)
        self.t_PTremotePath.grid(row=7, column=4, sticky='we')

        self.t_PTlocalPath = tk.Text(self, height=1)
        self.t_PTlocalPath.insert('insert', self.PTlocal_path)
        self.t_PTlocalPath.grid(row=8, column=4, sticky='we')

        self.t_PTsourcePath = tk.Text(self, height=1)
        self.t_PTsourcePath.insert('insert', self.PTsource_path)
        self.t_PTsourcePath.grid(row=9, column=4, sticky='we')

        self.t_outputBox = tk.Text(self)
        self.t_outputBox.grid(row=19, column=0, columnspan=5, sticky='nsew')
        self.t_outputBoxError = tk.Text(self)
        self.t_outputBoxError.grid(row=20, column=0, columnspan=5, sticky='nsew')

        self.t_configFile = tk.Text(self, height=1)
        self.t_configFile.insert('insert', self.ConfigFile)
        self.t_configFile.grid(row=21,column=1, columnspan=4,sticky='w')

        self.b_GURP = tk.Button(self, text='Get Unzip Rename Packages', command=self.GURP, width=10).grid(row=11, column=0, columnspan=2, sticky='we')
        self.b_CSSversions = tk.Button(self, text='CSS Versions', command=self.cssVersions).grid(row=12, column=0, columnspan=2, sticky='we')
        self.b_movePackages = tk.Button(self, text='Move CSS', command=self.movePackages).grid(row=13, column=0, columnspan=2, sticky='we')
        self.b_getPackages = tk.Button(self, text='Get Packages', command=self.getPackages).grid(row=15, column=3, columnspan=2, sticky='we')
        self.b_activeUnzip = tk.Button(self, text='Active Unzip', command=self.activeUnzip).grid(row=16, column=3, columnspan=2, sticky='we')
        self.b_movePackages2 = tk.Button(self, text='Move CSS', command=self.movePackages2).grid(row=17, column=3, columnspan=2, sticky='we')
        self.b_build4packages = tk.Button(self, text='Build 4 Packages', command=self.build4packages).grid(row=14, column=0, columnspan=2, sticky='we')
        self.b_buildBYT = tk.Button(self, text='Build BYT', command=self.buildBYT).grid(row=15, column=0, columnspan=2, sticky='we')
        self.b_buildBXT = tk.Button(self, text='Build BXT', command=self.buildBXT).grid(row=16, column=0, columnspan=2, sticky='we')
        self.b_buildCHTC2P = tk.Button(self, text='Build CHT CSI2PLUS', command=self.buildCHTC2P).grid(row=17, column=0, columnspan=2, sticky='we')
        self.b_buildSKC = tk.Button(self, text='Build SKC', command=self.buildSKC).grid(row=18, column=0, columnspan=2, sticky='we')
        self.b_load = tk.Button(self, text='load', command=self.load, width=10).grid(row=21, column=0, sticky='we')
        self.b_save = tk.Button(self, text='save', command=self.save, width=10).grid(row=22, column=0, sticky='we')
        self.b_exit = tk.Button(self, text='Exit', command=self.exit, width=10).grid(row=23, column=0, sticky='we')

        self.c_2400 = tk.Checkbutton(self, text='2400', variable=self.var_2400)
        self.c_2400.grid(row=12, column=3, sticky='w')
        self.c_2401C2P = tk.Checkbutton(self, text='2401C2P', variable=self.var_2401c2p).grid(row=13, column=3, sticky='w')
        self.c_2500 = tk.Checkbutton(self, text='2500', variable=self.var_2500).grid(row=12, column=4, sticky='w')
        self.c_2600 = tk.Checkbutton(self, text='2600', variable=self.var_2600).grid(row=13, column=4, sticky='w')

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.config(command=self.t_outputBox.yview)
        self.scrollbar.grid(row=19, column=5, sticky='ns')
        self.scrollbarError = tk.Scrollbar(self)
        self.scrollbarError.config(command=self.t_outputBoxError.yview)
        self.scrollbarError.grid(row=20, column=5, sticky='ns')
        self.t_outputBox.config(yscrollcommand=self.scrollbar.set)
        self.t_outputBoxError.config(yscrollcommand=self.scrollbarError.set)

        sys.stderr = StdError_redirector(self.t_outputBoxError)
        sys.stdout = Std_redirector(self.t_outputBox)

    def GURP(self):
        var = self.t_date.get('0.0','end-1c')
        text = self.t_date.get('0.0','end')
        print var + 'abc'
        self.t_outputBox.yview('end')

    def cssVersions(self):
        print 'css versions'

    def movePackages(self):
        print 'move packages'

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
        self.t_outputBox.yview('end')

    def activeUnzip(self):
        print 'active unzip'

    def movePackages2(self):
        print 'move packages2'

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

    def load(self):
        try:
            self.ConfigFile = self.t_configFile.get('0.0', 'end-1c')
            self.getPara()
            print 'load ' + self.ConfigFile
        except:
            print 'Unable to load {}'.format(self.ConfigFile)

    def save(self):
        print 'save'

    def exit(self):
        self.parent.destroy()


def main():
    root = tk.Tk()
    root.geometry('600x600+5+5')
    root.title('Windows OTM/Patch build Control Panel II')
    app = controlPanel(root)
#     sys.stderr = StdError_redirector(app.t_outputBoxError)
#     sys.stdout = Std_redirector(app.t_outputBox)
    root.mainloop()


if __name__ == '__main__':
    main()