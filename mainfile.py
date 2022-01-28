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

import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from m3_meta import set_tags

# SETUP DATA - amend for your use
source_folder = r'c:\users\donal\Documents\ttsimport'  # where you put files to be converted
dest_folder = r'c:\users\donal\Documents\ttsexport'  # where you create converted files
archive_folder = r'c:\users\donal\Documents\ttsarchive'
recordings_folder = r'c:\users\donal\Documents\Sound Recordings'

artist='current book'
album='my album'

# Not using these yet - lets see if we need to
# lines_per_file=10  #number of lines in text or html file before creating new file
# pages_per_file=1  #number of pages in pdf file before creating new file
# so think we use mutagen to set album and artst - but need some rules for this

# https://stackoverflow.com/questions/18369188/python-add-id3-tags-to-mp3-file-that-has- no-tags
# https://methodmatters.github.io/editing-id3-tags-mp3-meta-data-in-python/


engine = pyttsx3.init('sapi5')  # This would need to change for non-windows as sapi is win only
voices = engine.getProperty('voices')
newVoiceRate = 200  # average speech is 150 wpm but I prefer a little faster
engine.setProperty('rate', newVoiceRate)
engine.setProperty('voice', voices[1].id)


def iter_block_items(parent):
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            # yeild paragraphs from table cells
            # Note, it works for single level table (not nested tables)
            table = Table(child, parent)
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        yield paragraph


# we will look to process all files in import directory
def list_files(directory: str, ext=None):
    if ext:
        return (fil for fil in os.listdir(directory) if fil.endswith('.' + ext))
    else:
        return (fil for fil in os.listdir(directory))


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def savechunk(text: str, dest: str, artist, album):
    engine.save_to_file(text, dest)  # Saving Text In a audio file default is 'story.mp3'
    engine.runAndWait()
    set_tags(dest, artist, album)
    return


def save(text: str, dest='story.mp3',  artist='test', album='test', chunksize=20000):
    if len(text) <= chunksize:
        savechunk(text, dest, artist, album)
        return
    part = 1
    while len(text) > chunksize:
        txtpart = "_pt" + str(part)
        split = text.find(". ", chunksize) + 1
        newdest = dest[:-4] + txtpart + ".mp3"
        if not split:
            savechunk(text, newdest)
            break
        else:
            part += 1
            savechunk(text[:split], newdest)
            text = text[split:]
    return


def mp4_to_mp3(fil: str, artist: str, album: str):
    # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
    destname = fil[:-3] + "mp3"
    mp3 = os.path.join(dest_folder, destname)
    mp4 = os.path.join(source_folder, fil)
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close()
    return True


def readpdf(fil: str, artist: str, album: str):
    destname = fil[:-3] + "mp3"
    dest = os.path.join(dest_folder, destname)
    source = os.path.join(source_folder, fil)
    reader = PyPDF2.PdfFileReader(open(source, 'rb'))
    for page_num in range(reader.numPages):
        text = reader.getPage(page_num).extractText()
        cleaned_text = text.strip().replace('\n', ' ')  # Removes unnecessary spaces and break lines
        save(cleaned_text, dest, artist, album )
    return True


def remove_non_ascii(s: str) -> str:
    return "".join(c for c in s if ord(c) < 128)


def readtxt(fil: str, album: str, artist: str) -> bool:
    # This works OK with ansi text - now added remove non ascii to clean up
    destname = fil[:-3] + "mp3"
    dest = os.path.join(dest_folder, destname)
    source = os.path.join(source_folder, fil)
    with open(source, errors='ignore') as fp:
        line = fp.readline()
        cnt = 0
        story = []
        while line:
            if len(line) > 1:  # getting a lot of backslash n read out so added simple length filter
                story.append(remove_non_ascii(line.rstrip("\n")))
                cnt += 1
            line = fp.readline()
        storytext = ''.join(story)
        save(storytext, dest, album, artist)
    return True


def readurl(fil: str, filenam: str, artist: str, album: str) -> bool:
    # These are assumed to be short so no file_splitting
    res = requests.get(fil)
    soup = BeautifulSoup(res.text, 'html.parser')
    print(res.text)
    destname = filenam + ".mp3"
    dest = os.path.join(dest_folder, destname)
    articles = []
    for i in range(len(soup.select('.p'))):
        article = soup.select('.p')[i].getText().strip()
        articles.append(article)
    text = " ".join(articles)
    save(text, dest, album, artist)
    return False


def word_to_mp3(fil: str, artist: str, album: str) -> bool:
    source = os.path.join(source_folder, fil)
    destname = fil[:-4] + "mp3"
    dest = os.path.join(dest_folder, destname)
    articles = []
    doc = docx.Document(source)
    for block in iter_block_items(doc):
        print(block.text)
        articles.append(block.text)
    text = " ".join(articles)
    save(text, dest, album, artist)
    return True


def callbytype(ext, fil, filenam=None, artist='test_artist', album='test_album'):
    if ext == '.pdf':
        result = readpdf(fil, artist, album)
    elif ext == '.txt':
        result = readtxt(fil, artist, album)
    elif ext == '.url':
        result = readurl(fil, filenam, artist, album)
    elif ext == '.mp4':
        result = mp4_to_mp3(fil, artist, album)
    elif ext == '.docx':
        result = word_to_mp3(fil, artist, album)
    else:
        print('Extension ' + ext + ' is not supported yet')
        result = False
    return result


def process_folder(source_folder):
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
                    filename = "url" + str(filecount)
                    result = callbytype('.url', line, filename)
                    line = fp.readline()
                    filecount += 1
        else:
            result = callbytype(extension, file)
        if result:
            shutil.move(sourcelist, archivefile)


if __name__ == "__main__":
    process_folder(source_folder)
    process_folder(recordings_folder)
    engine.stop()
