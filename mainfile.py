# https://medium.com/pythoneers/10-handy-automation-scripts-you-should-try-using-python-fc9450116938
# this merges the pdf and url approaches into a single file for now - I think maybe extending to process
# a list of files of all types would be OK - word documents probably worth looking at as a format too
# and probably also process from a folder if that's easier with archiving after processing - so I just keep
# a list of bookmarks and the like and go with that - still no need for fancy interface perhaps and can run
# with some defaults presumably as well - maybe that handles the input
# output probably we do want some chunking options in the filename and generally we take the input name as basis
# for the ouput I think
# will also need to get the speed correct and part of the options
#pytts test
import pyttsx3
import requests
import PyPDF2
from bs4 import BeautifulSoup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
newVoiceRate = 200                       ## average speech is 150 wpm but I prefer a little faster
engine.setProperty('rate',newVoiceRate)
engine.setProperty('voice', voices[1].id)
def speak(audio):
  engine.say(audio)
  engine.runAndWait()
text = str(input("Paste article\n"))
if text[-3:]=='pdf':
    reader = PyPDF2.PdfFileReader(open(text,'rb'))
    for page_num in range(reader.numPages):
        text = reader.getPage(page_num).extractText()
        cleaned_text = text.strip().replace('\n',' ')  ## Removes unnecessary spaces and break lines
        #print(cleaned_text)                ## Print the text from PDF
        #engine.say(cleaned_text)        ## Let The Speaker Speak The Text
        engine.save_to_file(cleaned_text,'story.mp3')  ## Saving Text In a audio file 'story.mp3'
        engine.runAndWait()
elif text[-3:]=='txt':
    with open(text) as fp:
        line = fp.readline()
        cnt=0
        story=[]
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            story.append(line.strip())
            line = fp.readline()
            cnt+=1
        engine.save_to_file(story, 'story.mp3')  ## Saving Text In a audio file 'story.mp3'
        engine.runAndWait()
else: #url
    res = requests.get(text)
    soup = BeautifulSoup(res.text,'html.parser')
    articles = []
    for i in range(len(soup.select('.p'))):
        article = soup.select('.p')[i].getText().strip()
        articles.append(article)
    text = " ".join(articles)

    #speak(text)
    engine.save_to_file(text, 'test.mp3') ## If you want to save the speech as a audio file
    engine.runAndWait()


engine.stop()

''' 
Link To Try The Script
https://medium.com/@garyvee/a-message-for-those-feeling-lost-in-their-20s-278a878baac2
'''