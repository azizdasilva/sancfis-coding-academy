# This is a PDF to AudioBook Simple Python script.
# LABS-SCA-001-V-001
# DEPENDENCIES
#
#
#
#
#
#
#
#
#
#
#


import os
import pyttsx3
import pdftotext
from tkinter import *
from tkinter import filedialog
from langdetect import detect
from gtts import gTTS
from os.path import expanduser


home_dir_all_python = expanduser("~") # get the home directory working for all version of Python
from pathlib import Path
home_dir_python35_and_above_only = str(Path.home()) # get the home directory working for Python 3.5+


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

fileToBeProcessedLocation = filedialog.askopenfilename(initialdir=home_dir_all_python, title="Select the file to be processed")# Get the location of the pdf file

pdf_base_name=os.path.basename(fileToBeProcessedLocation) # get the pdf file name without extention
mp3_base_name=os.path.splitext(pdf_base_name)[0] # Build the mp3 base name according to the pdf

with open(fileToBeProcessedLocation, "rb") as fileToBeProcessed:  # open the file in reading (rb) mode and call it fileToBeProcessed
    pdf_txt_version = pdftotext.PDF(fileToBeProcessed)  # store a text version of the pdf file fileToBeProcessed in pdf variable
print("CONVERTION IN PROGRESS")
# Extract the text from the pdf to buld a string
string_of_text = ''
for text in pdf_txt_version:
    string_of_text += text

pdf_lang = detect(string_of_text) # detect the pdf file language

final_file = gTTS(text=string_of_text, lang=pdf_lang)  # store file in variable
final_file.save(home_dir_all_python+"/"+mp3_base_name+"_online.mp3")  # save file to the same location that the pdf
print("CONVERTION FINISHED")
print("You can find your mp3 file here: "+home_dir_all_python+"/"+mp3_base_name+"_online.mp3")

