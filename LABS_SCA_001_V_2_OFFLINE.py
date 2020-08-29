# This is a PDF to AudioBook Simple Python script.
# LABS-SCA-001-V-001-OFFLINE
# Dependencies : pyttsx3; PyPDF2
# Bakenon request
#
import time
start_time = time.time() # Start measuring processing time

import os
from os.path import expanduser
home_dir_all_python = expanduser("~") # get the home directory working for all version of Python
from pathlib import Path
home_dir_python35_and_above_only = str(Path.home()) # get the home directory working for Python 3.5+

from tkinter import *
from tkinter import filedialog

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

fileToBeProcessedLocation = filedialog.askopenfilename(initialdir=home_dir_all_python, title="Select the file to be processed")# Get the location of the pdf file

print("Running time" + " : *** %s seconds ***" % (time.time() - start_time))

pdf_base_name=os.path.basename(fileToBeProcessedLocation)# get the pdf file name without extention [0]

# OFFLINE VERSION
import pyttsx3
import PyPDF2

pdf_file_name = open(fileToBeProcessedLocation,'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file_name)
pages = pdf_reader.numPages

converter = pyttsx3.init()
print('playing....')

newVoiceRate = 100
converter.setProperty('rate',newVoiceRate)


for num in range(0,pages):
    page = pdf_reader.getPage(num)
    text = page.extractText()
    converter.say(text)
    converter.save_to_file(text,home_dir_all_python+"/"+os.path.splitext(os.path.basename(fileToBeProcessedLocation))[0]+"_offline.mp3")
    converter.runAndWait()
print("Your Code made" + " : *** %s seconds *** " % (time.time() - start_time) + "to run")