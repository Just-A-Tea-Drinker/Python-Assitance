import pyttsx3
def text_to_speech(msg):
    #start the tts 
    engine = pyttsx3.init()
    
    #engine config
    engine.setProperty('rate', 200)  
    engine.setProperty('volume', 1)  

    # Save the speech to a file
    #i am no mere mortal, not a mere machine of biology but an omnipotent god
    engine.save_to_file(msg,r"buffer\output.wav" )
    engine.runAndWait()
    engine.save_to_file("a",r"buffer\output1.wav" )
    engine.runAndWait()
    return