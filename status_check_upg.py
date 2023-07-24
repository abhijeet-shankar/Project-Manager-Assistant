import tkinter as tk
from tkinter import filedialog
import tabula
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import string
#Function to check the status of the project of given pdf 

passfail_status=[]
pass_status=[]
fail_status=[]
undefined_status=[]
others=[]
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
                if  'nan' not in i and 'pass/fail' in j.lower():
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
    selected_option = option_var.get()
    if selected_option == "All":
        treeview.delete(*treeview.get_children())
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

        for i,j in others:
            i=str(i).replace('\r', '')
            j=j.split('–')[-1]
            j=j.split('-')[-1]
            j=str(j).replace('\r','')
            #print(i +" " +j)
            treeview.insert('', tk.END, values=(i,j), tags = ('others',))

    elif selected_option == "Pass/Fail":
        treeview.delete(*treeview.get_children())
        for i,j in passfail_status:
            i=str(i).replace('\r', '')
            j=j.split('–')[-1]
            j=j.split('-')[-1]
            j=str(j).replace('\r','')
            #print(i +" " +j)
            treeview.insert('', tk.END, values=(i,j), tags = ('PF',))

    elif selected_option == "Pass":
        treeview.delete(*treeview.get_children())
        for i,j in pass_status:
            i=str(i).replace('\r', '')
            j=j.split('–')[-1]
            j=j.split('-')[-1]
            j=str(j).replace('\r','')
            #print(i +" " +j)
            treeview.insert('', tk.END, values=(i,j), tags = ('Pass',))


    elif selected_option == "Fail":
        treeview.delete(*treeview.get_children())
        for i,j in fail_status:
            i=str(i).replace('\r', '')
            j=j.split('–')[-1]
            j=j.split('-')[-1]
            j=str(j).replace('\r','')
            #print(i +" " +j)
            treeview.insert('', tk.END, values=(i,j), tags = ('Fail',))


    elif selected_option == "Others":
        treeview.delete(*treeview.get_children())
        for i,j in others:
            i=str(i).replace('\r', '')
            j=j.split('–')[-1]
            j=j.split('-')[-1]
            j=str(j).replace('\r','')
            #print(i +" " +j)
            treeview.insert('', tk.END, values=(i,j), tags = ('others',))

    elif selected_option == "Not--":
        treeview.delete(*treeview.get_children())
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
    treeview.tag_configure('others',background='PowderBlue')


def selection(event):  
    for i in treeview.selection():  
        item = treeview.item(i)  
        record = item['values']  
        messagebox.showinfo(title = 'Data', message = ''.join(str(record)))  

# def copy_selected():
#     for i in treeview.selection():  
#         item = treeview.item(i)  
#         record = item['values']  
#         text= ''.join(str(record))
#         app.clipboard_clear()
#         app.clipboard_append(text)

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

app=tk.Tk()
app.geometry('480x560')
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

style.configure("Custom.TLabel", font=("MS Serif", 18,'bold'), foreground="black", background="beige")
l=ttk.Label(app,anchor='center',text='STATUS CHECK',style='Custom.TLabel')
l.pack(pady=10)

treeview = ttk.Treeview(app, columns=('Column 1', 'Column 2'),height=20, show='headings')
treeview.heading('Column 1', text='Ref No.')
treeview.heading('Column 2', text='Status')
treeview.bind('<<TreeviewSelect>>', selection)  
# treeview.bind("<Control-c>", lambda event: copy_selected())

treeview.pack()

style.configure('treeview.heading', background="PowderBlue")

button_frame = tk.Frame(app)
button_frame.config(bg='beige')
button_frame.pack( anchor="center")

option_var = tk.StringVar(app)

options = ["Select an option","All","Pass/Fail" , "Pass", "Fail","Not--","Others"]

option_var.set(options[0])

option_menu = ttk.OptionMenu(app, option_var, *options, command=on_option_selected)
option_menu.pack()


b=ttk.Button(button_frame,text='Input PDF',command=select_pdf, style="Custom.TButton")
b1=ttk.Button(button_frame,text='Exit',command=app.destroy, style="Customm.TButton")
clr_b = ttk.Button(button_frame, text="Clear", command=clear_treeview, style="Custommm.TButton")
b.pack(padx=5,side=tk.LEFT)
clr_b.pack(padx=5,side=tk.LEFT)
b1.pack(padx=5,side=tk.LEFT, fill=tk.Y, expand=True)
app.mainloop()

