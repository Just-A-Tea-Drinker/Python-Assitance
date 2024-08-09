import platform
import os
import win32com.client
import webbrowser
import psutil
import time
from pywinauto import application
import pygetwindow as gw
import win32gui
import win32con
import re
from screeninfo import get_monitors
import auto_yt as yt
import common_funcs as cf
import threading as th

class Windows:
    num_monitors =1
    short_cuts = []
    url_apps = []
    exe_apps = []

    app_link =None
    app_type = False

    youtube =None
    yt_thread=None
    
    def __init__(self):
        
        #getting the number of monitors
        monitors = get_monitors()
        self.num_monitors = len(monitors)
        ##this will find all the applications and store them ready for use
        self.GetDeskApps()

    #basic app managment
    def ResShort(self,path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(path)
        return shortcut.TargetPath

    def ResIntshort(self,url):
        with open(url, 'r') as file:
            for line in file:
                if line.startswith("URL="):
                    return line.split("URL=")[-1].strip()
        return None

    def GetDeskShorts(self,desk):
        shortcuts = {'exe': [], 'url': []}
        for item in os.listdir(desk):
            full_path = os.path.join(desk, item)
            if item.endswith('.lnk'):
                shortcuts['exe'].append(full_path)
            elif item.endswith('.url'):
                shortcuts['url'].append(full_path)
        return shortcuts

    def GetDeskApps(self):
        desk = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.short_cuts = self.GetDeskShorts(desk)
        self.AppExtract()
        
    def AppExtract(self):
        #getting all the apps on desktop
        for short in self.short_cuts['url']:
            temp = short.split("\\")
            self.url_apps.append(temp[-1][0:-4])

        for short in self.short_cuts['exe']:
            temp = short.split("\\")
            self.exe_apps.append(temp[-1][0:-4])
    def OpenApp(self,apps2open):
        #finding and opening the apps specified
        for app in apps2open:
            if app =="YOUTUBE":
                #starting the youtube class main option as a thread
                self.youtube = yt.Youtube()
                if self.youtube.failed !=True:
                    self.yt_thread = th.Thread(target=self.youtube.main_feature(),)
                    self.yt_thread.start()
                
                
            else:

                to_search = self.url_apps+self.exe_apps
                best_ind = to_search.index(app)
                best = to_search[best_ind]
                if best_ind<len(self.url_apps)-1:
                    #getting the index, to get the link
                    self.app_link = self.short_cuts['url'][best_ind]
                    self.app_type = True
                else:
                    self.app_link = self.short_cuts['exe'][best_ind-len(self.url_apps)]
                    self.app_type = False

                if self.app_type:
                    url = self.ResIntshort(self.app_link)
                    if url:
                        webbrowser.open(url)
                else:
                    os.startfile(self.app_link)
    def CloseApp(self,apps):
        #closing all requested apps by finding the pid by name
        for app in apps:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and app.lower() in proc.info['name'].lower():
                    proc.terminate()
                    proc.wait()

    #app managment features such as selecting, mini/maxi/mising tabs and swapping monitors
    def GetCurrentTabs(self):
        windows = gw.getAllTitles()
        final = []
        for win in windows:
            temp =win.split('-')
            temp2 = []
            for t in temp:
                if len(t) > 0 and t !=None:
                    temp2.append(t.replace(" ", ""))
            if len(temp2)>0:       
                final.append(temp2)
                temp2=[]
        return final    
        
class Linux:
    pass
class macOS:
    pass


class AppManager:
    """"
    This is a class dedicated to finding the applications on the computer and managin system operations
    like minimised switching monitors, that kind of thing
    also this is built for all three of the major types of OS, macos, linux and windows
    Note: macOs has not been tested as i simply dont own a macOS device :3
    """
    apps =[]
    OS = None
    block =False

    OS_Obj = None
    def __init__(self):
        #startng the app opener by detecting the os
        self.detect_os()
        match self.OS:
            case "Windows":
                self.block =False
                #making a windows object that will automatically find all the applications located on the desktop
                self.OS_Obj = Windows()
                self.apps = self.OS_Obj.url_apps+self.OS_Obj.exe_apps
            case "Linux":
                self.block =False
            case "macOS":
                self.block =False
            case "Unknown":
                self.block = True

    def detect_os(self):
        os_name = platform.system()
        if os_name == "Windows":
            self.OS="Windows"
        elif os_name == "Darwin":
            self.OS="macOS"
        elif os_name == "Linux":
            self.OS="Linux"
        else:
           self.OS="Unknown"
    def OpenRequest(self,app):
        #sending a request to the os obj
        self.OS_Obj.OpenApp(app)

    def CloseRequest(self,app):
        #sending a request to the os obj
        self.OS_Obj.CloseApp(app)


    def MoveRequest(self,apps):
        for app in apps:
            window = gw.getWindowsWithTitle(app)[0]
            monitorInd = None
            wasMini = False
            if window.isMinimized:
                window.restore()
                wasMini = True
            monitors = get_monitors()
            win_rect = window._rect  # Access the window's rectangle
            win_center_x = win_rect.left + win_rect.width // 2
            win_center_y = win_rect.top + win_rect.height // 2
        
            for i, monitor in enumerate(monitors):
                if (monitor.x <= win_center_x <= monitor.x + monitor.width and monitor.y <= win_center_y <= monitor.y + monitor.height):
                    monitorInd = i

            if monitorInd is None:
                return 
            # Determine the next monitor index
            next_index = (monitorInd + 1) % len(monitors)
            monitor = monitors[next_index]
            
            # Restore the window if it's maximized or minimized
            if window.isMaximized or window.isMinimized:
                window.restore()
            
            # Move the window to the top-left corner of the next monitor
            window.moveTo(monitor.x, monitor.y)
            
            # Optionally maximize the window after moving
            if wasMini:
                window.minimize()
            else:
                window.maximize()

    def MaxiRequest(self,apps):
        for app in apps:
            window = gw.getWindowsWithTitle(app)[0]
            if window.isMaximized or window.isMinimized:
                window.restore()

            window.maximize()

    def MiniRequest(self,apps):
        for app in apps:
            window = gw.getWindowsWithTitle(app)[0]
            if window.isMaximized or window.isMinimized:
                window.restore()
            
            window.minimize()

    def SelRequest(self,app):
        window = gw.getWindowsWithTitle(app)[0]
        window.maximize()
        window.activate()
        
    
