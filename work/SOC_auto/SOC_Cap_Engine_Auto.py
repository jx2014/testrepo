#auto video record
#author: Jeremy Xue
#email: jeremy.xzm@gmail.com
#date: March 30th, 2015
#comment: add Flash photography

import os
import logging
import win32api, win32con
import win32com.client
import win32ui
import time
import ctypes
import subprocess

logging.basicConfig(format='%(asctime)s %(levelname)s::: %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p', 
                    filename='Output.log',
                    filemode='w',
                    level=logging.INFO,)

testSIandVR = 0
testSIwithFlash = 1
testSIwithHDR = 0
testSIwithULL = 0


recordAttempts = 1

videoDuration = 30
tests = ['SI', 'VR']

titleSocCaptureEngine = "Intel SoC Capture Engine (v0.1.40112.1)"
titleSaveVideo = "Select File Name"

shell = win32com.client.Dispatch("WScript.Shell")
shell.AppActivate(titleSocCaptureEngine)
user32 = ctypes.windll.user32

#resolution window
resWindowXStart = 716
resWindowXEnd = 835
resWindowYStart = 53
resWindowYEnd = 73 # next item begins at 73 + 1(offset window border)
resWindowFontSize = 12

#sensor window
senWindowXStart = 580
senWindowXEnd = 700
senWindowYStart = 53
senWindowYEnd = 73 # next item begins at 73 + 1(offset window border)
senWindowFontSize = 12

#HDR button
hdrButtonXStart = 462
hdrButtonXEnd = 503
hdrButtonYStart = 43
hdrButtonYEnd = 76

#Flash button
flashButtonXStart = 248
flashButtonXEnd = 277
flashButtonYStart = 43
flashButtonYEnd = 76


#ULL checker
ullCheckerXStart = 701
ullCheckerXEnd = 747
ullCheckerYStart = 377
ullCheckerYEnd = 397
ullCheckerFontSize = 12

#standard tab"
stdTabXStart = 646
stdTabXEnd = 705
stdTabYStart = 677
stdTabYEnd = 678




SENSOR_Window = {
                1: 'front',
                2: 'rear',
                }

ULL_Checker = {
        1:'Off',
        2:'On',
        }

UF_SI = {
        1:'2560x1440_YUY2',
        2:'2560x1440_NV12',
        3:'2560x1440_JPEG',
        4:'2560x1920_YUY2',
        5:'2560x1920_NV12',
        6:'2560x1920_JPEG',
         }

UF_VR = {
        1:'640x360_YUY2',       
        2:'640x360_NV12',       
        5:'1280x720_YUY2',      
        6:'1280x720_NV12',      
        9:'1920X1080_YUY2',     
        10:'1920X1080_NV12',        
        }

WF_SI = {
        1:'4096x2304_YUY2',
        2:'4096x2304_NV12',
        3:'4096x2304_JPEG',
        4:'4096x3072_YUY2',
        5:'4096x3072_NV12',
        6:'4096x3072_JPEG',
         }

WF_VR = {
        1:'640x360_YUY2',       
        #2:'640x360_YUY2_60fps',
        3:'640x360_NV12',
        #4:'640x360_NV12_60fps',
        9:'1280x720_YUY2',
        #10:'1280x720_YUY2_60fps',
        11:'1280x720_NV12',
        #12:'1280x720_NV12_60fps',
        17:'1920X1080_YUY2',
        #18:'1920X1080_YUY2_60fps',
        19:'1920X1080_NV12',
        #20:'1920X1080_NV12_60fps',
        }

def WindowCenter(x1, x2, y1, y2):
    xc = (x1 + x2) / 2
    yc = (y1 + y2) / 2
    return xc, yc

def GetWindowPosition(title):
    shell.AppActivate(title)
    x, y =  win32ui.FindWindow(None, title).GetWindowRect()[0:2]
    return x, y 
    
def MoveToImageMode():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    user32.SetCursorPos(x+30,y+60)

def MoveToVideoMode():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    user32.SetCursorPos(x+90,y+60)

def MoveToShutter():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    user32.SetCursorPos(x+150,y+60)

def MoveToSelectSensor():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    user32.SetCursorPos(x+650,y+60)

def MoveToSelectStandardTab():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    xc, yc = WindowCenter(stdTabXStart, stdTabXEnd, stdTabYStart, stdTabYEnd) #move to center of the resolution window
    user32.SetCursorPos(x+xc,y+yc)  
    
def MoveToSelectResolution():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    xc, yc = WindowCenter(resWindowXStart, resWindowXEnd, resWindowYStart, resWindowYEnd) #move to center of the resolution window
    user32.SetCursorPos(x+xc,y+yc)

def MoveToHDRbutton():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    xc, yc = WindowCenter(hdrButtonXStart, hdrButtonXEnd, hdrButtonYStart, hdrButtonYEnd) #move to center of the resolution window
    user32.SetCursorPos(x+xc,y+yc)

def MoveToFlashbutton():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    xc, yc = WindowCenter(flashButtonXStart, flashButtonXEnd, flashButtonYStart, flashButtonYEnd) #move to center of the resolution window
    user32.SetCursorPos(x+xc,y+yc)

def MoveToULLchecker():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    xc, yc = WindowCenter(ullCheckerXStart, ullCheckerXEnd, ullCheckerYStart, ullCheckerYEnd) #move to center of the resolution window
    user32.SetCursorPos(x+xc,y+yc)
    
def MoveToSave():
    x, y = GetWindowPosition(titleSocCaptureEngine)  
    user32.SetCursorPos(x+580,y+640)
    
def SendKeys(key):
    shell.SendKeys(key, 0)
    time.sleep(0.5)

def MouseClick():
    x, y = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    time.sleep(0.5)

def DropDownWindowSelector(index, FuncMoveCursor, windowXstart, windowXend, windowYstart, windowYend, windowFontSize):
    x, y = GetWindowPosition(titleSocCaptureEngine)
    FuncMoveCursor
    xs, ys = win32api.GetCursorPos()
    MouseClick()    # Active the drop down window of resolution
    xc, yc = WindowCenter(windowXstart, windowXend, windowYstart, windowYend)
    yc = (windowYend + 2) + (windowFontSize / 2) # Y center of the first selection and we go from here
    yc = yc + (index - 1) * (12 + 1)    
    xn, yn = 0, 0   
    while ((ys + yn) <= (y + yc)):
        yn += 1
        user32.SetCursorPos(xs + xn, ys + yn)
        time.sleep(0.01)    
    while ((xs + xn) <= (x + xc)):                      
        xn += 1         
        user32.SetCursorPos(xs + xn, ys + yn)
        time.sleep(0.01)    
    #user32.SetCursorPos(x + xc, y + yc) #Set cursor to the resolution according to the Cursor Pos.
    MouseClick()

def SelectSensor(sensor):
    for index, content in SENSOR_Window.iteritems():
        if content == sensor:
            DropDownWindowSelector(index, MoveToSelectSensor(), senWindowXStart, senWindowXEnd, senWindowYStart, senWindowYEnd, senWindowFontSize)
#   MoveToSelectSensor()
#   MouseClick()
#   x, y = win32api.GetCursorPos()
#   user32.SetCursorPos(x, y+17)
#   MouseClick()

#def SelectSecondSensor():
#   MoveToSelectSensor()
#   MouseClick()
#   x, y = win32api.GetCursorPos()
#   user32.SetCursorPos(x, y+35)
#   MouseClick()    
    
def SelectResolution(index):
    x, y = GetWindowPosition(titleSocCaptureEngine) 
    MoveToSelectResolution() # Move to center of the resolution window first
    xs, ys = win32api.GetCursorPos()
    #print xs, ys
    MouseClick() # Active the drop down window of resolution
    xc, yc = WindowCenter(resWindowXStart, resWindowXEnd, resWindowYStart, resWindowYEnd)
    yc = (resWindowYEnd + 2) + (resWindowFontSize / 2) # Y center of the first selection and we go from here
    yc = yc + (index - 1) * (12 + 1)    
    xn, yn = 0, 0   
    while ((ys + yn) <= (y + yc)):
        yn += 1
        user32.SetCursorPos(xs + xn, ys + yn)
        time.sleep(0.01)    
    while ((xs + xn) <= (x + xc)):                      
        xn += 1         
        user32.SetCursorPos(xs + xn, ys + yn)
        time.sleep(0.01)    
    #user32.SetCursorPos(x + xc, y + yc) #Set cursor to the resolution according to the Cursor Pos.
    MouseClick()

def VideoRecord(sensor, resList, shutterAttempts = 1, videoLength = 10):
    for key in resList.keys():  
        n = 1        
        MoveToVideoMode()
        MouseClick() #Select video mode
        SelectResolution(key) #select video resolution based on index
        time.sleep(1)        
        while n <= shutterAttempts:
            MoveToShutter()
            time.sleep(0.5)
            MouseClick() # record video
            time.sleep(2) #wait 2 seconds before entering title, sometimes it requires it.
            SendKeys('_'.join([sensor,resList.get(key),str(n)])) # enter video title 
            time.sleep(1)
            SendKeys("{ENTER}")
            #time.sleep(0.5)
            #SendKeys("{ENTER}") #In case to overwrite 
            outputLine =  " ".join(["VR:", sensor, resList.get(key), str(n), 'of', str(shutterAttempts)])
            print outputLine
            logging.info(outputLine)
            time.sleep(videoLength)
            MoveToShutter() #stop recording
            MouseClick()
            time.sleep(2) #wait for it to save
            n = n + 1

def StillImage(sensor, resList, shutterAttempts = 1, optionMSG = ''):
    for key in resList.keys():  
        n = 1        
        MoveToImageMode()
        MouseClick() 
        SelectResolution(key) #select resolution based on index
        time.sleep(1)        
        while n <= shutterAttempts:
            MoveToShutter()
            MouseClick() # Take image       
            outputLine = " ".join(filter(None, ["SI:", optionMSG, 'Key:', str(key), resList.get(key), str(n), 'of', str(shutterAttempts)]))         
            print outputLine
            logging.info(outputLine)
            n = n + 1
            time.sleep(1.5)

def StillImageHDR(sensor, resList, shutterAttempts = 1, optionMSG = ''):
    for key in resList.keys():  
        n = 1        
        #print '\n'
        #print resList.keys()
        #print 'current key is', key     
        MoveToImageMode()
        MouseClick() 
        time.sleep(0.1)
        SelectResolution(key) #select resolution based on index
        time.sleep(1)        
        MoveToHDRbutton() # Enable HDR  
        MouseClick()
        time.sleep(1)       
        while n <= shutterAttempts:
            MoveToShutter()
            MouseClick() # Take image
            outputLine = " ".join(filter(None, ["SI:", optionMSG, 'Key:', str(key), resList.get(key), str(n), 'of', str(shutterAttempts)]))          
            print outputLine
            logging.info(outputLine)
            n = n + 1
            time.sleep(1)
        #print "end of shutter attempts"
 

#Normal test of SI and VR
if testSIandVR == True:         
    for index, sensor in SENSOR_Window.iteritems():
        SelectSensor(sensor)
        time.sleep(2)       
        for testMode in tests:
            time.sleep(2)
            if testMode == 'SI' and sensor == 'front':
                StillImage(sensor, UF_SI, shutterAttempts = recordAttempts)
            elif testMode == 'VR' and sensor == 'front':
                VideoRecord(sensor, UF_VR, shutterAttempts = recordAttempts)
            elif testMode == 'SI' and sensor == 'rear':
                StillImage(sensor, WF_SI, shutterAttempts = recordAttempts)             
            elif testMode == 'VR' and sensor == 'rear':
                VideoRecord(sensor, WF_VR, shutterAttempts = recordAttempts)

                
#Take image with Flash on                
if testSIwithFlash == True:
    for index, sensor in SENSOR_Window.iteritems():
        SelectSensor(sensor)
        time.sleep(2)
        MoveToFlashbutton() # Enable Flash
        MouseClick()
        for testMode in tests:
            time.sleep(2)
            if testMode == 'SI' and sensor == 'front':                      
                StillImage(sensor, UF_SI, optionMSG='front Flash', shutterAttempts = recordAttempts)
            elif testMode == 'SI' and sensor == 'rear':
                StillImage(sensor, WF_SI, optionMSG='rear Flash', shutterAttempts = recordAttempts)
            elif testMode == 'VR':
                print "Flash Not supported in VR"
                continue
                
#Take HDR image
if testSIwithHDR == True:
    for index, sensor in SENSOR_Window.iteritems():
        SelectSensor(sensor)
        time.sleep(2)
        MoveToSelectStandardTab()
        MouseClick()
        for testMode in tests:
            time.sleep(2)
            if testMode == 'SI' and sensor == 'front':
                StillImageHDR(sensor, UF_SI, optionMSG='front HDR', shutterAttempts = recordAttempts)
            elif testMode == 'SI' and sensor == 'rear': 
                StillImageHDR(sensor, WF_SI, optionMSG='rear HDR', shutterAttempts = recordAttempts)
            elif testMode == 'VR':
                print "HDR Not supported in VR"
                continue

                
#Take ULL image
if testSIwithULL == True:
    for index, sensor in SENSOR_Window.iteritems():
        SelectSensor(sensor)
        time.sleep(2)
        MoveToSelectStandardTab()
        MouseClick()
        #Enable ULL
        for index, content in ULL_Checker.iteritems():      
            if content == 'On':
                DropDownWindowSelector(index, MoveToULLchecker(), ullCheckerXStart, ullCheckerXEnd, ullCheckerYStart, ullCheckerYEnd, ullCheckerFontSize)
                for testMode in tests:
                    time.sleep(2)
                    if testMode == 'SI' and sensor == 'front':                      
                        StillImage(sensor, UF_SI, optionMSG='front ULL', shutterAttempts = recordAttempts)
                    elif testMode == 'SI' and sensor == 'rear':
                        StillImage(sensor, WF_SI, optionMSG='rear ULL', shutterAttempts = recordAttempts)
                    elif testMode == 'VR':
                        print "ULL Not supported in VR"
                        continue                            
    #Disable ULL
    for index, content in ULL_Checker.iteritems():
        if content == 'Off':
            DropDownWindowSelector(index, MoveToULLchecker(), ullCheckerXStart, ullCheckerXEnd, ullCheckerYStart, ullCheckerYEnd, ullCheckerFontSize)   

subprocess.call('pause', shell=True)