from easygui import buttonbox
import speech_recognition as sr
import socket
from googletrans import Translator
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from itertools import count
import matplotlib.pyplot as plt
import numpy as np
import string 

translator = Translator()

gif_lst=['any questions', 'are you angry','are you hungry', 'be careful', 'do you have money', 'do you watch tv',
         'good morning','good question','happy journey', 'what is your name', 'i have a headache', 'nice to meet you',
         'open the door', 'call me later', 'give me your pen', 'can i help you', 'sit down',  'what are you doing',
         'what is your job', 'what is your mobile number', 'when will we go', 'where do you live', 'you are wrong' 
         'where is the bathroom','where is the police station','banana','bangalore','are you busy','address','bridge']

lst=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def is_connected():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname("one.one.one.one")
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False

def animate(aud1,aud):
    if(aud1 in gif_lst):
        class ImageLabel(tk.Label):
                def load(self, img):
                    if isinstance(img, str):
                        img = Image.open(img)
                    self.loc = 0
                    self.frames = []
                    try:
                        for i in count(1):
                            self.frames.append(ImageTk.PhotoImage(img.copy()))
                            img.seek(i)
                    except EOFError:
                        pass
                    try:
                        self.delay = img.info['duration']
                    except:
                        self.delay = 100
                    if len(self.frames) == 1:
                        self.config(image=self.frames[0])
                    else:
                        self.next_frame()

                def unload(self):
                    self.config(image=None)
                    self.frames = None

                def next_frame(self):
                    if self.frames:
                        self.loc += 1
                        self.loc %= len(self.frames)
                        self.config(image=self.frames[self.loc])
                        self.after(self.delay, self.next_frame)
        root = tk.Tk()
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load(r'Indian_Speech_Language_GIFS/{0}.gif'.format(aud1))
        text=Text(root,height=5)
        text.insert(INSERT,aud)
        text.pack()
        Button(root, text="Quit", command=root.destroy).pack()
        root.mainloop()
        
    else:
        for i in range(len(aud1)):
            if(aud1[i] in lst): 
                ImageAddress = 'Alphabets/'+aud1[i]+'.jpg'
                ImageItself = Image.open(ImageAddress)
                ImageNumpyFormat = np.asarray(ImageItself)
                plt.imshow(ImageNumpyFormat)
                plt.draw()
                plt.text(530,-40,aud,fontsize=12)
                plt.pause(0.8)
                if(i==len(aud1)-1):
                    plt.pause(0.8)
                    plt.close()
            else:
                continue



def takeCommandTelugu():
    aud=""
    if is_connected():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            r.pause_threshold = 0.7
            audio = r.listen(source)
            try:
                print("Recognizing")
                Query = r.recognize_google(audio, language="te-IN")
                result = translator.translate(Query, src="te", dest="en")
                print(result.text.lower())
                aud=result.text.lower()
            except Exception as e:
                print(e)
                print("Oops! Say That Again...")
                return "None"
            #return Query
    else:
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            r.pause_threshold = 0.7
            audio = r.listen(source)
            try:
                print("Recognizing")
                Query=r.recognize_sphinx(audio)
                print(Query)
                aud=Query
            except sr.UnknownValueError:  
                print("Oops! Say That Again...")  
            except sr.RequestError as e:  
                print("Sphinx error; {0}".format(e))
            #return Query
    aud1=aud.lower()
    for c in string.punctuation:
        aud1=aud1.replace(c,"")
    animate(aud1,aud)


# Driver Code
i=0
while(True):
    ch=["Speak", "Exit"]
    if(i>0):ch[0]="Speak Again"
    box=buttonbox("Speech to Sign Language",image="Sign.png",choices=ch)
    i+=1
    if(box==ch[0]):
        takeCommandTelugu()
    else:
        quit()