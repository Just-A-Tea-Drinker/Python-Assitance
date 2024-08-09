#similarity
import Levenshtein

import librosa

"""
This is where several functions are stored that have a common use case


"""
#simplistic trigger function for the computer to "activate or not, used by most classes"
def acknowledge(speech):
        if speech !=None:
            speech = speech.strip().split()
            for words in speech:
                if words == "computer":
                    return True
            return False
def GetWait():
        y, sr = librosa.load(r"buffer\output.wav", sr=None)
        audio_duration = librosa.get_duration(y=y, sr=sr)
        return audio_duration

#simple confidence check used to find which value input is compared to elements in an inputted list
def ConfidenceCheck(com,toCom):
    confidence = []
   
    for coms in toCom:
        conf = Levenshtein.ratio(coms, com)
        if conf>0.7:
            confidence.append(conf)
        else:
            confidence.append(0.0)
    if len(confidence)>0 :
        best = max(confidence)
        return confidence.index(best)
    else:
        return None

#finds the keywords in "text" that are in the inputted keywords list
def extract_keywords(text,keywords):
    keys = []
    if text !=None:
        text = text.strip().split()
        for words in text:
            if words in keywords:
                keys.append(words)
        return keys