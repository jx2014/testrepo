import Tkinter as tk
import sys
import stdout_test

class Std_redirector(object):
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        if not exit_thread:
            self.widget.insert(Tk.END,string)
            self.widget.see(Tk.END)

main_window = tk.Tk()
main_window.title('Windows OTM/Patch build Control Panel')
main_window.geometry('455x540+5+53',)

var_2400 = tk.IntVar()
var_2401c2p = tk.IntVar()
var_2500 = tk.IntVar()
var_2600 = tk.IntVar()

def GURP():
    var = t_date.get('0.0','end-1c')
    text = t_date.get('0.0','end')
    print 'shit'
    t_outputBox.insert('insert',text)
    t_outputBox.insert('insert')
    t_outputBox.yview('end')

def movePackages():
    pass

def getPackages():
    t_outputBox.insert('insert','Selected packages to be built\n')
    if var_2400.get() == 1:
        t_outputBox.insert('insert','2400\n')
    if var_2401c2p.get() == 1:
        t_outputBox.insert('insert','2401_csi2plus\n')
    if var_2500.get() == 1:
        t_outputBox.insert('insert','2500\n')
    if var_2600.get() == 1:
        t_outputBox.insert('insert','2600\n')
    t_outputBox.yview('end')

def activeUnzip():
    pass

def movePackages2():
    pass

def build4packages():
    pass

def buildBYT():
    pass

def buildBXT():
    pass

def buildCHTC2P():
    pass

def buildSKC():
    pass

def exit():
    main_window.destroy()


l_dailyIntegration = tk.Label(main_window, text = 'Daily Integration',font=(24)).grid(row=0,column=0, columnspan=2,sticky='w')
l_columnSpacer = tk.Label(main_window, text = ' ').grid(row=0,column=2,rowspan=11)
l_patchTesting = tk.Label(main_window, text = 'Patch Testing',font=(24)).grid(row=0,column=3, columnspan=2,sticky='w')
l_date = tk.Label(main_window, text = 'Date').grid(row=2,column = 0,sticky='w')
l_hour = tk.Label(main_window, text = 'Hour').grid(row=3,column = 0,sticky='w')
l_irci = tk.Label(main_window, text = 'Irci').grid(row=4,column = 0,sticky='w')
l_agent = tk.Label(main_window, text = 'Agent').grid(row=2,column = 3,sticky='w')
l_buildLabel = tk.Label(main_window, text = 'Build Label').grid(row=3,column=3,sticky='w')
l_rowSpacer  = tk.Label(main_window, text = ' ').grid(row=5,column=0,columnspan=4)
l_OTMremotePath = tk.Label(main_window, text = 'Remote path').grid(row=6,column=0,sticky='w')
l_OTMlocalPath = tk.Label(main_window, text = 'Local path').grid(row=7,column=0,sticky='w')
l_PTremotePath = tk.Label(main_window, text = 'Remote path').grid(row=6,column=3,sticky='w')
l_PTlocalPath = tk.Label(main_window, text = 'Local path').grid(row=7,column=3,sticky='w')
l_rowSpacer2  = tk.Label(main_window, text = ' ').grid(row=8,column=0,columnspan=4)
l_packages2build = tk.Label(main_window, text = 'Package(s) to be downloaded and built').grid(row=9,column=3,columnspan=2,sticky='w')
l_rowSpacer3  = tk.Label(main_window, text = ' ').grid(row=11,column=0,columnspan=2)
l_rowSpacer4  = tk.Label(main_window, text = ' ').grid(row=17,column=0,columnspan=5)

t_date = tk.Text(width=20,height=1)
t_date.grid(row=2,column=1)
t_hour = tk.Text(width=20,height=1).grid(row=3,column=1)
t_irci = tk.Text(width=20,height=1).grid(row=4,column=1)
t_agent = tk.Text(width=20,height=1).grid(row=2,column=4,columnspan=2,sticky='w')
t_buildLabel = tk.Text(width=20,height=1).grid(row=3,column=4,columnspan=2,sticky='w')
t_OTMremotePath = tk.Text(width=20,height=1).grid(row=6,column=1)
t_OTMlocalPath = tk.Text(width=20,height=1).grid(row=7,column=1)
t_PTremotePath = tk.Text(width=20,height=1).grid(row=6,column=4,)
t_PTlocalPath = tk.Text(width=20,height=1).grid(row=7,column=4)
t_outputBox = tk.Text(width=10,height=10)
t_outputBox.grid(row=18,column=0,columnspan=5,sticky='ew')

b_GURP = tk.Button(main_window,text='Get Unzip Rename Packages', command=GURP).grid(row=9,column=0,columnspan=2,sticky='we')
b_movePackages = tk.Button(main_window,text='Move CSS', command=movePackages).grid(row=10,column=0,columnspan=2,sticky='we')
b_getPackages = tk.Button(main_window,text='Get Packages', command=getPackages).grid(row=14,column=3,columnspan=2,sticky='we')
b_activeUnzip = tk.Button(main_window,text='Active Unzip', command=activeUnzip).grid(row=15,column=3,columnspan=2,sticky='we')
b_movePackages2 = tk.Button(main_window,text='Move CSS', command=movePackages2).grid(row=16,column=3,columnspan=2,sticky='we')
b_build4packages = tk.Button(main_window,text='Build 4 Packages', command=build4packages).grid(row=12,column=0,columnspan=2,sticky='we')
b_buildBYT = tk.Button(main_window,text='Build BYT', command=buildBYT).grid(row=13,column=0,columnspan=2,sticky='we')
b_buildBXT = tk.Button(main_window,text='Build BXT', command=buildBXT).grid(row=14,column=0,columnspan=2,sticky='we')
b_buildCHTC2P = tk.Button(main_window,text='Build CHT CSI2PLUS', command=buildCHTC2P).grid(row=15,column=0,columnspan=2,sticky='we')
b_buildSKC = tk.Button(main_window,text='Build SKC', command=buildSKC).grid(row=16,column=0,columnspan=2,sticky='we')
b_exit = tk.Button(main_window,text='Exit', command=exit).grid(row=19,column=4,pady=4,sticky='we')

c_2400 = tk.Checkbutton(main_window,text = '2400',variable=var_2400)
c_2400.grid(row=10,column=3,sticky='w')
c_2401C2P = tk.Checkbutton(main_window,text = '2401C2P',variable=var_2401c2p).grid(row=11,column=3,sticky='w')
c_2500 = tk.Checkbutton(main_window,text = '2500',variable=var_2500).grid(row=10,column=4,sticky='w')
c_2600 = tk.Checkbutton(main_window,text = '2600',variable=var_2600).grid(row=11,column=4,sticky='w')

scrollbar = tk.Scrollbar(main_window)
scrollbar.config(command=t_outputBox.yview)
scrollbar.grid(row=18,column=5,sticky='ns')
t_outputBox.config(yscrollcommand=scrollbar.set)


main_window.mainloop()

##test
# root = tk.Tk()
# root.title("Whois Tool")
#
# text = tk.Text()
# text1 = tk.Text()
#
# text1.config(width=15, height=2)
# text1.grid(row=0)
#
# n = 0
#
# def button1():
#     global n
#     n += 1
#     text.insert('insert', 'homo {}\n'.format(n))
#     text.yview('end')
# #    text.insert('insert', text1.get("1.0", 'end'))
# #     text.insert(END, text1)
#
# b = tk.Button(root, text="Enter", width=10, height=2, command=button1)
# b.grid(row = 1)
# #
# scrollbar = tk.Scrollbar(root)
# scrollbar.grid(row=2,column=1,sticky='NS')
# text.config(width=60, height=15)
# text.grid(row=2,column=0)
# scrollbar.config(command=text.yview)
# text.config(yscrollcommand=scrollbar.set)
#
# root.mainloop()