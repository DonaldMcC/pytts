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
# mp4 to mp3 from https://stackoverflow.com/questions/55081352/how-to-convert-mp4-to-mp3-using-python

import pyttsx3
import requests
import PyPDF2
from bs4 import BeautifulSoup
import shutil
from moviepy.editor import *


# SETUP DATA - amend for your use
source_folder = r'c:\users\donal\Documents\ttsimport'  # where you put files to be converted
dest_folder = r'c:\users\donal\Documents\ttsexport'  # where you create converted files
archive_folder = r'c:\users\donal\Documents\ttsarchive'
# Not using these yet - lets see if we need to
# lines_per_file=10  #number of lines in text or html file before creating new file
# pages_per_file=1  #number of pages in pdf file before creating new file
# TODO - may include word files - seems there is a pydocx module for this
# TODO - probably want to populate Album and Artist metadata in the output file

engine = pyttsx3.init('sapi5')  # This would need to change for non-windows as sapi is win only
voices = engine.getProperty('voices')
newVoiceRate = 200  # average speech is 150 wpm but I prefer a little faster
engine.setProperty('rate', newVoiceRate)
engine.setProperty('voice', voices[1].id)


# we will look to process all files in import directory
def list_files(directory, ext=None):
    if ext:
        return (fil for fil in os.listdir(directory) if fil.endswith('.' + ext))
    else:
        return (fil for fil in os.listdir(directory))


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def save(text, dest='story.mp3'):
    engine.save_to_file(text, dest)  # Saving Text In a audio file default is 'story.mp3'
    engine.runAndWait()


def mp4_to_mp3(fil):
    # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
    destname = file[:-3] + "mp3"
    mp3 = os.path.join(dest_folder, destname)
    mp4 = os.path.join(source_folder, fil)
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close()
    return True


def callbytype(ext, file, filename=None):
    if ext == '.pdf':
        result = readpdf(file)
    elif ext == '.txt':
        result = readtxt(file)
    elif ext == '.url':
        result = readurl(file, filename)
    elif ext == '.mp4':
        result = mp4_to_mp3(file)
    else:
        print('Extension ' + ext + ' is not supported yet')
        result = False
    return result


# below needs fixed for multiple pages
def readpdf(fil):
    destname = file[:-3] + "mp3"
    dest = os.path.join(dest_folder, destname)
    source = os.path.join(source_folder, fil)
    reader = PyPDF2.PdfFileReader(open(source, 'rb'))
    for page_num in range(reader.numPages):
        text = reader.getPage(page_num).extractText()
        cleaned_text = text.strip().replace('\n', ' ')  # Removes unnecessary spaces and break lines
        save(cleaned_text, dest)
    return True


def readtxt(fil):
    #This works OK with ansi text - but getting lots of Euro symbol and other stuff from
    #apostrophes without this step when copied and pasted from website
    #will need to deal with this somewhere somehow
    destname = file[:-3] + "mp3"
    dest = os.path.join(dest_folder, destname)
    source = os.path.join(source_folder, fil)
    with open(source, errors='ignore') as fp:
        line = fp.readline()
        cnt = 0
        story = []
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            story.append(line.strip())
            line = fp.readline()
            cnt += 1
        save(story, dest)
    return True


def readurl(fil, filenam):
    # These are assumed to be short so no file_splitting
    res = requests.get(fil)
    soup = BeautifulSoup(res.text, 'html.parser')
    destname = filenam + ".mp3"
    dest = os.path.join(dest_folder, destname)
    articles = []
    for i in range(len(soup.select('.p'))):
        article = soup.select('.p')[i].getText().strip()
        articles.append(article)
    text = " ".join(articles)
    save(text, dest)
    return True


# TODO - possibly support friendly names in url layout I guess
f = list_files(source_folder)
for file in f:
    extension = os.path.splitext(file)[1]
    sourcelist = os.path.join(source_folder, file)
    archivefile = os.path.join(archive_folder, file)
    result = False
    if extension == '.url':
        with open(sourcelist) as fp:
            line = fp.readline()
            filecount = 0
            while line:
                filename = ".url" + str(filecount)
                result = callbytype('.url', line, filename)
                line = fp.readline()
                filecount += 1
    else:
        result = callbytype(extension, file)
    if result:
        shutil.move(sourcelist, archivefile)

engine.stop()
