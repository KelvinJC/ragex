import speech_recognition as sr
import pyttsx3 


# Initialize the recognizer 
r = sr.Recognizer() 

def recognise_speech(file):
    # Loop infinitely for user to speak
    while(1):    
        print("Bot listening...")
        try:
            # use the audio file as source for input.
            with sr.AudioFile(file) as source2:
                # wait for a second to let the recognizer adjust the energy threshold based on
                # the surrounding noise level 
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                # listen for the user's speech input 
                speech_input = r.listen(source2)
                
                # use google to recognize audio
                text_output = r.recognize_google(speech_input)
                text_output = text_output.lower()
                return text_output                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")


def speak_text(text: str):
    """ Convert provided text to speech"""
    engine = pyttsx3.init()
    engine.say(text) 
    engine.runAndWait()