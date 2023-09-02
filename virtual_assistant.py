import speech_recognition as sr
import pygame
import json
import random


with open("_default_responses/_responses.txt", "r") as fp:
    responses = json.load(fp)

def respond(responseKey):
    response = random.choice(responses.get(responseKey))
    pygame.mixer.init()
    pygame.mixer.music.load("_default_responses/" + response + ".mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.quit()

def listen():
    r = sr.Recognizer()
    data = ""
    with sr.Microphone() as source:
        print("I am listening...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            data = r.recognize_google(audio)
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            respond("UnknownValueError")
        except sr.RequestError as e:
            print("Request Failed; {0}".format(e))
    return data


