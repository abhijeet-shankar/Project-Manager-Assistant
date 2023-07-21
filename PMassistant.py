import random
import tkinter as tk
from tkinter import filedialog
import tabula
import pandas as pd
import re
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
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


def change_color():
    # Generate random RGB values for dynamic color
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # Convert RGB values to hexadecimal format
    color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    main_app.config(bg=color_hex)
    button_frame.config(bg=color_hex)
    style.configure("Title.TLabel",background=color_hex)
    # color_hex1 = "#{:02x}{:02x}{:02x}".format(r,b, g)
    # style.configure("Title.TLabel",foreground=color_hex1)




#Function to check the priority of the projects of given file 
def check_priority():
    with open('pmbotlogreg.pkl', 'rb') as file:
        logreg = pickle.load(file)


    vectorizer=joblib.load('vect.joblib')


    #app=tk.Tk()
    main_app.withdraw()
    app = tk.Toplevel(main_app)
    app.geometry('480x500')
    app.title('PMassistant')
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
        try:
            df=pd.read_csv(file_path,index_col=False)
            proj_stream=df['project_stream'].tolist()
            #print(x)
            processed_proj_stream=df['project_stream'].apply(preprocess)
            processed_proj_stream=vectorizer.transform(processed_proj_stream)
            #print(l)
            predictions =logreg.predict(processed_proj_stream)
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
            
            for i1, i2 in zip(proj_stream, predictions):
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
        except:
            messagebox.showerror('PDF error', 'Please enter valid pDF')



    style = ttk.Style(app) 
    style.theme_use("clam")
    style.configure("Custom.TButton", font=("MS Serif", 18), foreground="black", background="PowderBlue")
    style.map("Custom.TButton", foreground=[('active', 'grey')], background=[('active', 'PowderBlue')])
    treeview = ttk.Treeview(app, columns=('Column 1', 'Column 2'),height=20, show='headings')
    treeview.heading('Column 1', text='Project Name')
    treeview.heading('Column 2', text='Priority')
    treeview.pack()

    style.configure('treeview.heading', background="PowderBlue")


    b=ttk.Button(app,text='Input File ',command=browse_file, style="Custom.TButton")
    b.pack()


    app.mainloop()
    main_app.deiconify()

#Function to check the status of the project of given pdf 
def check_status():
    passfail_status=[]
    pass_status=[]
    fail_status=[]
    undefined_status=[]
    def select_pdf():
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            read_pdf(file_path)
        else:
            messagebox.showerror('No FIle','Please give a PDF to begin with')


    def read_pdf(file_path):
        # tabula.convert_into("test1.pdf", "output.csv", output_format="csv", pages='all')
        extracted_data = tabula.read_pdf(file_path, pages='all', guess=True)
        #df=pd.read_csv('output.csv',usecols=columns_to_read)
        #print(len(extracted_data))
        for i in range(len(extracted_data)):
            df=extracted_data[i]
            #print(df)
            for i,j in zip(df.iloc[:,1],df.iloc[:,2]):
                try:
                    if 'Pass/Fail' in j:
                        passfail_status.append([i,j])
                    elif 'Pass' in j and 'Pass/Fail' not in j:
                        pass_status.append([i,j])
                    elif 'Fail' in j and 'Pass/Fail' not in j:
                        fail_status.append([i,j])
                    elif 'Not Tested' in j or 'Not Shown' in j or 'Not Applicable' in j:
                        undefined_status.append([i,j])
                except:
                    pass

        if pass_status==[] and fail_status==[] and passfail_status==[] and undefined_status==[]:
            messagebox.showerror('Invalid PDF','Please enter a valid PDF')
        else:               
            for i,j in passfail_status:
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j), tags = ('PF',))

            for i,j in pass_status:
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j), tags = ('Pass',))

            for i,j in fail_status:
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j), tags = ('Fail',))

            for i,j in undefined_status:
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j), tags = ('Not',))
                #print(extracted_data[i])
        treeview.tag_configure('PF', background='orange')
        treeview.tag_configure('Pass', background='green',foreground='white')
        treeview.tag_configure('Fail', background='yellow')
        treeview.tag_configure('Not', background='red')

    #print(extracted_data[1])
    #df=extracted_data[1]
    #print(df)
    #print(df.iloc[:,1:3])
    main_app.withdraw()
    app=tk.Tk()
    app.geometry('480x500')
    app.title('PMassistant')
    app.config(background='white')
    app.attributes('-topmost', True)
    app.resizable(0, 0)


    style = ttk.Style(app) 
    style.theme_use("clam")
    style.configure("Custom.TButton", font=("MS Serif", 18), foreground="black", background="PowderBlue")
    style.map("Custom.TButton", foreground=[('active', 'grey')], background=[('active', 'PowderBlue')])
    treeview = ttk.Treeview(app, columns=('Column 1', 'Column 2'),height=20, show='headings')
    treeview.heading('Column 1', text='Ref No.')
    treeview.heading('Column 2', text='Status')
    treeview.pack()

    style.configure('treeview.heading', background="PowderBlue")



    b=ttk.Button(app,text='Input PDF',command=select_pdf, style="Custom.TButton")
    b.pack()
    app.mainloop()
    main_app.deiconify()


main_app=tk.Tk()
main_app.geometry('480x500')
main_app.config(bg='black')
main_app.attributes('-topmost', True)
main_app.resizable(0, 0)
main_app.title("Project Management Assistant")


# Created a style to beautify the widgets
style = ttk.Style()
style.configure("Title.TLabel", font=("MS Serif", 24), foreground="white",background="black")
style.configure("Custom.TButton", font=("MS Serif", 18), foreground="black", background="black")
style.map("Custom.TButton", foreground=[('active', 'darkblue')], background=[('active', 'black')])

# Created widgets
title_label = ttk.Label(main_app, text="Project Manager Assistant", style="Title.TLabel")

button1 = ttk.Button(main_app, text="Get Priority", style="Custom.TButton", command=check_priority)
button2 = ttk.Button(main_app, text="Get Status", style="Custom.TButton", command=check_status)

# img = tk.PhotoImage(file="pdf.png")
# img1 = img.subsample(10)

# button1.config( text="Get Priority",image=img1,compound=tk.RIGHT)
# button2.config( text="Get Status",image=img1,compound=tk.RIGHT)


# Packed the widgets
title_label.pack(pady=70)
button1.pack(pady=10)
button2.pack(pady=10)

button_frame = tk.Frame(main_app)

button_frame.pack(pady=80)
button_frame.config(bg='black')

style1 = ttk.Style()
style1.configure("Custom.TTButton", font=("MS Serif", 15), foreground="black", background="black")
style1.map("Custom.TTButton", foreground=[('active', 'darkblue')], background=[('active', 'black')])


color_button = ttk.Button(button_frame, text="Change Color", command=change_color,style="Custom.TButton")

exitt=ttk.Button(button_frame, text="Exit", command=main_app.destroy,style="Custom.TButton")
color_button.pack(side=tk.LEFT, padx=10)
exitt.pack(side=tk.LEFT, padx=20)

main_app.mainloop()
#DONE :)