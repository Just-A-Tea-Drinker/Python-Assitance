#email function based on: https://www.makeuseof.com/send-outlook-emails-using-python/
#os and scheduling
import time
import os
import threading as th

#custom imports
import voice_recog_module as sr #voice recogntition google api based
import voice_module as vd #computer tts text into a a wav
import visual_face as vf
import common_funcs as cf
import app_manager as ao


#misc imports 
import random
import win32com.client

class main_frame:
    """MAIN_FRAME 
    info:
    main frame is the spine of the applicatiions hosting core functions such as:
        - app configuration
        - user interaction/config
        - opening files 
        - starting other app specialised classes
        - initialising core components such as GUI
    
    inputs:
    microphone/sound

    outputs:
    N/a
    """
    #user config
    info = []
    name = None # username
    #programmed speeches
    phrases = []
    
    #object place holders
    stt = None
    appMan =None

    #keywords
    com_keys =[] #used to hold the keyword for key command like open,close etc
    app_names = [] #storage for the names of the applications

    #commands
    commands = []
    command=None

    tabs=[]

    #contacts for the emails
    contact_e = []
    contact_name = []




    def __init__(self):
        #starting the queue for the processes returns
        self.stt = sr.stt()
        self.appMan= ao.AppManager()
        self.app_names = self.appMan.apps

        #load in the userconfig file
        if not os.path.exists(r"complementary\Userconfig.txt"):
            with open(r"complementary\Userconfig.txt",'w') as file:
                file.close()
        else:
            with open(r"complementary\Userconfig.txt",'r') as file:
                content = file.readlines()
                for lines in content:
                    
                    line = lines.strip()
                    if len(line)>0:
                        self.info.append(line)
                
            file.close()
        #load in scripts and phrases
        with open(r"complementary\phrases.txt",'r') as file:
            content = file.readlines()
            temp = []
            
            for lines in content:
                line = lines.strip()
                
                if len(line)>0:
                    temp.append(line)
                else:
                    self.phrases.append(temp)
                    temp = []
            self.phrases.append(temp)
        file.close()
        
        #getting potential commands
        with open(r"complementary\mainFrame_keywords.txt",'r') as file:
            content = file.readlines()
            for lines in content:
                
                line = lines.strip()
                self.com_keys.append(line)
        file.close()
        
        with open(r"complementary\mainFrame_commands.txt",'r') as file:
            content = file.readlines()
            for lines in content:
                line = lines.strip()
                if len(line)>0:
                    self.commands.append(line)
            file.close()

        with open(r"complementary\email_contacts.txt",'r') as file:
            content = file.readlines()
            for lines in content:
                
                line = lines.strip().split()
                if len(line)>0:
                    self.contact_e.append(line[0])
                    self.contact_name.append(line[1])
            file.close()

        #startting the visual component
        event = th.Event()
        visual = th.Thread(target=vf.run,args=(event,))
        visual.start()
        event.wait()
        
        #gettig the user config or welcoming a returning user
        self.GetUser()
        #starting the main featue
        self.main_frame()

    def GetUser(self):
        if len(self.info) == 0:
            #starting the intro sequence
            vd.text_to_speech(self.phrases[0][0])
            time.sleep(cf.GetWait())
            #getting the name of the user
            while True:
                vd.text_to_speech(self.phrases[0][1])
                time.sleep(cf.GetWait())
                while self.name ==None:
                    self.name =self.stt.speech_to_text()
                    if self.name == None:
                        vd.text_to_speech(self.phrases[0][6])
                        time.sleep(cf.GetWait())

                confirm_msg = self.phrases[0][2]+" "+self.name
                vd.text_to_speech(confirm_msg)
                time.sleep(cf.GetWait())
                
                confirm =self.stt.speech_to_text()
                
                confirm =confirm.lower().strip().split()
                if "yes" in confirm:
                    break
                else:
                    self.name = None
                
                    
            msg = "okay "+self.name+" "+self.phrases[0][3]
            vd.text_to_speech(msg)
            time.sleep(cf.GetWait())
            

            #call file edit to remember the name
            self.info.append(self.name)
            self.InfoEdit()
            #telling the user how to use the computer
            vd.text_to_speech(self.phrases[0][4])

        else:
            return_msg = self.phrases[0][5] + " " +self.info[0]
            vd.text_to_speech(return_msg)
            time.sleep(cf.GetWait())
            #reminding the user how to use the computer
            vd.text_to_speech(self.phrases[0][7])
            time.sleep(cf.GetWait())

        #starting the main function for listening for commands
        #attempting to use two threads running to not have a gap

    def InfoEdit(self):
        ##main function used to store the information like user name
        with open(r"complementary\Userconfig.txt",'a') as file:
                for lines in self.info:
     
                    file.write(f'{lines}')
   

    def AppInteract(self,speech,act):
        tempApps=[]
        for app in self.app_names:
            tempApps.append(app.upper())
        
        #adding another option that isnt strictly an app
        tempApps.append('YOUTUBE')
        #speech = speech.upper().strip().split()

       
        #finding the most likely application that needs to be opened
        apps2sort = []
        found_apps = [app for app in tempApps if app in speech.upper()]
        for app in found_apps:
            apps2sort.append(self.app_names[tempApps.index(app)])
                 
        match act:
            case "Open":
                self.appMan.OpenRequest(apps2sort)
            case "Close":
                self.appMan.CloseRequest(apps2sort)
            case "Maxi":
                self.appMan.MaxiRequest(apps2sort)
            case "Mini":
                self.appMan.MiniRequest(apps2sort)
            case "switch_monitor"|"swap_monitor":
                self.appMan.MoveRequest(apps2sort)
            case "switch_to"|"swap_to"|"select":
                self.appMan.SelRequest(apps2sort[0])

    def EmailHandle(self,speech):
        #this is where you can send an email using your voice as long as you have contacts of course
        tempNames=[]
        for app in self.contact_name:
            tempNames.append(app.upper())
        speech = speech.upper().strip().split()
        #finding the most likely application that needs to be opened
        names = []
        for word in speech:
            for app in tempNames:
                
                conf = cf.Levenshtein.ratio(word,app)
                if conf>0.8:
                    names.append(self.contact_e[tempNames.index(app)])
        
        #now that we have the name/contact we canget hold of the subject text and the main body of the email.
        ol=win32com.client.Dispatch("outlook.application")
        olmailitem=0x0 #size of the new email
        newmail=ol.CreateItem(olmailitem)

        #getting the subject
        subject = None
        body = None
        try:
            newmail.To=names[0]
        except:
            return
        
        
        #getting the users subject content
        while subject ==None:
            vd.text_to_speech(self.phrases[3][0])
            time.sleep(cf.GetWait())
            subject =self.stt.speech_to_text()
        newmail.Subject= subject

        while body ==None:
            vd.text_to_speech(self.phrases[3][1])
            time.sleep(cf.GetWait())
            body =self.stt.speech_to_text()
        newmail.Body= body
        newmail.Send()
        vd.text_to_speech(self.phrases[3][2])
        time.sleep(cf.GetWait())

    def ActivateCom(self,speech):
        #obtaining an update of the tabs opened
        self.tabs=self.appMan.OS_Obj.GetCurrentTabs()
        #taking a given command and activating its contents
        match self.command:
            case "send_email":
                self.EmailHandle(speech)
            case "open":
                self.AppInteract(speech,"Open")
            case "close":
                self.AppInteract(speech,"Close")
            case "maximise":
                self.AppInteract(speech,"Maxi")
            case "minimise":
                self.AppInteract(speech,"Mini")
            case "switch_monitor"|"swap_monitor":
                self.AppInteract(speech,"Monitor")
            case "switch_to"|"swap_to":
                self.AppInteract(speech,"Switch")
            
            
    
    def main_frame(self):
        #this will be where the computer awaits commands from th

        #making the procsses for the voice recognition these will work together to hopefully avoid any gaps
        while True:
            #calling the speech recognition repeatedly to obtain keywords or commands
            speech = self.stt.speech_to_text()
            if cf.acknowledge(speech):
                
                #keep trying for a command
                while True:
                    keyGet = cf.extract_keywords(speech,self.com_keys)
                    if keyGet!=None:
                        to_check = '_'.join(keyGet)
                        ind = cf.ConfidenceCheck(to_check,self.commands)
                        if ind!=None:
                            self.command = self.commands[ind]
                            break
                        else:
                            vd.text_to_speech(self.phrases[0][8])
                            time.sleep(cf.GetWait())
                #hopefully now we should have a command and now we acivate it
                sel = random.choice(self.phrases[2])
                vd.text_to_speech(sel)
                time.sleep(cf.GetWait())
                self.ActivateCom(speech)
                           

if __name__ == "__main__":
    obj = main_frame()