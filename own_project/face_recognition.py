import cv2
import numpy as np
from threading import Timer, Thread
import os 
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
from text_to_speech import say_out_loud

name = None
cam = None
minW = None
minH = None
recognizer = None
cascadePath = "/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
r = sr.Recognizer()
USER_DATA = []
WAIT_SECONDS = 120
id = 0
count_face_appear = 0
path = 'dataset/Users/'
page = requests.get('https://ncov2019.live/data')
soup = BeautifulSoup(page.text, 'html.parser')
ORDER_DATA = []

class users:  
    def __init__(self, id, name, on_camera):
        self.id = id
        self.name = name  
        self.on_camera = on_camera

class VOCAB():
    def __init__(self):
        self.death_vocab = ["dead", "die", "death", "decease", "passed on", "passed away", "perish"]
        self.recovered_vocab = ["recover", "cure", "heal", "rehabilitate"]
        self.confirmed_vocab = ["confirm", "have coronavirus", "coronavirus cases", "infect", "contaminate"]
        self.today_vocab = ["today", "recently", "lately", "just now", "not long ago"]
        self.serious_vocab = ["serious", "danger"]

class collected_data:
    def __init__(self,data):
        self.name = data[0]
        self.confirmed = data[1]
        self.confirmed_changes_today = data[2]
        self.deceased = data[4]
        self.deceased_changes_today = data[5]
        self.recovered = data[7]
        self.serious = data[8]

def find_in_data(place):
    for x in ORDER_DATA:
        if x.name.lower() == place:
            return (x)
    return (None)

def coronavirus_scrapper():
    places_list = soup.find("tbody")
    place_data = places_list.find_all("tr")
    for places in place_data:
        allStats = places.find_all("td")
        order_data = []
        for data in allStats:
            order_data.append(data.get_text().replace("  ","").replace("\n",""))
        ORDER_DATA.append(collected_data(order_data))


def find_vocab_in_speech(speech, vocab):
    for i in vocab:
        if speech.find(i) != -1:
            return True
    return False

def command_help():
    say_out_loud("try to say: How many people got infected today in France or how many people died in Italy")
    user_demand(voice_recognition())

def user_demand(speech):
    if (speech.find("help") != -1):
        command_help()
    speech = speech.replace("corona virus", "coronavirus")
    vocab = VOCAB()
    print (speech)
    try:
        place = speech.split("in ",1)[1]
    except:
        place = "total"
    data_of_place = find_in_data(place)
    if (find_vocab_in_speech(speech, vocab.death_vocab)):
        if find_vocab_in_speech(speech, vocab.today_vocab):
            say_out_loud("Just today " +  data_of_place.deceased_changes_today + " people died in " + place)
        else:
            say_out_loud(data_of_place.deceased + " people died in " + place)
    elif (find_vocab_in_speech(speech, vocab.confirmed_vocab)):
        if find_vocab_in_speech(speech, vocab.today_vocab):
            say_out_loud("Just today " + data_of_place.confirmed_changes_today + " people have been infected by coronavirus in " + place)
        else:
            say_out_loud(data_of_place.confirmed + " people have been infected by coronavirus in " + place)
    elif (find_vocab_in_speech(speech, vocab.recovered_vocab)):
        say_out_loud(data_of_place.recovered + " people have recovered from coronavirus in " + place)
    elif (find_vocab_in_speech(speech, vocab.serious_vocab)):
        say_out_loud(data_of_place.serious + " people are in a serious case because of coronavirus in " + place)
    else:
        say_out_loud("I didn't understand. For some examples of use. say help")
        user_demand(voice_recognition())
    say_out_loud("Do you want other numbers related to coronavirus ?")
    answer = voice_recognition()
    if answer.find("yes") != -1:
        say_out_loud("What numbers do you want to know on coronavirus, say help if you need examples")
        user_demand(voice_recognition())

# with sr.Microphone() as source:
#     audio = r.listen(source)

def voice_recognition():
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        speech = r.recognize_google(audio)
        print(speech)
        if (speech == "stop" or speech == "exit"):
            exit(0)
        return (speech.lower())
    except sr.UnknownValueError:
        say_out_loud("Could you please repeat, I didn't understand")
        return (voice_recognition())
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        say_out_loud("Could you please check if you're connected to internet ?")
        return (voice_recognition())

def getNames(user_list):
    names_array = []
    for f in user_list:
        names_array.insert(int(f.id) - 1, f.name)
    return names_array

def user_gone(id):
    global count_face_appear

    if USER_DATA[id - 1].on_camera == 0:
        print ("restart")
        count_face_appear = 0
        
    else:
        print ("still on camera")
        Timer(WAIT_SECONDS, user_gone, [id]).start()
        USER_DATA[id - 1].on_camera = 0

def register_new_comer(id, name):
    global count_face_appear

    if count_face_appear <= 10:
        count_face_appear += 1
    if count_face_appear == 10:
        USER_DATA.append(users(id, name, 0))
        say_out_loud("Oh hello " + name + ". Do you wish to know numbers about the Coronavirus ?")
        answer = voice_recognition()
        if (answer.find("yes") != -1):
            say_out_loud("Just give me a second, I'm collecting the latest numbers " + name)
            coronavirus_scrapper()
            say_out_loud("Ok, done !")
            say_out_loud("What numbers do you want to know on coronavirus, say help if you need examples")
            user_demand(voice_recognition())
            say_out_loud("Ok then, see you next time " + name)
            USER_DATA[id - 1].on_camera = 0
        else:
            say_out_loud("Ok then, see you next time " + name)
            USER_DATA[id - 1].on_camera = 0
        try:
            Timer(WAIT_SECONDS, user_gone, [id]).start()
        except:
            pass
    if count_face_appear == 11 and USER_DATA[id - 1].on_camera != 1:
        USER_DATA[id - 1].on_camera = 1



def life_cycle(): 
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            if (confidence < 100):
                name = names[id - 1]
                if (100 - confidence > 35):
                    register_new_comer(id, name)
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                name = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

def face_recognition_starter(user_list):
    global names
    global cam
    global minH
    global minW
    global recognizer

    names = getNames(user_list)
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('tmp/trainer.yml')
    life_cycle()
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
