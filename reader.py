import subprocess
import cv2
import pytesseract
import os
from gtts import gTTS
import pygame
from datetime import datetime
import glob
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

directory = "/home/pi/Desktop/Project"

def upload_img(file_name):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    folder = "1G5i-2QbT3fuYGyviqBKbF5BfCxV49ypo"
    file = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : file_name})
    file.SetContentFile(directory + "/_images/" + file_name)
    file.Upload()

def upload_text(file_name):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    folder = "1XiOTXInvhe9_O5tjn0mJVuBHt7hrE7Qp"
    file = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : file_name})
    file.SetContentFile(directory + "/_texts/" + file_name)
    file.Upload()

def upload_audio(file_name):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    folder = "1bigZU0VBXfnsaARg1uXK8PjQEPtc0F9S"
    file = drive.CreateFile({'parents' : [{'id' : folder}], 'title' : file_name})
    file.SetContentFile(directory + "/_audios/" + file_name)
    file.Upload()


def generate_ustring():
    now = datetime.now()
    ustring = now.strftime("%d-%b-%Y_%H.%M.%S")
    return ustring

def capture_img():
    ustring = generate_ustring()
    img_name = "img_" + ustring + ".jpg"
    open("_images/" + img_name, "x")
    subprocess.Popen("sudo fswebcam -r 640x480 _images/" + img_name, shell=True).communicate()
    upload_img(img_name)
    img =cv2.imread("_images/" + img_name)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    return img, ustring

def img_to_text(img, ustring):
    img = cv2.resize(img, (600, 360))
    text = pytesseract.image_to_string(img)
    text = text.replace("\n", " ")
    text_name = "text_" + ustring + ".txt"
    with open("_texts/" + text_name, "w") as f:
        f.write(text)
    upload_text(text_name)
    return text

def text_to_speech(text, ustring):
    audio = gTTS(text = text, lang = 'en', slow = False, tld = 'co.in')
    audio_name = "speech_" + ustring + ".mp3"
    audio.save("_audios/" + audio_name)
    pygame.mixer.init()
    pygame.mixer.music.load("_audios/" + audio_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    upload_audio(audio_name)

def read():
    img, ustring = capture_img()
    time.sleep(0.2)
    text = img_to_text(img, ustring)
    print(text)
    time.sleep(0.2)
    text_to_speech(text, ustring)

def read_again(key):
    files = glob.glob(r'_audios/*mp3')
    if key=="recent1":    
        pygame.mixer.init()
        pygame.mixer.music.load(files[0])
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    if key=="recent2":    
        pygame.mixer.init()
        pygame.mixer.music.load(files[1])
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue






