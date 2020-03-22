import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 130)

engine.say("36.7%")
engine.runAndWait()
engine.stop()