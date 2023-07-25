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
    style.configure("Title1.TLabel",background=color_hex)
    # color_hex1 = "#{:02x}{:02x}{:02x}".format(r,b, g)
    # style.configure("Title.TLabel",foreground=color_hex1)


#Function to check the priority of the projects of given file 
def check_priority():
    proj_stream=[]
    predictions=[]
    with open('pmbotlogreg.pkl', 'rb') as file:
        logreg = pickle.load(file)


    vectorizer=joblib.load('vect.joblib')

    #app=tk.Tk()


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
            messagebox.showerror('CSV error', 'Please enter valid CSV')

    def back():
        app.destroy()
        main_app.deiconify()

    def selection(event):  
        for i in treeview.selection():  
            item = treeview.item(i)  
            record = item['values']  
            messagebox.showinfo(title = 'Data', message = ''.join(str(record)))  

    def clear_treeview():
        treeview.delete(*treeview.get_children())
        messagebox.showwarning("Alert !!!","Input a CSV now")
        proj_stream.clear()
        predictions.clear()

    def close_main():
        app.destroy()
        main_app.destroy()

    main_app.withdraw()
    app = tk.Tk()
    app.geometry('480x580')
    app.title('PMassistant')
    app.config(background='white')
    app.attributes('-topmost', True)
    app.resizable(0, 0)


    style = ttk.Style(app) 
    style.theme_use("clam")

    style.configure("Custom.TButton", font=("MS Serif", 18), foreground="black", background="PowderBlue")
    style.map("Custom.TButton", foreground=[('active', 'grey')], background=[('active', 'PowderBlue')])

    style.configure("Custom1.TButton", font=("MS Serif", 18), foreground="black", background="DarkOliveGreen1")
    style.map("Custom1.TButton", foreground=[('active', 'grey')], background=[('active', 'DarkOliveGreen2')])

    style.configure("Custom2.TButton", font=("MS Serif", 18), foreground="black", background="red")
    style.map("Custom2.TButton", foreground=[('active', 'grey')], background=[('active', 'red1')])

    style.configure("Custom3.TButton", font=("MS Serif", 18), foreground="black", background="beige")
    style.map("Custom3.TButton", foreground=[('active', 'grey')], background=[('active', 'RosyBrown1')])

    style.configure("Custom.TLabel", font=("MS Serif", 18,'bold'), foreground="brown", background="white")
    l=ttk.Label(app,anchor='center',text='PRIORITY CHECK',style='Custom.TLabel')
    l.pack(pady=10)

    treeview = ttk.Treeview(app, columns=('Column 1', 'Column 2'),height=20, show='headings')
    treeview.heading('Column 1', text='Project Name')
    treeview.heading('Column 2', text='Priority')
    treeview.bind('<<TreeviewSelect>>', selection)  
    treeview.pack()

    style.configure('treeview.heading', background="PowderBlue")
    
    button_frame=tk.Frame(app)
    button_frame.pack(anchor='center')

    b=ttk.Button(button_frame,text='Input File ',command=browse_file, style="Custom.TButton")
    b.pack(side=tk.LEFT)

    b1=ttk.Button(button_frame,text='Back',command=back, style="Custom1.TButton")
    b1.pack(side=tk.LEFT)

    b2=ttk.Button(button_frame,text='Exit',command=close_main, style="Custom2.TButton")
    b2.pack(side=tk.LEFT) 

    b3=ttk.Button(app,text='Clear',command=clear_treeview, style="Custom3.TButton")
    b3.pack(pady=5) 

    app.mainloop()
    #main_app.deiconify()


#Function to check the status of the project of given pdf 
def check_status():
    #Function to check the status of the project of given pdf 
    passfail_status=[]
    pass_status=[]
    fail_status=[]
    undefined_status=[]
    others=[]
    count_all,count_pass,count_fail,count_pf,count_not,count_others=0,0,0,0,0,0
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
                    x=j.replace(" ","")
                    if  'nan' not in i and 'pass/fail' in j.lower():
                        passfail_status.append([i,j])
                    elif r'pass/fail' in x.lower() :
                        passfail_status.append([i,j])
                    elif 'nan' not in i and 'not tested' in j.lower() or 'not shown' in j.lower() or 'not applicable' in j.lower() or 'notapplicable' in j.lower() or 'notshown' in j.lower() or  'nottested' in j.lower() or "not ok" in j.lower() or "notok" in j.lower():
                        undefined_status.append([i,j])
                    elif  'nan' not in i and 'pass' in j.lower() and 'pass/fail' not in j.lower():
                        pass_status.append([i,j])
                    elif  'nan' not in i and 'fail' in j.lower() and 'pass/fail' not in j.lower():
                        fail_status.append([i,j])
                    else:
                        if 'nan' not in i:
                            others.append([i,j])
                except:
                    pass

        if pass_status==[] and fail_status==[] and passfail_status==[] and undefined_status==[]:
            messagebox.showerror('Invalid PDF','Please enter a valid PDF')
        else:    
            on_option_selected()      

    def on_option_selected(*args):
        count_all=len(passfail_status)+len(pass_status)+len(fail_status)+len(undefined_status)+len(others)
        count_fail=len(fail_status)
        count_pass=len(pass_status)
        count_not=len(undefined_status)
        count_pf=len(passfail_status)
        count_others=len(others)

        selected_option = option_var.get()

        if selected_option == "All":
            treeview.delete(*treeview.get_children())
            for i,j in passfail_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('PF',))

            for i,j in pass_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('Pass',))

            for i,j in fail_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('Fail',))

            for i,j in undefined_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('Not',))

            for i,j in others:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('others',))
            lc.config(text=f'[{count_all}]')

        elif selected_option == "Pass/Fail":
            treeview.delete(*treeview.get_children())
            for i,j in passfail_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('PF',))
            lc.config(text=f'[{count_pf}]')

        elif selected_option == "Pass":
            treeview.delete(*treeview.get_children())
            for i,j in pass_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('Pass',))
            lc.config(text=f'[{count_pass}]')


        elif selected_option == "Fail":
            treeview.delete(*treeview.get_children())
            for i,j in fail_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('Fail',))
            lc.config(text=f'[{count_fail}]')


        elif selected_option == "Others":
            treeview.delete(*treeview.get_children())
            for i,j in others:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('others',))
            lc.config(text=f'[{count_others}]')

        elif selected_option == "Not--":
            treeview.delete(*treeview.get_children())
            for i,j in undefined_status:
                s=str(j).replace('\r',' ')
                i=str(i).replace('\r', '')
                j=j.split('–')[-1]
                j=j.split('-')[-1]
                j=str(j).replace('\r','')
                #print(i +" " +j)
                treeview.insert('', tk.END, values=(i,j,s), tags = ('Not',))
            lc.config(text=f'[{count_not}]')

            #print(extracted_data[i])
        treeview.tag_configure('PF', background='orange')
        treeview.tag_configure('Pass', background='green',foreground='white')
        treeview.tag_configure('Fail', background='yellow')
        treeview.tag_configure('Not', background='red')
        treeview.tag_configure('others',background='PowderBlue')


    def selection(event):  
        for i in treeview.selection():  
            item = treeview.item(i)  
            record = item['values']  
            messagebox.showinfo(title = 'Data', message = ''.join(str(record)))  

    def back():
        app.destroy()
        main_app.deiconify()

    def clear_treeview():
        treeview.delete(*treeview.get_children())
        if pass_status==[] and fail_status==[] and passfail_status==[] and undefined_status==[]:
            messagebox.showwarning(title='Alert',message='PDF should be given')
        else:
            messagebox.showwarning(title='Alert',message='New/Old PDF to be given again')
            passfail_status.clear()
            pass_status.clear()
            fail_status.clear()
            undefined_status.clear()
            others.clear()
        #print(extracted_data[1])
        #df=extracted_data[1]
        #print(df)
        #print(df.iloc[:,1:3])


    def close_main():
        app.destroy()
        main_app.destroy()


    main_app.withdraw()
    app=tk.Tk()
    app.geometry('640x690')
    app.title('PMassistant')
    app.config(background='beige')
    app.attributes('-topmost', True)
    app.resizable(0, 0)

    style = ttk.Style(app) 
    style.theme_use("clam")

    style.configure("Custom.TButton", font=("MS Serif", 18), foreground="black", background="PowderBlue")
    style.map("Custom.TButton", foreground=[('active', 'grey')], background=[('active', 'PowderBlue')])

    style.configure("Customm.TButton", font=("MS Serif", 18), foreground="black", background="Red")
    style.map("Customm.TButton", foreground=[('active', 'black')], background=[('active', 'dark red')])

    style.configure("Custommm.TButton", font=("MS Serif", 18), foreground="black", background="coral2")
    style.map("Custommm.TButton", foreground=[('active', 'black')], background=[('active', 'BlanchedAlmond')])

    style.configure("Custom4.TButton", font=("MS Serif", 18), foreground="black", background="DarkOliveGreen1")
    style.map("Custom4.TButton", foreground=[('active', 'grey')], background=[('active', 'DarkOliveGreen2')])

    style.configure("Custom.TLabel", font=("MS Serif", 18,'bold'), foreground="black", background="beige")
    l=ttk.Label(app,anchor='center',text='STATUS CHECK',style='Custom.TLabel')
    l.pack(pady=10)

    treeview = ttk.Treeview(app, columns=('Column 1', 'Column 2','Column 3'),height=20, show='headings')
    treeview.heading('Column 1', text='Ref No.')
    treeview.heading('Column 2', text='Status')
    treeview.heading('Column 3', text='Details')
    treeview.bind('<<TreeviewSelect>>', selection)  
    treeview.pack(pady=10)

    style.configure('treeview.heading', background="PowderBlue")

    button_frame = tk.Frame(app)
    button_frame.config(bg='beige')
    button_frame.pack( anchor="center")

    option_var = tk.StringVar(app)
    options = ["Select an option","All","Pass/Fail" , "Pass", "Fail","Not--","Others"]
    option_var.set(options[0])
    option_menu = ttk.OptionMenu(app, option_var, *options, command=on_option_selected)
    style.configure("Customlc.TLabel", font=("Arial", 14,'bold'), foreground="midnight blue", background="beige")
    lc=ttk.Label(app,text='[COUNT HERE]',style='Customlc.TLabel')
    lc.pack(pady=5)


    b=ttk.Button(button_frame,text='Input PDF',command=select_pdf, style="Custom.TButton")
    b1=ttk.Button(app,text='Exit',command=close_main, style="Customm.TButton")
    clr_b = ttk.Button(button_frame, text="Clear", command=clear_treeview, style="Custommm.TButton")
    b2=ttk.Button(button_frame, text="Back", command=back, style="Custom4.TButton")
    b.pack(padx=5,side=tk.LEFT)
    clr_b.pack(padx=5,side=tk.LEFT)
    b2.pack(padx=5,side=tk.LEFT, fill=tk.Y, expand=True)
    option_menu.pack(pady=5)
    b1.pack(pady=15)
    app.mainloop()


main_app=tk.Tk()
main_app.geometry('480x500')
main_app.config(bg='black')
main_app.attributes('-topmost', True)
main_app.resizable(0, 0)
main_app.title("Project Manager Assistant")


# Created a style to beautify the widgets
style = ttk.Style(main_app)

style.configure("Title1.TLabel", font=("MS Serif", 24), foreground="white",background="black")
style.configure("Custom.TButton", font=("MS Serif", 18), foreground="black", background="black")
style.map("Custom.TButton", foreground=[('active', 'darkblue')], background=[('active', 'black')])

# Created widgets
title_label = ttk.Label(main_app, text="Project Manager Assistant", style="Title1.TLabel")

button1 = ttk.Button(main_app, text="Get Priority", style="Custom.TButton", command=check_priority)
button2 = ttk.Button(main_app, text="Get Status", style="Custom.TButton", command=check_status)


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
