import tarfile
import os
import re
import shutil

#add by chilleetablet
# css_2400 and css_2401 will be sub'd by css{}
css_number = ['2400','2401','2401_csi2plus']
css_number2 = list(css_number)

#the compile pattern will be constructed dynamically.
# for css_num in css_number:
#     compile_pattern = r'^(?=.*' + css_num + r')(?=.*windows)[\w\\.-:]*$'
#     pattern = re.compile(compile_pattern)

real_file = []
f_path = r'E:\Temp\tartest'

#extract all tar
for ph,b,fn in os.walk(f_path):
    for f in fn:
        file_path = ph + '\\' + f
        #print file_path
        for css_num in css_number:
            compile_pattern = r'^(?=.*' + css_num + r')(?=.*windows)[\w\\.-:]*$'
            pattern = re.compile(compile_pattern)
            if pattern.match(file_path) is not None:
                #print file_path
                with tarfile.open(file_path) as tf:
                    tf.extractall(f_path)
                css_number.remove(css_num)

#rename and move css
for ph,b,fn in os.walk(f_path):
    for f in fn:
        file_path = ph + '\\' + f
        #print file_path
        for css_num in css_number2:
            compile_pattern_css_f = r'^(?=.*' + css_num + r')(?=.*windows)[\w\\.-:]*\\css$'
            pattern_css_f = re.compile(compile_pattern_css_f)
            if pattern_css_f.match(ph) is not None:
                #print 'ph is', ph
                try:
                    os.rename(ph,ph.replace(r'\css','\\'+ css_num))
                    shutil.copytree(ph.replace(r'\css','\\'+ css_num),f_path+'\\'+css_num)
                except:
                    pass
            compile_pattern = r'^(?=.*' + css_num + r')(?=.*windows)[\w\\.-:]*css_fw\.bin$'
            pattern = re.compile(compile_pattern)
            if pattern.match(file_path) is not None:
                #print file_path
                try:
                    os.rename(file_path,file_path.replace('css_fw.bin', 'css_fw_'+ css_num +'.bin'))
                    shutil.copy2(file_path.replace('css_fw.bin', 'css_fw_'+ css_num +'.bin'),f_path)
                except:
                    pass



css = {
       '2400':'sh_css_2400_abc.windows.tar.gz',
       '2401':'sh_css_2401_abc.windows.tar.gz'
       }

all_files = [
             'E:\\sh_css_2400_abc.linux.tar.gz',
             'sh_css_2400_abc.windows.tar.gz',
             'sh_css_2401_abc.windows.tar.gz',
             'sh_css_2401_abc.linuxs.tar.gz'
             ]


