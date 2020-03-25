import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 130)

def say_out_loud(text):
    engine.say(text)
    engine.runAndWait()
    engine.stop()