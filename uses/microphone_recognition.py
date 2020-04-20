#!/usr/bin/env python3

import speech_recognition as sr
import os
import subprocess
from pynput.keyboard import Key, Controller
import time


# instatiate recognizer instance
r = sr.Recognizer()

# list available microphones
print('\nCurrently available Microphones')
print('-----------------------------------------------------')
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("\nMicrophone with name \"{1}\" found for `Microphone(device_index={0})`".format(
        index, name))

# amount of time microphone keeps listening after a pause
# r.pause_threshold = 1

print('\n-----------------------------------------------------')

# define file paths
steel_viking = "C:\Steel Viking\SteelViking.exe"
steel_viking_update = "C:\Steel Viking\Steel Viking Update Tool.vbs"


def open_steel_viking():
    # open steel viking update tool
    print("Opening Steel Viking...", steel_viking_update)
    subprocess.call(["cscript", steel_viking_update])

    # give time for steel viking message box to open and hit ok
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
  

    # open steel viking
    # print("Opening Steel Viking...", steel_viking)
    # subprocess.Popen(steel_viking)


# Speech to key press
keyboard = Controller()
exit_words = ['exit', 'Exit', 'stop', 'Stop', 'quit', 'Quit']

def speech_to_key_press():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=.5)
        print("\nSpeak anytime")
        audio = r.listen(source, timeout=30, phrase_time_limit=15)
        # as long as audio is listening type what is said
        while audio:
            keyboard.type(r.recognize_google(audio))
            exit_words_match_source = any(exit_word in r.recognize_google(audio) for exit_word in exit_words)
            if (exit_words_match_source):
                print('You said an exit command, exiting SV assistant')
                exit()
            else:            
                speech_to_key_press()


# Keywords that will trigger opening SV. Accounts for mispronunciation, or different dialects.
keywords = [
    "steel", "Steel", "viking", "Viking", "still", "Still", "biking", "Biking", "seal", "Seal", "sealed", "Sealed", "steal", "Steal","decking", "Decking", "making", "Making"
]


# obtain audio from the microphone
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=.5)
    print("\nSpeak anytime")
    audio = r.listen(source, timeout=3, phrase_time_limit=4)


# recognize speech using Google Speech Recognition
try:
    print("You said: " + r.recognize_google(audio))

    # check if any keywords match the source
    keyword_matches_source = any(keyword in r.recognize_google(audio) for keyword in keywords)

    # If any of the keywords were captured open Steel Viking
    if (keyword_matches_source):
        open_steel_viking()
        # start speech to type for login
        speech_to_key_press()


except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))



