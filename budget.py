#All necessary Packages
from tkinter import messagebox, ttk, Button, Frame, Label, Scrollbar, Toplevel, PhotoImage, BOTTOM, LEFT, RIGHT, CENTER, X, Y, Tk, Entry, NW, END, Text, StringVar
from tkinter.ttk import Style, Treeview
from tkcalendar import DateEntry
import datetime
<<<<<<< HEAD
import sqlite3
import sqlite3
=======
import sqlite3 
>>>>>>> 0fe8a7936ff03ba52f8cfb3f91196a25ee02ce32
from json import dumps, loads

#Styles
book_antiqua=("Helvetica Neue Light",12,"normal")
arial=('Arial', 12)
book_antiqua_size18=("Book Antiqua",18,"bold")

frame_color='#242729'

element_color='white'
entry_box_color='#666869'

menu_button_color='#0b5a8c'
frame_button_color='#165a72'

tree_view_color_bg='#242729'
tree_view_color_fg='#242729'

selection_color='darkblue'

menu_button_height=4

def scroll_bar(frame_name,widget):
    if frame_name=='menu_frame':
        v = Scrollbar(widget, orient = 'vertical')
        v.pack(side = LEFT, fill = Y)
    else:
        h = Scrollbar(widget, orient = 'horizontal')
        h.pack(side = BOTTOM, fill = X)
        v = Scrollbar(widget,orient = 'vertical')
        v.pack(side = RIGHT, fill = Y)

#Validation
def validation_2charecters(event):
    val = event.widget.get()
    if len(val)>1:
        event.widget.delete(1)

def validation_10charecters(event):
    val = event.widget.get()
    if len(val)>9:
        event.widget.delete(9)

def validation_15charecters(event):
    val = event.widget.get()
    if len(val)>14:
        event.widget.delete(14)

def validation_25charecters(event):
    val = event.widget.get()
    if len(val)>24:
        event.widget.delete(24)

def validation_95charecters(event):
    val = event.widget.get(1.0, END)
    if len(val)>94.0:
        event.widget.delete(1.94)

#Tkinter window configs
if "__main__"==__name__:
    root=Tk()
    root.title("Billing App")
    #get your Windows width/height, set size to full window
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    #wont allow to resize window, and full screen when opening
    root.resizable(False,False)
    #root.state('zoomed')

def openeditwindow():
    global editwindow
    editwindow = Toplevel(root)
    editwindow.grab_set()
    editwindow.title("Edit")
    editwindow.geometry('%dx%d+%d+%d' % (332, 140, 800, 400))
    editwindow.resizable(False,False)

menu_frame= Frame(root,bg="#161719",width=250,height=1060)
menu_frame.grid(row=0,column=0)
menu_frame.propagate(0)
style = Style(root)
style.theme_use("clam")
style.configure("Treeview", background=tree_view_color_bg,fieldbackground=tree_view_color_fg, foreground="white")
style.configure("TCombobox",fieldbackground= entry_box_color,foreground= element_color)

def clear_all(treeview_name):
        for item in treeview_name.get_children():
            treeview_name.delete(item)

def selected_item_from_treeview(treeview_name,treeview_name_string):
    curItem = treeview_name.focus()
    treeview_name.item(curItem)
    selected_items =treeview_name.item(curItem)
    if treeview_name_string=='purchase_tree_view' or 'item_tree_view' or 'report_tree_view':
        for key, value in selected_items.items():
            if key == 'values':
                selected_treeview_item=value[0]
                return selected_treeview_item


def menu_frame_obj():
    global login_btn,add_btn,dealer_btn,update_btn,explore_btn
    login_btn=Button(menu_frame,text="Login",width = 25,height=menu_button_height,fg=element_color,bg=menu_button_color,command=lambda:[login_obj()])
    add_btn=Button(menu_frame,text="Todays Budget",width = 25,state='disabled',fg=element_color,height=menu_button_height,bg=menu_button_color,command=lambda:[])
    update_btn=Button(menu_frame,text="Update Budget",width = 25,fg=element_color,state='disabled',height=menu_button_height,bg=menu_button_color,command=lambda:[()])
    explore_btn=Button(menu_frame,text="Budget History",width = 25,fg=element_color,state='disabled',height=menu_button_height,bg=menu_button_color,command=lambda:[])

    def place_menu(click):
        y=0.4+click
        add=0.1
        login_btn.place(relx = 0.475, rely = y, anchor = CENTER)
        y+=add
        add_btn.place(relx = 0.475, rely = y, anchor = CENTER)
        y+=add
        update_btn.place(relx = 0.475, rely = y, anchor = CENTER)
        y+=add
        explore_btn.place(relx = 0.475, rely = y, anchor = CENTER)
    place_menu(-0.1)

def menu_btn_disabled():
    add_btn.config(state='disabled')
    update_btn.config(state='disabled')
    explore_btn.config(state='disabled')

def menu_btn_normal():
    add_btn.config(state='normal')
    update_btn.config(state='normal')
    explore_btn.config(state='normal')

def login_obj():
    global login_frame
    login_frame= Frame(root,width=1670,height=1060,bg=frame_color)
    login_frame.grid(row=0,column=1)
    login_frame.propagate(0)

    username='admin'
    password='admin123'
    #login_obj
    username_lbl=Label(login_frame,text="User Name",font=book_antiqua,bg=frame_color,fg=element_color)
    username_lbl.place(relx = 0.1, rely = 0.2, anchor = NW)
    username_tb=Entry(login_frame,fg=element_color,bg=entry_box_color,font=arial,border=4)
    username_tb.place(relx = 0.2, rely = 0.2, anchor = NW)
    username_tb.bind('<Key>',validation_10charecters)
    #Password
    password_lbl=Label(login_frame,text="Password",font=book_antiqua,bg=frame_color,fg=element_color)
    password_lbl.place(relx = 0.1, rely = 0.24, anchor = NW)
    password_tb=Entry(login_frame,fg=element_color,bg=entry_box_color,font=arial,border=4)
    password_tb.place(relx = 0.2, rely = 0.24, anchor = NW)
    password_tb.bind('<Key>',validation_10charecters)

    #Login
    login_btn=Button(login_frame,fg=element_color,bg=frame_button_color,text="LogIn",width = 20,border=4,command=lambda:[check_password()])
    login_btn.place(relx = 0.1, rely = 0.32, anchor = NW)

    #Logoout
    logout_btn=Button(login_frame,fg=element_color,bg=frame_button_color,state='disabled',text="LogOut",width = 20,border=4,command=lambda:[menu_btn_disabled(),logout_btn.config(state='disabled'),login_btn.config(state='normal')])
    logout_btn.place(relx = 0.205, rely = 0.32, anchor = NW)

    def check_password():
        if(username_tb.get()==username or password_tb.get()==password):
            logout_btn.config(state='normal')
            login_btn.config(state='disabled')
            menu_btn_normal()
        else:
            messagebox.showerror(title='Error', message="Wrong Password")





menu_frame_obj()
root.mainloop()