#All necessary Packages
from tkinter import messagebox, Button, Frame, Label, Toplevel, CENTER, Tk, Entry, NW, END, StringVar
from tkinter.ttk import Style, Treeview
from tkcalendar import DateEntry
import datetime
import sqlite3
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
#date and time, sorting date into dd/mm/yyyy
date=datetime.date.today()
datesorted=date.strftime("%d-%m-%Y")
#Validation
def validation_10charecters(event):
    val = event.widget.get()
    if len(val)>9:
        event.widget.delete(9)
def validation_25charecters(event):
    val = event.widget.get()
    if len(val)>24:
        event.widget.delete(24)
#Tkinter window configs
if "__main__"==__name__:
    root=Tk()
    root.title("Billing App")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.resizable(False,False)
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
def clear_tv(label_name,treeview_name):
    label=label_name
    temp=messagebox.askquestion('Delete Product', 'Are you sure you want to Delete')
    if temp=='yes':
        for item in treeview_name.get_children():
            treeview_name.delete(item)
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            cur.execute("drop table temp_daily_spends")
            cur.execute("CREATE TABLE IF NOT EXISTS temp_daily_spends(date dates NOT NULL,particulars varchar2(25) NOT NULL,income decimal,expense decimal,PRIMARY KEY (date, particulars))")
            con.commit()
            cur.execute("SELECT SUM(income)-SUM(expense) FROM temp_daily_spends")
            total=cur.fetchall()
            if str(total[0][0])=='None':
                label.configure(text="0000.00")
            else:
                label.configure(text="{:.2f}".format(float(total[0][0])))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)
            con.close()
def selected_item_from_treeview(treeview_name):
    curItem = treeview_name.focus()
    treeview_name.item(curItem)
    selected_items =treeview_name.item(curItem)
    for key, value in selected_items.items():
        if key == 'values':
            selected_treeview_item=value[1]
            return selected_treeview_item
        
def selected_item_from_treeview1(treeview_name):
    curItem = treeview_name.focus()
    treeview_name.item(curItem)
    selected_items =treeview_name.item(curItem)
    for key, value in selected_items.items():
        if key == 'values':
            selected_treeview_item=value[0]
            return selected_treeview_item

def total_lbl_update(label1,frame_name):
    label=label1
    try:
        con=sqlite3.connect("my_data.sql")
        cur=con.cursor()
        if frame_name=='todays_budget_frame':
            cur.execute("SELECT SUM(income)-SUM(expense) FROM temp_daily_spends")
            total=cur.fetchall()
        elif frame_name=='update_budget_frame':
            cur.execute("SELECT SUM(income)-SUM(expense) FROM daily_spends")
            total=cur.fetchall()
        if str(total[0][0])=='None':
            label.configure(text="0000.00")
        else:
            label.configure(text="{:.2f}".format(float(total[0][0])))
        con.close()
    except sqlite3.Error as err:
        print("Error - ",err)
        con.close()

    

def menu_frame_obj():
    global login_btn,add_btn,dealer_btn,update_btn,history_btn
    login_btn=Button(menu_frame,text="Login",width = 25,height=menu_button_height,fg=element_color,bg=menu_button_color,command=lambda:[login_obj()])
    add_btn=Button(menu_frame,text="Todays Budget",width = 25,state='disabled',fg=element_color,height=menu_button_height,bg=menu_button_color,command=lambda:[todays_budget()])
    update_btn=Button(menu_frame,text="Update Budget",width = 25,fg=element_color,state='disabled',height=menu_button_height,bg=menu_button_color,command=lambda:[update_budget()])
    history_btn=Button(menu_frame,text="Budget History",width = 25,fg=element_color,state='disabled',height=menu_button_height,bg=menu_button_color,command=lambda:[history()])

    def place_menu(click):
        y=0.4+click
        add=0.1
        login_btn.place(relx = 0.475, rely = y, anchor = CENTER)
        y+=add
        add_btn.place(relx = 0.475, rely = y, anchor = CENTER)
        y+=add
        update_btn.place(relx = 0.475, rely = y, anchor = CENTER)
        y+=add
        history_btn.place(relx = 0.475, rely = y, anchor = CENTER)
    place_menu(-0.1)

def menu_btn_disabled():
    add_btn.config(state='disabled')
    update_btn.config(state='disabled')
    history_btn.config(state='disabled')

def menu_btn_normal():
    add_btn.config(state='normal')
    update_btn.config(state='normal')
    history_btn.config(state='normal')

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
        if(username_tb.get()==username and password_tb.get()==password):
            logout_btn.config(state='normal')
            login_btn.config(state='disabled')
            menu_btn_normal()
        else:
            messagebox.showerror(title='Error', message="Wrong Password")

def todays_budget():
    global todays_budget_frame,todays_total_lbl
    todays_budget_frame= Frame(root,width=1670,height=1060,bg=frame_color)
    todays_budget_frame.grid(row=0,column=1)
    todays_budget_frame.propagate(0)

    todays_budget_lbl=Label(todays_budget_frame,text="Add Records",font=book_antiqua_size18,bg=frame_color,fg=element_color)
    todays_budget_lbl.place(relx = 0.4, rely = 0.008, anchor = NW)

    #Objects
    today = date.today()
    date_tb = DateEntry(todays_budget_frame, width= 16,height=0, background= "grey", foreground= "white",bd=4, maxdate=today)
    date_tb.place(relx = 0.03, rely = 0.202, anchor = NW)

    def lower_case2(event):
        particulars.set(particulars.get().lower())
    particulars= StringVar()
    particulars_tb=Entry(todays_budget_frame,fg=element_color,bg=entry_box_color,font=arial,border=4,width=22,textvariable=particulars)
    particulars_tb.place(relx = 0.10, rely = 0.198, anchor = NW)
    particulars_tb.bind('<Key>',validation_25charecters)
    particulars_tb.bind('<KeyRelease>',lower_case2)

    def insert0(event):
        income_tb.delete(0,END)
        income_tb.insert(0,0)
    def insert1(event):
        expense_tb.delete(0,END)
        expense_tb.insert(0,0)

    income_tb=Entry(todays_budget_frame,fg=element_color,bg=entry_box_color,font=arial,border=4,width=10,state='normal')
    income_tb.insert(0,0)
    income_tb.place(relx = 0.222, rely = 0.198, anchor = NW)
    income_tb.bind('<FocusOut>', insert0)

    expense_tb=Entry(todays_budget_frame,fg=element_color,bg=entry_box_color,font=arial,border=4,width=10,state='normal')
    expense_tb.insert(0,0)
    expense_tb.place(relx = 0.28, rely = 0.198, anchor = NW)
    expense_tb.bind('<FocusOut>', insert1)

    #Purchase Add Button
    add_btn=Button(todays_budget_frame,fg=element_color,bg=frame_button_color,text="Add",width = 21,border=4,command=lambda:[add_data()])
    add_btn.place(relx = 0.34, rely = 0.198, anchor = NW)

    #Purchase Delete Button
    todays_delete_btn=Button(todays_budget_frame,fg=element_color,bg=frame_button_color,text="Delete",width = 21,border=4,command=lambda:[delete_todays_item()])
    todays_delete_btn.place(relx = 0.03, rely = 0.575, anchor = NW)

    #clear all button
    todays_clearall_btn=Button(todays_budget_frame,fg=element_color,bg=frame_button_color,text="clear All",width = 21,border=4,command=lambda:[clear_tv(todays_total_lbl,todays_tree_view)])
    todays_clearall_btn.place(relx = 0.13, rely = 0.575, anchor = NW)

    todays_save_btn=Button(todays_budget_frame,fg=element_color,bg=frame_button_color,text="Save",width = 16,height=2,border=4,command=lambda:[save_my_data_to_database()])
    todays_save_btn.place(relx = 0.34, rely = 0.532, anchor = NW)
    
    #Purchase Total
    todays_total_lbl0=Label(todays_budget_frame,text="Bal: ",font=book_antiqua_size18,bg=frame_color,fg=element_color)
    todays_total_lbl0.place(relx = 0.26, rely = 0.574, anchor = NW)
    todays_total_lbl=Label(todays_budget_frame,text="0000.00",font=book_antiqua_size18,bg=frame_color,fg=element_color)
    todays_total_lbl.place(relx = 0.3, rely = 0.574, anchor = NW)


    def add_data():
        todays_date=date_tb.get_date().strftime("%d-%m-%Y")
        income=float(income_tb.get())
        expense=float(expense_tb.get())
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS temp_daily_spends(date dates NOT NULL,particulars varchar2(25) NOT NULL,income decimal,expense decimal,PRIMARY KEY (date, particulars))")
            cur.execute("INSERT INTO temp_daily_spends(date,particulars,income,expense) VALUES (?, ?, ?, ?) ON CONFLICT(particulars, date) DO UPDATE SET income=income+?, expense=expense+?", (todays_date, particulars_tb.get(), float(income), float(expense), float(income), float(expense)))
            con.commit()
            cur.execute("SELECT date,particulars,income,expense from temp_daily_spends ORDER BY expense ASC")
            row=cur.fetchall()
            clear_all(todays_tree_view)
            con.commit()
            for i in row:
                todays_tree_view.insert("", 'end', text ="L1",values =(i[0],i[1],i[2],i[3]))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)
            con.close()
        total_lbl_update(todays_total_lbl,'todays_budget_frame')


    def delete_todays_item():
        selected_treeview_item=selected_item_from_treeview(todays_tree_view)
        temp=messagebox.askquestion('Delete Product', 'Are you sure you want to Delete')
        if temp=='yes':
            try:
                con=sqlite3.connect("my_data.sql")
                cur=con.cursor()
                cur.execute("DELETE FROM temp_daily_spends where particulars='{}'".format(str(selected_treeview_item)))
                con.commit()
                cur.execute("SELECT * FROM temp_daily_spends ORDER BY expense ASC")
                row=cur.fetchall()
                clear_all(todays_tree_view)
                for i in row:
                    todays_tree_view.insert("", 'end', text ="L1",values =(i[0],i[1],i[2],i[3]))
                con.commit()
                total_lbl_update(todays_total_lbl,'todays_budget_frame')
                con.close()
            except sqlite3.Error as err:
                print("Error - ",err)

    def save_my_data_to_database():
            try:
                con=sqlite3.connect("my_data.sql")
                cur=con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS daily_spends(date dates NOT NULL,particulars varchar2(25) NOT NULL,income decimal,expense decimal,total decimal,PRIMARY KEY (date, particulars))")
                #cur.execute("CREATE TABLE IF NOT EXISTS item_purchase_details(item_id int(10) PRIMARY KEY NOT NULL,date date NOT NULL,item_name varchar(25) NOT NULL,purchase_quantity REAL NOT NULL,buying_price REAL NOT NULL,total_price REAL NOT NULL,selling_price REAL,item_category varchar(15))")
                cur.execute("SELECT * from temp_daily_spends")
                row=cur.fetchall()
                for i in row:
                    cur.execute("INSERT OR REPLACE INTO daily_spends (date, particulars, income, expense, total)VALUES (?, ?, ?, ?, (SELECT COALESCE(SUM(income), 0) - COALESCE(SUM(expense), 0) FROM daily_spends WHERE particulars = ?))", (i[0], i[1], i[2], i[3], i[1]))
                cur.execute("UPDATE daily_spends SET total=(SELECT SUM(income)-SUM(expense) FROM daily_spends WHERE date=?) WHERE date=?", (row[0][0], row[0][0]))
                messagebox.showinfo(title='Saved', message="Products Added to inventory")
                con.commit()
                con.close()
                clear_tv(todays_total_lbl,todays_tree_view)
            except sqlite3.Error as err:
                print("Error - ",err)
                messagebox.showerror(title='Error', message="Data not Save")
                con.close()

    #treeview element
    todays_tree_view= Treeview(todays_budget_frame,selectmode='browse',height=17)
    todays_tree_view.place(relx = 0.03, rely = 0.225, anchor = NW)

    #verticle scrollbar
    #vertical_scrollbar=Scrollbar(billing_frame,orient="vertical",command=tree_view.yview)
    #vertical_scrollbar.place(relx = 0.03, rely = 0.3, anchor = NW)
    #tree_view.configure(xscrollcommand=vertical_scrollbar.set)

    #Definning number of columns
    todays_tree_view["columns"]=("1","2","3","4")

    #defining heading
    todays_tree_view["show"]='headings'

    #modifying the size of the columns
    todays_tree_view.column("1",width=118)
    todays_tree_view.column("2",width=200)
    todays_tree_view.column("3",width=100)
    todays_tree_view.column("4",width=98)

    #assigning heading name
    todays_tree_view.heading("1",text="Date")
    todays_tree_view.heading("2",text="Particulars")
    todays_tree_view.heading("3",text="Income")
    todays_tree_view.heading("4",text="Expense")

    con=sqlite3.connect("my_data.sql")
    cur=con.cursor()
    cur.execute("drop table IF EXISTS temp_daily_spends")
    cur.execute("CREATE TABLE IF NOT EXISTS temp_daily_spends(date dates NOT NULL,particulars varchar2(25) NOT NULL,income decimal,expense decimal,PRIMARY KEY (date, particulars))")
    con.commit()
    con.close()

def update_budget():
    global update_budget_frame,update_total_lbl
    update_budget_frame= Frame(root,width=1670,height=1060,bg=frame_color)
    update_budget_frame.grid(row=0,column=1)
    update_budget_frame.propagate(0)

    update_budget_lbl=Label(update_budget_frame,text="Update Budget",font=book_antiqua_size18,bg=frame_color,fg=element_color)
    update_budget_lbl.place(relx = 0.4, rely = 0.008, anchor = NW)

    #Objects
    today = date.today()
    dateentry = DateEntry(update_budget_frame, width= 16,height=0, background= "grey", foreground= "white",bd=4, maxdate=today,date_pattern='dd-MM-yyyy')
    dateentry.place(relx = 0.03, rely = 0.202, anchor = NW)
    dateentry.place_forget()

    def lower_case2(event):
        particulars.set(particulars.get().lower())
    particulars= StringVar()
    particulars_tb=Entry(update_budget_frame,fg=element_color,bg=entry_box_color,font=arial,border=4,width=28,textvariable=particulars)
    particulars_tb.bind('<Key>',validation_25charecters)
    particulars_tb.bind('<KeyRelease>',lower_case2)

    def insert0(event):
        income_tb.delete(0,END)
        income_tb.insert(0,0)
    def insert1(event):
        expense_tb.delete(0,END)
        expense_tb.insert(0,0)


    income_tb=Entry(update_budget_frame,fg=element_color,bg=entry_box_color,font=arial,border=4,width=10,state='normal')
    income_tb.insert(0,0)
    income_tb.bind('<FocusOut>', insert0)

    expense_tb=Entry(update_budget_frame,fg=element_color,bg=entry_box_color,font=arial,border=4,width=10,state='normal')
    expense_tb.insert(0,0)
    expense_tb.bind('<FocusOut>', insert1)
    #from date
    report_date_lbl=Label(update_budget_frame,text="From",font=book_antiqua,bg=frame_color,fg=element_color)
    report_date_lbl.place(relx = 0.04, rely = 0.09, anchor = NW)
    
    today = date.today()
    report_from_date_tb = DateEntry(update_budget_frame, width= 16,height=0, background= "grey", foreground= "white",bd=4, maxdate=today)
    report_from_date_tb.place(relx = 0.07, rely = 0.09, anchor = NW)

    #to date
    report_date_lbl=Label(update_budget_frame,text="To",font=book_antiqua,bg=frame_color,fg=element_color)
    report_date_lbl.place(relx = 0.16, rely = 0.09, anchor = NW)
    
    report_to_date_tb = DateEntry(update_budget_frame, width= 16,height=0, background= "grey", foreground= "white",bd=4, maxdate=today)
    report_to_date_tb.place(relx = 0.177, rely = 0.09, anchor = NW)

    search_lbl=Label(update_budget_frame,text="Search: ",font=book_antiqua,bg=frame_color,fg=element_color)
    search_lbl.place(relx = 0.04, rely = 0.125, anchor = NW)

    search_tb=Entry(update_budget_frame,fg=element_color,bg=entry_box_color,font=arial,border=4,width=25,state='normal')
    search_tb.place(relx = 0.08, rely = 0.125, anchor = NW)

    #Search btn
    report_filter_btn=Button(update_budget_frame,fg=element_color,bg=frame_button_color,text="Filter",width = 16,border=4,command=lambda:[date_filter()])
    report_filter_btn.place(relx = 0.27, rely = 0.09, anchor = NW)

    #Purchase Add Button
    update_focus_bool=0
    add_btn=Button(update_budget_frame,fg=element_color,bg=frame_button_color,text="Update",width = 21,border=4,command=lambda:[add_data(),update_tree_view.configure(selectmode='extended'),search_tb.config(state='normal'),report_to_date_tb.config(state='normal'),report_from_date_tb.config(state='normal'),report_filter_btn.config(state='normal')])

    #Purchase Delete Button
    update_delete_btn=Button(update_budget_frame,fg=element_color,bg=frame_button_color,text="Delete",width = 21,border=4,command=lambda:[delete_update_item()])
    update_delete_btn.place(relx = 0.03, rely = 0.575, anchor = NW)

    #clear all button
    update_clearall_btn=Button(update_budget_frame,fg=element_color,bg=frame_button_color,text="Edit",width = 21,border=4,command=lambda:[edit_budget_info(),search_tb.config(state='disabled'),report_to_date_tb.config(state='disabled'),report_from_date_tb.config(state='disabled'),report_filter_btn.config(state='disabled')])
    update_clearall_btn.place(relx = 0.13, rely = 0.575, anchor = NW)
    
    #Purchase Total
    update_total_lbl0=Label(update_budget_frame,text="Bal: ",font=book_antiqua_size18,bg=frame_color,fg=element_color)
    update_total_lbl0.place(relx = 0.26, rely = 0.574, anchor = NW)
    update_total_lbl=Label(update_budget_frame,text="0000.00",font=book_antiqua_size18,bg=frame_color,fg=element_color)
    update_total_lbl.place(relx = 0.3, rely = 0.574, anchor = NW)

    #Date bug########################
    def date_filter():
        clear_all(update_tree_view)
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            from_date=report_from_date_tb.get_date().strftime("%d-%m-%Y")
            print(from_date)
            to_date=report_to_date_tb.get_date().strftime("%d-%m-%Y")
            print(to_date)
            cur.execute("SELECT * FROM daily_spends WHERE date BETWEEN ? AND ? ORDER BY date",(from_date,to_date))
            report=cur.fetchall()
            for i in report:
                update_tree_view.insert("", 'end', text ="L1",values =(i[0],i[1],i[2],i[3]))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)

    def add_data():
        todays_date=dateentry.get_date().strftime("%d-%m-%Y")
        print(dateentry)
        particulars=particulars_tb.get()
        income=float(income_tb.get())
        expense=float(expense_tb.get())
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS daily_spends(date dates NOT NULL,particulars varchar2(25) NOT NULL,income decimal,expense decimal,total decimal,PRIMARY KEY (date, particulars))")
            cur.execute("UPDATE daily_spends SET particulars=?, income=?, expense=? WHERE date=? AND particulars=?", (particulars, float(income), float(expense), todays_date,particulars))
            cur.execute("SELECT * from daily_spends")
            row1=cur.fetchall()
            cur.execute("UPDATE daily_spends SET total=(SELECT SUM(income)-SUM(expense) FROM daily_spends WHERE date=?) WHERE date=?", (row1[0][0], row1[0][0]))
            con.commit()
            cur.execute("SELECT date,particulars,income,expense from daily_spends ORDER BY expense ASC")
            row=cur.fetchall()
            clear_all(update_tree_view)
            con.commit()
            for i in row:
                update_tree_view.insert("", 'end', text ="L1",values =(i[0],i[1],i[2],i[3]))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)
            con.close()
        total_lbl_update(update_total_lbl,'update_budget_frame')
        destroy_update_element()

    def delete_update_item():
        selected_treeview_item=selected_item_from_treeview1(update_tree_view)
        selected_treeview_item1=selected_item_from_treeview(update_tree_view)
        print(selected_treeview_item," ",selected_treeview_item1)
        temp=messagebox.askquestion('Delete Product', 'Are you sure you want to Delete')
        if temp=='yes':
            try:
                con=sqlite3.connect("my_data.sql")
                cur=con.cursor()
                cur.execute("DELETE FROM daily_spends where particulars=? AND date=?",(selected_treeview_item1,selected_treeview_item))
                con.commit()
                cur.execute("SELECT * from daily_spends")
                row1=cur.fetchall()
                if len(row1)==0:
                    print()
                elif len(row1)>0:
                    cur.execute("UPDATE daily_spends SET total=(SELECT SUM(income)-SUM(expense) FROM daily_spends WHERE date=?) WHERE date=?", (row1[0][0], row1[0][0]))
                con.commit()
                cur.execute("SELECT * FROM daily_spends ORDER BY expense ASC")
                row=cur.fetchall()
                clear_all(update_tree_view)
                for i in row:
                    update_tree_view.insert("", 'end', text ="L1",values =(i[0],i[1],i[2],i[3]))
                con.commit()
                total_lbl_update(update_total_lbl,'update_budget_frame')
                con.close()
            except sqlite3.Error as err:
                print("Error - ",err)

    #treeview element
    update_tree_view= Treeview(update_budget_frame,selectmode='browse',height=17)
    update_tree_view.place(relx = 0.03, rely = 0.225, anchor = NW)

    #verticle scrollbar
    #vertical_scrollbar=Scrollbar(billing_frame,orient="vertical",command=tree_view.yview)
    #vertical_scrollbar.place(relx = 0.03, rely = 0.3, anchor = NW)
    #tree_view.configure(xscrollcommand=vertical_scrollbar.set)

    #Definning number of columns
    update_tree_view["columns"]=("1","2","3","4")

    #defining heading
    update_tree_view["show"]='headings'

    #modifying the size of the columns
    update_tree_view.column("1",width=118)
    update_tree_view.column("2",width=200)
    update_tree_view.column("3",width=100)
    update_tree_view.column("4",width=100)

    #assigning heading name
    update_tree_view.heading("1",text="Date")
    update_tree_view.heading("2",text="Particulars")
    update_tree_view.heading("3",text="Income")
    update_tree_view.heading("4",text="Expense")
    total_lbl_update(update_total_lbl,'update_budget_frame')

    item={}     #####################################################################PUT THIS IN VIEW FRAME
    def Scankey2(event):
        #val stores the selected value
        val = event.widget.get()
        if len(val)==1 or len(val)==0:
            clear_all(update_tree_view)
            item_info()
        else:
            name_data = {}
            for key,value in item.items():
                if val.lower() in key.lower():
                    name_data[key]=value
                    Update2(name_data)

    def Update2(data):
        for item in update_tree_view.get_children():
            update_tree_view.delete(item)
        for key, value in data.items():
            update_tree_view.insert("",'end',text="L1",values=(value[0],value[1],value[2],value[3]))

    def item_info():
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            cur.execute("SELECT * from daily_spends ORDER BY date ASC")
            row=cur.fetchall()
            for i in row:
                item[i[1]]=[i[0],i[1],i[2],i[3]]
                update_tree_view.insert("", 'end', text ="L1", values=(i[0],i[1],i[2],i[3]))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)
    item_info()
    search_tb.bind('<Key>', Scankey2)
    
    def edit_budget_info():
        global parti
        curItem = update_tree_view.focus()
        update_tree_view.item(curItem)
        selected_items =update_tree_view.item(curItem)
        for key, value in selected_items.items():
            if key == 'values':
                date=value[0]
                particulars=value[1]
                income=value[2]
                expense=value[3]
                parti=value[1]
        update_tree_view.configure(selectmode='none')

        dateentry.place(relx = 0.03, rely = 0.202, anchor = NW)
        particulars_tb.place(relx = 0.10, rely = 0.198, anchor = NW)
        income_tb.place(relx = 0.222, rely = 0.198, anchor = NW)
        expense_tb.place(relx = 0.28, rely = 0.198, anchor = NW)
        add_btn.place(relx = 0.34, rely = 0.198, anchor = NW)

        dateentry.delete(0,END)
        particulars_tb.delete(0,END)
        income_tb.delete(0,END)
        expense_tb.delete(0,END)

        dateentry.insert(0,date)
        particulars_tb.insert(0,particulars)
        income_tb.insert(0,income)
        expense_tb.insert(0,expense)

    def destroy_update_element():
        dateentry.place_forget()
        particulars_tb.place_forget()
        income_tb.place_forget()
        expense_tb.place_forget()
        add_btn.place_forget()

def history():
    global history_budget_frame,history_total_lbl,history_tree_view,search_lbl,search_tb,history_totalincome_lbl0,history_totalexp_lbl0,history_total_lbl0,get_total

    def get_total(column):
        total = 0
        for item in history_tree_view.get_children():
            value = int(history_tree_view.item(item, "values")[column])
            total += value
        return total

    history_budget_frame= Frame(root,width=1670,height=1060,bg=frame_color)
    history_budget_frame.grid(row=0,column=1)
    history_budget_frame.propagate(0)

    history_budget_lbl=Label(history_budget_frame,text="Budget History",font=book_antiqua_size18,bg=frame_color,fg=element_color)
    history_budget_lbl.place(relx = 0.4, rely = 0.008, anchor = NW)
    
    #Purchase Total
    history_totalincome_lbl0=Label(history_budget_frame,text=" ",font=book_antiqua,bg=frame_color,fg='green')
    history_totalincome_lbl0.place(relx = 0.115, rely = 0.574, anchor = NW)

    history_totalexp_lbl0=Label(history_budget_frame,text=" ",font=book_antiqua,bg=frame_color,fg='red')
    history_totalexp_lbl0.place(relx = 0.196, rely = 0.574, anchor = NW)

    history_total_lbl0=Label(history_budget_frame,text="Bal: ",font=book_antiqua,bg=frame_color,fg=element_color)
    history_total_lbl0.place(relx = 0.29, rely = 0.574, anchor = NW)
    

    #from date
    report_date_lbl=Label(history_budget_frame,text="From",font=book_antiqua,bg=frame_color,fg=element_color)
    report_date_lbl.place(relx = 0.04, rely = 0.15, anchor = NW)
    
    today = date.today()
    report_from_date_tb = DateEntry(history_budget_frame, width= 16,height=0, background= "grey", foreground= "white",bd=4, maxdate=today)
    report_from_date_tb.place(relx = 0.07, rely = 0.15, anchor = NW)

    #to date
    report_date_lbl=Label(history_budget_frame,text="To",font=book_antiqua,bg=frame_color,fg=element_color)
    report_date_lbl.place(relx = 0.16, rely = 0.15, anchor = NW)
    
    report_to_date_tb = DateEntry(history_budget_frame, width= 16,height=0, background= "grey", foreground= "white",bd=4, maxdate=today)
    report_to_date_tb.place(relx = 0.177, rely = 0.15, anchor = NW)

    #Search btn
    report_filter_btn=Button(history_budget_frame,fg=element_color,bg=frame_button_color,text="Filter",width = 14,border=4,command=lambda:[date_filter()])
    report_filter_btn.place(relx = 0.255, rely = 0.15, anchor = NW)

    #Date bug########################
    def date_filter():
        clear_all(history_tree_view)
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            from_date=report_from_date_tb.get_date().strftime("%d-%m-%Y")
            print(from_date)
            to_date=report_to_date_tb.get_date().strftime("%d-%m-%Y")
            print(to_date)
            cur.execute("SELECT date, SUM(income), SUM(expense), total FROM daily_spends WHERE date BETWEEN ? AND ? GROUP BY date ORDER BY date ASC",(from_date,to_date))
            report=cur.fetchall()
            for i in report:
                history_tree_view.insert("", 'end', text ="L1",values =(i[0],i[1],i[2],i[3]))
            history_totalincome_lbl0.configure(text="{:.2f}".format(get_total(2)))
            history_totalexp_lbl0.configure(text="{:.2f}".format(get_total(3)))
            history_total_lbl0.configure(text="{:.2f}".format(get_total(4)))
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)

    #treeview element
    history_tree_view= Treeview(history_budget_frame,selectmode='browse',height=17)
    history_tree_view.place(relx = 0.03, rely = 0.225, anchor = NW)

    #verticle scrollbar
    #vertical_scrollbar=Scrollbar(billing_frame,orient="vertical",command=tree_view.yview)
    #vertical_scrollbar.place(relx = 0.03, rely = 0.3, anchor = NW)
    #tree_view.configure(xscrollcommand=vertical_scrollbar.set)

    #Definning number of columns
    history_tree_view["columns"]=("1","2","3","4","5")

    #defining heading
    history_tree_view["show"]='headings'

    #modifying the size of the columns
    history_tree_view.column("1",width=118)
    history_tree_view.column("2",width=200)
    history_tree_view.column("3",width=160)
    history_tree_view.column("4",width=160)
    history_tree_view.column("5",width=160)

    #assigning heading name
    history_tree_view.heading("1",text="Date")
    history_tree_view.heading("2",text="Particulars")
    history_tree_view.heading("3",text="Income")
    history_tree_view.heading("4",text="Expense")
    history_tree_view.heading("5",text="Days Balance")
    history_tree_view.column("#2",width=0, stretch=False)

    def item_info():
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            cur.execute("SELECT date,particulars,SUM(income), SUM(expense), total FROM daily_spends GROUP BY date ORDER BY date ASC")
            row=cur.fetchall()
            for i in row:
                history_tree_view.insert("", 'end', text ="L1", values=(i[0],i[1],i[2],i[3],i[4]))
            history_totalincome_lbl0.configure(text="{:.2f}".format(get_total(2)))
            history_totalexp_lbl0.configure(text="{:.2f}".format(get_total(3)))
            history_total_lbl0.configure(text="{:.2f}".format(get_total(4)))
            
            con.close()
        except sqlite3.Error as err:
            print("Error - ",err)
    item_info()

    expand_btn=Button(history_budget_frame,fg=element_color,bg=frame_button_color,text="Expand",width = 14,border=4,command=lambda:[expand(),report_from_date_tb.config(state='disabled'),report_to_date_tb.config(state='disabled'),report_filter_btn.config(state='disabled')])
    expand_btn.place(relx = 0.3245, rely = 0.197, anchor = NW)

    #clear all button
    goback_btn=Button(history_budget_frame,fg=element_color,bg=frame_button_color,text="Go Back",width = 14,border=4,command=lambda:[goback()])
    goback_btn.place(relx = 0.0287, rely = 0.197, anchor = NW)

def expand():
    curItem = history_tree_view.focus()
    history_tree_view.item(curItem)
    selected_items =history_tree_view.item(curItem)
    for key, value in selected_items.items():
        if key == 'values':
            date1=value[0]
    history_tree_view.configure(selectmode='none')
    
    history_totalincome_lbl0.place(relx = 0.195, rely = 0.574, anchor = NW)
    history_totalexp_lbl0.place(relx = 0.262, rely = 0.574, anchor = NW)
    history_total_lbl0.place(relx = 0.325, rely = 0.574, anchor = NW)


    if history_budget_frame.focus_get() == history_tree_view:
        history_tree_view.column("2",width=200)
        clear_all(history_tree_view)
        try:
            con=sqlite3.connect("my_data.sql")
            cur=con.cursor()
            cur.execute("SELECT date,particulars,income,expense from daily_spends where date=?",(date1,))
            row=cur.fetchall()
            for i in row:
                history_tree_view.insert("", 'end', text ="L1", values=(i[0],i[1],i[2],i[3]))
            history_totalincome_lbl0.configure(text="{:.2f}".format(get_total(2)))
            history_totalexp_lbl0.configure(text="{:.2f}".format(get_total(3)))
            history_total_lbl0.configure(text="{:.2f}".format(get_total(2)-get_total(3)))
            con.close()
        except sqlite3.Error as err:
                print("Error - ",err)



def goback():
    history_tree_view.destroy()
    history()
    

menu_frame_obj()
root.mainloop()