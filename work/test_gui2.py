import Tkinter as tk
import ConfigParser
import sys

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
        config = ConfigParser.ConfigParser()
        config.read(r'C:\Users\ChilleeChillee\git\testrepo\work\path_config.ini')
        self.daily_folder = config.get('DailyPatch', 'daily_folder')
        self.irci = config.get('DailyPatch', 'irci')
        #package_date = config.get('DailyPatch', 'package_date')
        self.package_hr = config.get('DailyPatch', 'package_hr')
        self.remote_path = config.get('DailyPatch', 'remote_path')
        self.local_path = config.get('DailyPatch', 'local_path')
        self.parent = parent
        self.constructUI()

    def main_loop(self):
        self.parent.mainloop()

    def constructUI(self):
        self.pack(fill='both', expand=1)
        #self.grid(sticky='nsew')
        self.grid_rowconfigure(18,weight=1)
        self.grid_rowconfigure(19,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(4,weight=1)
#
        self.var_2400 = tk.IntVar()
        self.var_2401c2p = tk.IntVar()
        self.var_2500 = tk.IntVar()
        self.var_2600 = tk.IntVar()

        l_dailyIntegration = tk.Label(self, text = 'Daily Integration',font=(24)).grid(row=0,column=0, columnspan=2,sticky='w')
        l_patchTesting = tk.Label(self, text = 'Patch Testing',font=(24)).grid(row=0,column=3, columnspan=2,sticky='w')
        l_columnSpacer = tk.Label(self, text = ' ').grid(row=0,column=2,rowspan=11)

        l_date = tk.Label(self, text='Date')
        l_date.grid(row=2, column=0, sticky='w')
        l_hour = tk.Label(self, text='Hour').grid(row=3, column=0, sticky='w')
        l_irci = tk.Label(self, text='Irci').grid(row=4, column=0, sticky='w')
        l_agent = tk.Label(self, text='Agent').grid(row=2, column=3, sticky='w')
        l_buildLabel = tk.Label(self, text='Build Label').grid(row=3, column=3, sticky='w')
        l_rowSpacer  = tk.Label(self, text=' ').grid(row=5,column=0, columnspan=4)
        l_OTMremotePath = tk.Label(self, text='Remote path').grid(row=6, column=0, sticky='w')
        l_OTMlocalPath = tk.Label(self, text='Local path').grid(row=7, column=0, sticky='w')
        l_PTremotePath = tk.Label(self, text='Remote path').grid(row=6, column=3, sticky='w')
        l_PTlocalPath = tk.Label(self, text='Local path').grid(row=7, column=3, sticky='w')
        l_OTMsourcePath  = tk.Label(self, text='Source path').grid(row=8, column=0, sticky='w')
        l_PTsourcePath  = tk.Label(self, text='Source path').grid(row=8, column=3, sticky='w')
        l_packages2build = tk.Label(self, text='Package(s) to be downloaded and built').grid(row=9, column=3, columnspan=2, sticky='w')
        l_rowSpacer3  = tk.Label(self, text=' ').grid(row=11, column=0, columnspan=2)
        l_rowSpacer4  = tk.Label(self, text=' ').grid(row=17, column=0, columnspan=5)

        self.t_date = tk.Text(self, width=20, height=1)
        self.t_date.grid(row=2, column=1, sticky='w')
        self.t_hour = tk.Text(self, width=20, height=1).grid(row=3, column=1, sticky='w')
        self.t_irci = tk.Text(self, width=20, height=1).grid(row=4, column=1, sticky='w')
        self.t_agent = tk.Text(self, width=20, height=1).grid(row=2, column=4, sticky='w')
        self.t_buildLabel = tk.Text(self, width=20, height=1).grid(row=3, column=4, sticky='w')
        self.t_OTMremotePath = tk.Text(self, height=1).grid(row=6, column=1, sticky='we')
        self.t_OTMlocalPath = tk.Text(self, height=1).grid(row=7, column=1, sticky='we')
        self.t_OTMsourcePath = tk.Text(self, height=1).grid(row=8, column=1, sticky='we')
        self.t_PTremotePath = tk.Text(self, height=1).grid(row=6, column=4, sticky='we')
        self.t_PTlocalPath = tk.Text(self, height=1).grid(row=7, column=4, sticky='we')
        self.t_PTsourcePath = tk.Text(self, height=1).grid(row=8, column=4, sticky='we')
        self.t_outputBox = tk.Text(self)
        self.t_outputBox.grid(row=18, column=0, columnspan=5, sticky='nsew')
        self.t_outputBoxError = tk.Text(self)
        self.t_outputBoxError.grid(row=19, column=0, columnspan=5, sticky='nsew')

        self.b_GURP = tk.Button(self, text='Get Unzip Rename Packages', command=self.GURP, width=10).grid(row=9, column=0, columnspan=2, pady=2, sticky='we')
        self.b_movePackages = tk.Button(self, text='Move CSS', command=self.movePackages).grid(row=10, column=0, columnspan=2, sticky='we')
        self.b_getPackages = tk.Button(self, text='Get Packages', command=self.getPackages).grid(row=14, column=3, columnspan=2, sticky='we')
        self.b_activeUnzip = tk.Button(self, text='Active Unzip', command=self.activeUnzip).grid(row=15, column=3, columnspan=2, sticky='we')
        self.b_movePackages2 = tk.Button(self, text='Move CSS', command=self.movePackages2).grid(row=16, column=3, columnspan=2, sticky='we')
        self.b_build4packages = tk.Button(self, text='Build 4 Packages', command=self.build4packages).grid(row=12, column=0, columnspan=2, sticky='we')
        self.b_buildBYT = tk.Button(self, text='Build BYT', command=self.buildBYT).grid(row=13, column=0, columnspan=2, sticky='we')
        self.b_buildBXT = tk.Button(self, text='Build BXT', command=self.buildBXT).grid(row=14, column=0, columnspan=2, sticky='we')
        self.b_buildCHTC2P = tk.Button(self, text='Build CHT CSI2PLUS', command=self.buildCHTC2P).grid(row=15, column=0, columnspan=2, sticky='we')
        self.b_buildSKC = tk.Button(self, text='Build SKC', command=self.buildSKC).grid(row=16, column=0, columnspan=2, sticky='we')
        self.b_exit = tk.Button(self, text='Exit', command=exit,width=10).grid(row=20, column=0, pady=4, sticky='we')

        self.c_2400 = tk.Checkbutton(self, text='2400', variable=self.var_2400)
        self.c_2400.grid(row=10, column=3, sticky='w')
        self.c_2401C2P = tk.Checkbutton(self, text='2401C2P', variable=self.var_2401c2p).grid(row=11, column=3, sticky='w')
        self.c_2500 = tk.Checkbutton(self, text='2500', variable=self.var_2500).grid(row=10, column=4, sticky='w')
        self.c_2600 = tk.Checkbutton(self, text='2600', variable=self.var_2600).grid(row=11, column=4, sticky='w')

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.config(command=self.t_outputBox.yview)
        self.scrollbar.grid(row=18, column=5, sticky='ns')
        self.scrollbarError = tk.Scrollbar(self)
        self.scrollbarError.config(command=self.t_outputBoxError.yview)
        self.scrollbarError.grid(row=19, column=5, sticky='ns')
        self.t_outputBox.config(yscrollcommand=self.scrollbar.set)
        self.t_outputBoxError.config(yscrollcommand=self.scrollbarError.set)

    def GURP(self):
        var = self.t_date.get('0.0','end-1c')
        text = self.t_date.get('0.0','end')
        print var
        self.t_outputBox.yview('end')

    def movePackages(self):
        print 'move packages'

    def getPackages(self):
        print 'insert','Selected packages to be built'
        if self.var_2400.get() == 1:
            print 2400
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

    def exit(self):
        self.parent.destroy()


def main():
    root = tk.Tk()
    root.geometry('600x700+5+5')
    root.title('Windows OTM/Patch build Control Panel II')
    app = controlPanel(root)
    sys.stderr = StdError_redirector(app.t_outputBoxError)
    sys.stdout = Std_redirector(app.t_outputBox)
    root.mainloop()


if __name__ == '__main__':
    main()