import tkinter as tk
from tkinter import ttk

def display_columns():
    list1 = ['Apple', 'Banana', 'Orange', 'Mango']
    list2 = ['Red', 'Yellow', 'Orange', 'Green']

    for item1, item2 in zip(list1, list2):
        if item2 == 'Orange':
            treeview.insert('', tk.END, values=(item1, item2), tags=('orange_value',))
        else:
            treeview.insert('', tk.END, values=(item1, item2))

    treeview.tag_configure('orange_value', foreground='orange')  # Set color for specific values

# Create the Tkinter window
window = tk.Tk()
window.title("Column Display")

# Create a Treeview widget
treeview = ttk.Treeview(window, columns=('Column 1', 'Column 2'))
treeview.heading('Column 1', text='Column 1')
treeview.heading('Column 2', text='Column 2')
treeview.pack()

# Create a button to display the columns
display_button = ttk.Button(window, text="Display Columns", command=display_columns)
display_button.pack()

# Run the Tkinter event loop
window.mainloop()
