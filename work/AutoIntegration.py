import os
import subprocess
import string
import filecmp
import difflib
import re
import string

#folder_otm = r"C:\Users\zjxuex\My Documents\LiClipse Workspace\GeneralPurpose\FolderA"
#folder_fw = r"C:\Users\zjxuex\My Documents\LiClipse Workspace\GeneralPurpose\FolderB"
folder_otm = r"C:\JX_Projects\vieddrv-trunk\camerasw\Source\Camera\ISP\css\2401_csi2plus"
folder_fw = r"F:\Incoming_packages\2401_csi2plus"



dcmp = filecmp.dircmp(folder_otm, folder_fw)

def unique_files(a,b): #verified  with beyond compare
    for rs, ds, fs in os.walk(a):
        for f in fs:
            a_path = string.join([rs,f],'\\')
            b_path = a_path.replace(a, b)
            if os.path.exists(b_path) == False:
                yield a_path

def common_files(a,b): #verified  with beyond compare
    for rs, ds, fs in os.walk(a):
        for f in fs:
            a_path = string.join([rs,f],'\\')
            b_path = a_path.replace(a, b)
            if os.path.exists(b_path) == True:
                yield a_path

def same_files(a, b): #return same files from a directory and its sub-directories
    for rs, ds, fs in os.walk(a):
        for f in fs:
            a_path = string.join([rs,f],'\\')
            b_path = a_path.replace(a, b)
            if os.path.exists(b_path) == True:
                if compare_a_b(a_path,b_path) == True:
                    yield f

def diff_files(a, b):
    for rs, ds, fs in os.walk(a):
        for f in fs:
            a_path = string.join([rs,f],'\\')
            b_path = a_path.replace(a, b)
            if os.path.exists(b_path) == True:
                #print a_path, b_path
                if compare_a_b(a_path,b_path) == False:
                    yield f

def empty_folders(a):
    for rs,ds,fs in os.walk(a):
        if len(os.listdir(rs)) < 1:
            yield rs

# def identical_file(a, b): #for single file
#     with open(a, 'U') as file1:
#         with open(b, 'U') as file2:
#             if set(file1) == set(file2):
#                 return True
#             else:
#                 return False

n = 1
for i in same_files(folder_otm, folder_fw):
    print n
    print i
    n = n + 1


n = 1
for i in diff_files(folder_otm, folder_fw):
    print n
    print i
    n = n + 1

# def compare(a, b):
#     """Compare two basestrings, normalizing whitespace -&gt; bool"""
#     return re.sub("\s{2,}", " ", a) == re.sub("\s{2,}", " ", b)
#
# def compare2(a,b):
#     return a.translate(None,string.whitespace) == b.translate(None,string.whitespace)

# def compare_a_b():
#     a = r"E:\FamilyProject\TestProject\testrepo\a.txt"
#     b = r"E:\FamilyProject\TestProject\testrepo\b.txt"
#     with open(a,'rU') as A:
#         with open(b,'rU') as B:
#             return A.read().replace('\r\n', "").replace('\n', "") == B.read().replace('\r\n', "").replace('\n', "")

a = r"E:\FamilyProject\TestProject\testrepo\a.txt"
b = r"E:\FamilyProject\TestProject\testrepo\b.txt"

def compare_a_b(a, b):
    with open(a,'rU') as A:
        with open(b,'rU') as B:
            return [line for line in A.read().split('\n') if line.strip()] == [line for line in B.read().split('\n') if line.strip()]



