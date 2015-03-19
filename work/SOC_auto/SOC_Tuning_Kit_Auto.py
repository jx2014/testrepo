#auto video record
#author: Jeremy Xue
#email: jeremy.xzm@gmail.com
#date: Feb 17th, 2015

import win32api, win32con
import win32com.client
import win32ui
import time
import ctypes
import os
import subprocess

testVR60FPS = False
testRAW = True

recordAttempts = 1
videoDuration = 30

sensors = ['front', 'rear']
tests = ['SI','VR']
mp4FIlePath = r'C:\Users\irp\Desktop'

titleSocCaptureEngine = "SoC Camera Tuning Kit (v0.2.40108.1)"
titleSaveVideo = "Select File Name"

shell = win32com.client.Dispatch("WScript.Shell")
shell.AppActivate(titleSocCaptureEngine)
user32 = ctypes.windll.user32



#sensor window
sensorWindowXStart = 695
sensorWindowXEnd = 814
sensorWindowYStart = 153
sensorWindowYEnd = 173 # next item begins at 73 + 1(offset window border)
sensorWindowFontSize = 12

#stream window - preview pin, capture pin, etc
streamWindowXStart = 695
streamWindowXEnd = 814
streamWindowYStart = 179
streamWindowYEnd = 199 # next item begins at 73 + 1(offset window border)
streamWindowFontSize = 12

#format window - 640x480, yuy2, etc
formatWindowXStart = 695
formatWindowXEnd = 814
formatWindowYStart = 205
formatWindowYEnd = 225 # next item begins at 73 + 1(offset window border)
formatWindowFontSize = 12

#Start button
startButtonXStart = 654
startButtonXEnd = 717
startButtonYStart = 261
startButtonYEnd = 287 

#Stop button
stopButtonXStart = 720
stopButtonXEnd = 783
stopButtonYStart = 261
stopButtonYEnd = 287 

#SI, aka snapshot, take photo, dumpRaw button
siButtonXStart = 786
siButtonXEnd = 849
siButtonYStart = 261
siButtonYEnd = 287

#VR button
vrButtonXStart = 858
vrButtonXEnd = 939
vrButtonYStart = 261
vrButtonYEnd = 287


SENSOR_Window = {
				1: 'front', #UF
				2: 'rear', #WF
				}

STREAM_Window = {
				1: 'Preview Pin',
				2: 'Capture Pin',
				3: 'Image Pin',
				4: 'Raw Pin',
				}

UF_RAW = {
		1:'2688x1944, GR10',
		}

WF_RAW = {
		1:'2176x1376_GR10_60FPS',
		2:'2176x1560_GR10',
		3:'4224x3120_GR10',
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
		2:'640x360_YUY2_60fps',		
		4:'640x360_NV12_60fps',
		6:'640x480_YUY2_60fps',		
		8:'640x480_NV12_60fps',
		10:'1280x720_YUY2_60fps',
		12:'1280x720_NV12_60fps',
		14:'1280x960_YUY2_60fps',
		16:'1280x960_NV12_60fps',
		18:'1920X1080_YUY2_60fps',
		20:'1920X1080_NV12_60fps',
		}

def WindowCenter(x1, x2, y1, y2):
	xc = (x1 + x2) / 2
	yc = (y1 + y2) / 2
	return xc, yc

def GetWindowPosition(title):
	shell.AppActivate(title)
	x, y =  win32ui.FindWindow(None, title).GetWindowRect()[0:2]
	return x, y	
	
# def MoveToImageMode():
	# x, y = GetWindowPosition(titleSocCaptureEngine)	 
	# user32.SetCursorPos(x+30,y+60)

# def MoveToVideoMode():
	# x, y = GetWindowPosition(titleSocCaptureEngine)	 
	# user32.SetCursorPos(x+90,y+60)

# def MoveToShutter():
	# x, y = GetWindowPosition(titleSocCaptureEngine)	 
	# user32.SetCursorPos(x+150,y+60)

def MoveToSelectSensor():
	x, y = GetWindowPosition(titleSocCaptureEngine)	 
	xc, yc = WindowCenter(sensorWindowXStart, sensorWindowXEnd, sensorWindowYStart, sensorWindowYEnd) #move to center of the format window
	user32.SetCursorPos(x+xc,y+yc)

def MoveToSelectStream():
	x, y = GetWindowPosition(titleSocCaptureEngine)	 
	xc, yc = WindowCenter(streamWindowXStart, streamWindowXEnd, streamWindowYStart, streamWindowYEnd) #move to center of the format window
	user32.SetCursorPos(x+xc,y+yc)	

def MoveToSelectFormat():
	x, y = GetWindowPosition(titleSocCaptureEngine)	 
	xc, yc = WindowCenter(formatWindowXStart, formatWindowXEnd, formatWindowYStart, formatWindowYEnd) #move to center of the format window
	user32.SetCursorPos(x+xc,y+yc)

def MoveToSTARTbutton():
	x, y = GetWindowPosition(titleSocCaptureEngine)	 
	xc, yc = WindowCenter(startButtonXStart, startButtonXEnd, startButtonYStart, startButtonYEnd) 
	user32.SetCursorPos(x+xc,y+yc)

def MoveToSTOPbutton():
	x, y = GetWindowPosition(titleSocCaptureEngine)	 
	xc, yc = WindowCenter(stopButtonXStart, stopButtonXEnd, stopButtonYStart, stopButtonYEnd) 
	user32.SetCursorPos(x+xc,y+yc)

def MoveToSIbutton(): #aka Dump Raw, 
	x, y = GetWindowPosition(titleSocCaptureEngine)	 
	xc, yc = WindowCenter(siButtonXStart, siButtonXEnd, siButtonYStart, siButtonYEnd) 
	user32.SetCursorPos(x+xc,y+yc)	

def MoveToVRbutton():
	x, y = GetWindowPosition(titleSocCaptureEngine)	 
	xc, yc = WindowCenter(vrButtonXStart, vrButtonXEnd, vrButtonYStart, vrButtonYEnd) 
	user32.SetCursorPos(x+xc,y+yc)		

# def MoveToULLchecker():
	# x, y = GetWindowPosition(titleSocCaptureEngine)	 
	# xc, yc = WindowCenter(ullCheckerXStart, ullCheckerXEnd, ullCheckerYStart, ullCheckerYEnd) #move to center of the resolution window
	# user32.SetCursorPos(x+xc,y+yc)
	
# def MoveToSave():
	# x, y = GetWindowPosition(titleSocCaptureEngine)	 
	# user32.SetCursorPos(x+580,y+640)
	
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
	MouseClick()	# Active the drop down window of resolution
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
	'''
		1: 'front', #UF
		2: 'rear', #WF
	'''
	for index, content in SENSOR_Window.iteritems():
		if content == sensor:
			DropDownWindowSelector(index, MoveToSelectSensor(), sensorWindowXStart, sensorWindowXEnd, sensorWindowYStart, sensorWindowYEnd, sensorWindowFontSize)

def SelectStream(stream):
	'''		
		1: 'Preview Pin',
		2: 'Capture Pin',
		3: 'Image Pin',
		4: 'Raw Pin',
	'''
	for index, content in STREAM_Window.iteritems():
		if content == stream:
			DropDownWindowSelector(index, MoveToSelectStream(), streamWindowXStart, streamWindowXEnd, streamWindowYStart, streamWindowYEnd, streamWindowFontSize)

def SelectFormatByName(FormatName, FormatSettings):
	for index, content in FormatSettings.iteritems():
		if content == stream:
			DropDownWindowSelector(index, MoveToSelectFormat(), formatWindowXStart, formatWindowXEnd, formatWindowYStart, formatWindowYEnd, formatWindowFontSize)
	
def SelectFormat(index): #may not be needed, substituted by DropDownWindowSelector
	x, y = GetWindowPosition(titleSocCaptureEngine)	
	MoveToSelectFormat() # Move to center of the resolution window first
	xs, ys = win32api.GetCursorPos()
	#print xs, ys
	MouseClick() # Active the drop down window of resolution
	xc, yc = WindowCenter(formatWindowXStart, formatWindowXEnd, formatWindowYStart, formatWindowYEnd)
	yc = (formatWindowYEnd + 2) + (formatWindowFontSize / 2) # Y center of the first selection and we go from here
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

def VideoRecord(sensor, resList, shutterAttempts = 1, videoLength = 10, optionMSG=' '):
	t = len(resList.keys())
	tx = 1
	for key in resList.keys():	
		n = 1		
		while n <= shutterAttempts:
			SelectFormat(key)
			#start preview
			MoveToSTARTbutton()
			MouseClick() 
			time.sleep(1)	
			#start video recording
			MoveToVRbutton() 
			MouseClick() 
			time.sleep(videoLength)
			#stop video recording
			MoveToSTOPbutton()
			MouseClick()
			#rename saved video file
			newFileName = '_'.join([sensor,resList.get(key),str(n)])
			newFileName = '.'.join([newFileName,'mp4'])
			newFileName = '\\'.join([mp4FIlePath, newFileName]) 
			oldFileName = '\\'.join([mp4FIlePath, 'sink.mp4'])
			print " ".join(filter(None, ["VR:", optionMSG, resList.get(key),"Attempts:",str(n), "Format:", str(tx), "of", str(t)]))	
			time.sleep(2)
			if os.path.exists(newFileName):
				os.remove(newFileName)
			os.rename(oldFileName, newFileName)
			n = n + 1
		tx = tx + 1

def StillImage(sensor, resList, shutterAttempts = 1, optionMSG = ''):
	for key in resList.keys():	
		n = 1
		while n <= shutterAttempts:
			SelectStream("Image Pin")
			time.sleep(0.5)
			SelectFormat(key) #select resolution based on index
			time.sleep(0.5)
			#MoveToShutter() #This is substituted by image capture
			MouseClick() # Take image
			print " ".join(filter(None, ["SI:", optionMSG, str(key), resList.get(key),str(n)]))			
			n = n + 1

def RawImage(sensor, resList, shutterAttempts = 1, optionMSG = ''):
	t = len(resList.keys())
	tx = 1
	for key in resList.keys():	
		n = 1		
		while n <= shutterAttempts:
			SelectFormat(key)
			#start preview
			MoveToSTARTbutton()
			MouseClick() 
			time.sleep(0.5)
			#start Dump Raw
			MoveToSIbutton()
			MouseClick()
			time.sleep(0.5)
			#stop preview
			MoveToSTOPbutton()
			MouseClick()
			#rename saved video file
			print " ".join(filter(None, ["SI:", optionMSG, resList.get(key),"Attempts:",str(n), "Format:", str(tx), "of", str(t)]))	
			time.sleep(0.5)
			n = n + 1
		tx = tx + 1


#test VR with 60FPS
if testVR60FPS == True:			
	sensor = 'rear'
	SelectSensor(sensor)
	SelectStream('Capture Pin')
	time.sleep(2)
	VideoRecord(sensor, WF_VR)

#test raw capture			
if testRAW == True:			
	for sensor in sensors:
		SelectSensor(sensor)
		SelectStream('Raw Pin')
		time.sleep(2)
		if sensor == 'front':
			RawImage(sensor, UF_RAW)
		elif sensor == 'rear':
			RawImage(sensor, WF_RAW)
				
subprocess.call('pause', shell=True)

# def StillImageHDR(sensor, resList, shutterAttempts = 1, optionMSG = ''):
	# for key in resList.keys():	
		# n = 1
		# while n <= shutterAttempts:
			# MoveToImageMode()
			# MouseClick() 
			# time.sleep(0.1)
			# SelectFormat(key) #select resolution based on index
			# time.sleep(1)
			
			# MoveToHDRbutton() # Enable HDR	
			# MouseClick()
			# time.sleep(1)
			
			# MoveToShutter()
			# MouseClick() # Take image
			# print " ".join(filter(None, ["SI:", optionMSG, str(key), resList.get(key),str(n)]))			
			# n = n + 1
			# time.sleep(1)
			


				
# #Take HDR image
# if testSIwithHDR == True:
	# for index, sensor in SENSOR_Window.iteritems():
		# SelectSensor(sensor)
		# time.sleep(2)
		# for testMode in tests:									
			# if testMode == 'SI' and sensor == 'front':
				# StillImageHDR(sensor, UF_SI, optionMSG='front HDR')
			# elif testMode == 'SI' and sensor == 'rear':	
				# StillImageHDR(sensor, WF_SI, optionMSG='rear HDR')
			# elif testMode == 'VR':
				# print "HDR Not supported in VR"
				# continue

				
# #Take ULL image
# if testSIwithULL == True:
	# for index, sensor in SENSOR_Window.iteritems():
		# SelectSensor(sensor)
		# time.sleep(2)
		# #Enable ULL
		# for index, content in ULL_Checker.iteritems():
			# if content == 'On':
				# DropDownWindowSelector(index, MoveToULLchecker(), ullCheckerXStart, ullCheckerXEnd, ullCheckerYStart, ullCheckerYEnd, ullCheckerFontSize)
				# for testMode in tests:							
					# if testMode == 'SI' and sensor == 'front':						
						# StillImage(sensor, UF_SI, optionMSG='front ULL')
					# elif testMode == 'SI' and sensor == 'rear':
						# StillImage(sensor, WF_SI, optionMSG='rear ULL')
					# elif testMode == 'VR':
						# print "ULL Not supported in VR"
						# continue							
	# #Disable ULL
	# for index, content in ULL_Checker.iteritems():
		# if content == 'Off':
			# DropDownWindowSelector(index, MoveToULLchecker(), ullCheckerXStart, ullCheckerXEnd, ullCheckerYStart, ullCheckerYEnd, ullCheckerFontSize)	
