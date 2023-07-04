import tkinter as tk
from tkinter import *
from tkinter import filedialog
import csv
import pandas as pd
import joblib
import pickle 
import numpy as np
import nltk
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import string
import re
from nltk.stem import WordNetLemmatizer
from string import punctuation
from nltk.corpus import stopwords
from tkinter import ttk



with open('pmbotlogreg.pkl', 'rb') as file:
    logreg = pickle.load(file)


vectorizer=joblib.load('vect.joblib')


app=tk.Tk()
app.geometry('480x500')
app.title('PMbot')
app.config(background='white')
app.attributes('-topmost', True)
app.resizable(0, 0)


def sent_tokens_func(text):
  return nltk.sent_tokenize(text)

def word_tokens_func(text):
  return nltk.word_tokenize(text)  

def to_lower(text):
  if not isinstance(text,str):
    text = str(text)
  return text.lower()

def number_omit_func(text):
  output = ''.join(c for c in text if not c.isdigit())
  return output

def remove_punctuation(text):
  return ''.join(c for c in text if c not in punctuation) 

def stopword_remove_func(sentence):
  stop_words = stopwords.words('english')
  return ' '.join([w for w in nltk.word_tokenize(sentence) if not w in stop_words])

def lemmatize(text):
          wordnet_lemmatizer = WordNetLemmatizer()
          lemmatized_word = [wordnet_lemmatizer.lemmatize(word)for word in nltk.word_tokenize(text)]
          return " ".join(lemmatized_word)

def preprocess(text):
        lower_text = to_lower(text)
        sentence_tokens = sent_tokens_func(lower_text)
        word_list = []
        for each_sent in sentence_tokens:
            lemmatizzed_sent = lemmatize(each_sent)
            clean_text = number_omit_func(lemmatizzed_sent)
            clean_text = remove_punctuation(clean_text)
            clean_text = stopword_remove_func(clean_text)
            word_tokens = word_tokens_func(clean_text)
            for i in word_tokens:
                word_list.append(i)
        return " ".join(word_list)


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        read_csv_file(file_path)

def read_csv_file(file_path):
    df=pd.read_csv(file_path,index_col=False)
    x=df['project_stream'].tolist()
    #print(x)
    l=df['project_stream'].apply(preprocess)
    l=vectorizer.transform(l)
    #print(l)
    predictions =logreg.predict(l)
    # for text, prediction in zip(x, predictions):
    #     if prediction==[0]:
    #         #print('High')
    #         print(f"Text: {text}  Prediction: 'High' ")
    #     elif prediction==[1]:
    #         #print('Low')
    #         print(f"Text: {text}  Prediction: 'Low' ")
    #     else:
    #         #print('Medium')
    #         print(f"Text: {text}  Prediction:'Medium' ")
    #     # print(predictions)
      
    for i1, i2 in zip(x, predictions):
        if i2==[0]:
            #print('High')
            #print(f"Text: {text}  Prediction: 'High' ")
            treeview.insert('', tk.END, values=(i1, 'High'), tags = ('High',))
            #treeview.tag_configure('High', background='#E8E8E8')
        elif i2==[1]:
            #print('Low')
            #print(f"Text: {text}  Prediction: 'Low' ")
            treeview.insert('', tk.END, values=(i1, 'Low'), tags = ('Low',))
        else:
            #print('Medium')
            #print(f"Text: {text}  Prediction:'Medium' ")
            
            treeview.insert('', tk.END, values=(i1, 'Medium'), tags = ('Medium',))
        treeview.tag_configure('High', background='red')
        treeview.tag_configure('Low', background='green',foreground='white')
        treeview.tag_configure('Medium', background='yellow')



style = ttk.Style(app) 
style.theme_use("clam")

treeview = ttk.Treeview(app, columns=('Column 1', 'Column 2'),height=20, show='headings')
treeview.heading('Column 1', text='Project Name')
treeview.heading('Column 2', text='Priority')
treeview.pack()

style.configure('treeview.heading', background="PowderBlue")



l1=Label(app,text='Click the button to input the file',background='white')
l1.pack()


b1=Button(app,background='PowderBlue',text='Input File',command=browse_file)
b1.pack()


app.mainloop()