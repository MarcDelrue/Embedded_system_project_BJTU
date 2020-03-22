import speech_recognition as sr


class VOCAB():
    def __init__(self):
        self.death_vocab = ["dead", "die", "death", "decease", "passed on", "passed away", "perish"]
        self.recovered_vocab = ["recover", "cure", "heal", "rehabilitate"]
        self.confirmed_vocab = ["confirm", "have coronavirus", "coronavirus cases", "infect", "contaminate"]
        self.today_vocab = ["today", "recently", "lately", "just now", "not long ago"]
        self.serious_vocab = ["serious", "danger"]

def find_vocab_in_speech(speech, vocab):
    for i in vocab:
        if speech.find(i) != -1:
            return True
    return False

def user_demand(speech):
    speech = speech.lower().replace("corona virus", "coronavirus")
    vocab = VOCAB()
    print (speech)
    try:
        place = speech.split("in ",1)[1]
    except:
        place = "global"
    print(place)
    if (find_vocab_in_speech(speech, vocab.death_vocab)):
        if find_vocab_in_speech(speech, vocab.today_vocab):
            print("death today")
        else:
            print("total death")
    elif (find_vocab_in_speech(speech, vocab.confirmed_vocab)):
        if find_vocab_in_speech(speech, vocab.today_vocab):
            print("confirmed today")
        else:
            print("total confirmed")
    elif (find_vocab_in_speech(speech, vocab.recovered_vocab)):
        print("cured")
    elif (find_vocab_in_speech(speech, vocab.serious_vocab)):
        print("serious")
    else:
        print("didn't understand")

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    speech = r.recognize_google(audio)
    print(speech)
    user_demand(speech)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
