import speech_recognition as sr

class stt:
    recognizer = None
    text = None
    def __init__(self):
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()

    # Function to convert speech to text
    def speech_to_text(self):
        # Use the microphone as the source for input
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")

            # Capture the audio from the microphone
            audio_data = self.recognizer.listen(source)

            # Recognize speech using Google Web Speech API
            try:
                
                self.text = self.recognizer.recognize_google(audio_data)
                return self.text
            except sr.UnknownValueError:
                return None