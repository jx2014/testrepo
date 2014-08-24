import os

dir = r'C:\JX_Projects\vieddrv-trunk\camerasw\Source\Camera\ISP\css\2500'

for r,d,f in os.walk(dir):
    if len(d) == 0:
        if len(f) == 0:
            print r
            os.rmdir(r)
