#!/usr/bin/env python3
# https://medium.com/pythoneers/10-handy-automation-scripts-you-should-try-using-python-fc9450116938
# this will now handle 3 things
# txt files in the import folder
# pdf files in the import folder
# a text file consisting of urls provided it has an extension of .url
# there should now be no actual input the program just runs
# word documents probably worth looking at as a format too
# output probably we do want some chunking options in the filename and generally we take the input name as basis
# for the ouput I think
# will also need to get the speed correct and part of the options
#pytts test
import pyttsx3
import requests
import PyPDF2
from bs4 import BeautifulSoup
import os

#SETUP DATA - amend for your use
source_folder = r'c:\users\donal\Documents\ttsimport'  # where you put files to be converted
dest_folder = r'c:\users\donal\Documents\ttsexport' # where you create converted files

#Not using these yet - lets see if we need to
#lines_per_file=10  #number of lines in text or html file before creating new file
#pages_per_file=1  #number of pages in pdf file before creating new file

engine = pyttsx3.init('sapi5')  #This would need to change for non-windows as sapi is win only
voices = engine.getProperty('voices')
newVoiceRate = 200                       ## average speech is 150 wpm but I prefer a little faster
engine.setProperty('rate',newVoiceRate)
engine.setProperty('voice', voices[1].id)

#we will look to process all files in import directory
def list_files(directory, extension=None):
    if extension:
        return (f for f in os.listdir(directory) if f.endswith('.' + extension))
    else:
        return (f for f in os.listdir(directory))


def speak(audio):
  engine.say(audio)
  engine.runAndWait()


def save(text, dest='story.mp3'):
  engine.save_to_file(text, dest)  ## Saving Text In a audio file default is 'story.mp3'
  engine.runAndWait()


def callbytype(extension, source):
    if extension=='pdf':
        readpdf(source)
    elif extension=='txt':
        readtxt(source)
    elif extension=='url':
        readurl(source)
    else:
        print('Extension '+ extension + ' is not supported yet')


# below needs fixed for multiple pages
def readpdf(file):
    reader = PyPDF2.PdfFileReader(open(file,'rb'))
    for page_num in range(reader.numPages):
        text = reader.getPage(page_num).extractText()
        cleaned_text = text.strip().replace('\n',' ')  ## Removes unnecessary spaces and break lines
        save(cleaned_text, dest)
    return


def readtxt(file):
    with open(file) as fp:
        line = fp.readline()
        cnt=0
        story=[]
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            story.append(line.strip())
            line = fp.readline()
            cnt+=1
        save(story, dest)


def readurl(file):
    #These are assumed to be short so no file_splitting
    res = requests.get(text)
    soup = BeautifulSoup(res.text,'html.parser')
    destname = file[:-3] + "mp3"
    dest = os.path.join(dest_folder, destname)
    articles = []
    for i in range(len(soup.select('.p'))):
        article = soup.select('.p')[i].getText().strip()
        articles.append(article)
    text = " ".join(articles)
    save(text, dest)


f = list_files(source)
for file in f:
    with open(os.path.join(source, file)) as textfile:
        extension=file[-3:]
        if extension == 'url':
            with open(file) as fp:
                line = fp.readline()
                while line:
                    callbytype('url', line)
                    line = fp.readline()
        else:
            callbytype(extension, file)
engine.stop()

