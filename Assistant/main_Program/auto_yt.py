
#keyboard input
from pyKey import pressKey, releaseKey

#webscraping/navigation tools
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#large language interpretation
import spacy
nlp = spacy.load("en_core_web_sm")
from spacy.matcher import Matcher

#word numbers to ints
from word2number import w2n

#general
import numpy as np
import random

#custom voice input
import voice_recog_module as sr
import common_funcs as cf
import voice_module as vd #computer tts text into a a wav




    
class Youtube():
    driver = None
    func = []
    short = []
    main_func = ["select","click","read","close"]
    keywords = []
    
    inp_len = 0
    inp_used = False

    phrases = []
    failed = False

    stt =None
    def __init__(self):
        #getting the shortcuts
        self.stt = sr.stt()
        with open(r"complementary\youtube_shortcuts.txt",'r') as file:
                content = file.readlines()
                for lines in content:
                    
                    line = lines.strip().split()
                    if len(line)>0:
                        self.func.append(line[0])
                        self.short.append(line[1])
                file.close()
        with open(r"complementary\youtube_keywords.txt",'r') as file:
                content = file.readlines()
                for lines in content:
                    
                    line = lines.strip().split()
                    if len(line)>0:
                        self.keywords.append(line[0])
                            
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
                        
        
        #starting selenium
        service = Service(verbose = True)
        self.driver = webdriver.Edge(service = service)
        #opening youtube
        self.driver.get('https://www.youtube.com')

        #selecting the reject youtube option
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(("xpath",'//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button'))
            )
            element.click()
        except:
            vd.text_to_speech("Youtube has faled to load")
            time.sleep(cf.GetWait())
            self.failed = True
            self.driver.quit()
            pass
     

    def main_feature(self):
        while True:
            #used to control the main functions of the bot
            try:
                query = ''
                #get any speech/potential commands
                speech = self.stt.speech_to_text().lower()
                
                if cf.acknowledge(speech):
                    sel = random.choice(self.phrases[2])
                    vd.text_to_speech(sel)
                    time.sleep(cf.GetWait())
                    #search for command
                    key_words=self.extract_keywords(speech)
                    
                    common_elements = np.intersect1d(self.keywords, key_words)
                    main_func = False
                    for ele in common_elements:
                        if ele in self.main_func:
                            main_func = True
                            break
                    if len(common_elements)>0 and main_func ==False:
                        to_check = '_'.join(common_elements)
                        #checks the likiness and select the closest match
                        response = self.short[cf.ConfidenceCheck(to_check,self.func)]
                        #now we need to know the command
                        command = self.extract_input(speech)
                        
                        if command != None:
                            
                            #do some more complex phrase building
                            command_pro = command.strip().split()
                            speech_pro = speech.strip().split()
                            query = ''
                            command_index = speech_pro.index(command_pro[0])
                            query = ' '.join(speech_pro[command_index:])
                            
                            #checking to see if something has been inputed before
                            
                            self.ShortCut(response)
                            for i in range(self.inp_len):
                                pressKey("BKSP")
                                time.sleep(0.02)
                                releaseKey("BKSP")
                                time.sleep(0.02)
                            self.inp_used =False
                            #activating the command
                            
                            #inputting the query if neccasary
                            self.autoKeys(query)
                            self.inp_len = len(query)+1
                            self.inp_used =True
                        else:
                            
                            if response =='/':
                                #makig sure there is enough indexes are the common element
                                
                                
                                command_index = key_words.index(common_elements)
                                
                                speech_pro = speech.strip().split()
                                
                                start_query = speech_pro.index(key_words[command_index])
                                
                                query = ' '.join(speech_pro[start_query+1:])
                                
                                
                                #getting rid of the previous inquiray and inputting the new one
                                resp=self.ShortCut(response)
                                for i in range(self.inp_len):
                                    pressKey("BKSP")
                                    time.sleep(0.02)
                                    releaseKey("BKSP")
                                    time.sleep(0.02)
                                self.inp_used =False
                                self.autoKeys(query)
                                self.inp_len = len(query)+1
                                self.inp_used =True
                            else:
                                #activate a youtube short cut
                                
                                self.ShortCut(response)
                    else:
                        #checking for other main function such as reading out titles
                        common_elements = np.intersect1d(self.main_func, key_words)
                        response = None
                        if len(common_elements)>0:
                            response = common_elements[0]
                        
                        
                        if response == "click" or response =="select":
                            #checking if the user is talking about a video or reel
                            #getting the selectable videos and reels
                            elements = self.driver.find_elements(By.ID, 'video-title')
                            all_titles = []
                            for ele in elements:
                                all_titles.append(ele.text)
                            #finding the position of the common element to find a query to losely compare to the titles to select that video
                            speech_split = speech.strip().split()
                            ind = speech_split.index(common_elements[0])
                            to_test = ' '.join(speech_split[ind:])
                            confidence = []
                            for tit in all_titles:
                                confidence.append(cf.Levenshtein.ratio(to_test, tit.lower()))
                                best = max(confidence)
                            title_ind = confidence.index(best)
                            elements[title_ind].click()
                            
                        elif response =="read":
                            #getting all the titles of the video on the page
                            elements = self.driver.find_elements(By.ID, 'video-title')
                            all_titles = []
                            for ele in elements:
                                all_titles.append(ele.text)
                            common = []
                            #ascertaining whether the user wants reels or videos
                            if "real" in common_elements or "reel" in common_elements:
                                elements = self.driver.find_elements(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')
                                titles = []
                                for ele in elements:
                                    titles.append(ele.text)
                                    common = np.setdiff1d(all_titles, titles)
                            if "video" in common_elements:
                                elements = self.driver.find_elements(By.XPATH, '//*[@id="video-title"]/yt-formatted-string')
                                titles = []
                                for ele in elements:
                                    titles.append(ele.text)
                                common = titles
                            # Start the speech in a separate process
                            for tit in common:
                                vd.text_to_speech(tit)
                                # Start listening for the stop command
                                speech = self.stt.speech_to_text()
                                if speech == "stop":
                                    break
                        elif response == "close":
                            self.StopYoutube()
                            break
            except:
                pass   
        #saying the a confirmation message 

    def autoKeys(self,inp):
        for char in inp:
            if char == " ":
                pressKey("SPACEBAR")
                time.sleep(0.02)
                releaseKey("SPACEBAR")
            else:
                
                pressKey(str(char))
                time.sleep(0.02)
                releaseKey(str(char))
        pressKey("ENTER")
        time.sleep(0.02)
        releaseKey("ENTER")

    def ShortCut(self,short):

        match short:
            #search feature
            case "/":
                pressKey(short)
                time.sleep(0.02)
                releaseKey(short)
                return True
            
            #attempting to skip an advert
            case "F5":
                element = self.driver.find_elements(By.XPATH, '//*[@id="skip-button:3"]')
                if len(element)>0:
                    element[0].click()
                else:
                    pressKey(short)
                    time.sleep(0.02)
                    releaseKey(short)

            #going to a previous video
            case "Shift+P":
                pressKey('LSHIFT')
                time.sleep(0.02)
                pressKey('p')
                releaseKey('LSHIFT')
                releaseKey('p')

            #going to the next video
            case "Shift+N":
                pressKey('LSHIFT')
                time.sleep(0.02)
                pressKey('n')
                releaseKey('LSHIFT')
                releaseKey('n')
            
            case ">":
                pressKey('LSHIFT')
                time.sleep(0.02)
                pressKey('.')
                releaseKey('LSHIFT')
                releaseKey('.')

            case "<":
                pressKey('LSHIFT')
                time.sleep(0.02)
                pressKey(',')
                releaseKey('LSHIFT')
                releaseKey(',')
            case default:
                pressKey(short)
                time.sleep(0.05)
                releaseKey(short)
        
    def StopYoutube(self):
        self.driver.quit()    
    def GetMeaning(self,text):
        #function used to actually get an input for the search bar, conceptualises speech into key words,commands phrases

        #finding the command first as the first part of the input
        self.extract_input(text)

    def extract_keywords(self,text):
        keys = []
        text = text.strip().split()
        for words in text:
            if words in self.keywords:
                keys.append(words)
        return keys

    def extract_input(self,text):
        # Process the text with spaCy
        doc = nlp(text)
        
        # Initialize the Matcher with the shared vocabulary
        matcher = Matcher(nlp.vocab)
        
        # Define a pattern to match phrases like "how to fix a car"
        patternhow = [
            {"LOWER": "how"},
            {"IS_ALPHA": True, "OP": "+"}  # Matches one or more alphabetic tokens
        ]
        patternwhy = [
            {"LOWER": "why"},
            {"IS_ALPHA": True, "OP": "+"}  # Matches one or more alphabetic tokens
        ]
        patternwhat = [
            {"LOWER": "what"},
            {"IS_ALPHA": True, "OP": "+"}  # Matches one or more alphabetic tokens
        ]
        patternwhere = [
            {"LOWER": "where"},
            {"IS_ALPHA": True, "OP": "+"}  # Matches one or more alphabetic tokens
        ]
        patternwhen = [
            {"LOWER": "when"},
            {"IS_ALPHA": True, "OP": "+"}  # Matches one or more alphabetic tokens
        ]
     
        # Add the pattern to the matcher
        matcher.add("HOW_PATTERN", [patternhow])
        matcher.add("WHY_PATTERN", [patternwhy])
        matcher.add("WHAT_PATTERN", [patternwhat])
        matcher.add("WHERE_PATTERN", [patternwhere])
        matcher.add("WHEN_PATTERN", [patternwhen])
       
        
        # Apply the matcher to the doc
        matches = matcher(doc)
        
        # Extract the matched span
        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text  # Return the matched phrase
        
        return None  # Return None if no match found