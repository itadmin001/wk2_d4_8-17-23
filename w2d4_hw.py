from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename


list = {}
categories = ['Drink','Meat','Snacks','Dairy','Seafood','Produce','Poultry']
escape = False
item_count = 0

class Cart():
    
    def __init__(self):
        self.item = str
        self.categories = []
        self.list = {}
        self.quantity = int
        self.item_price = int
        self.take_input()

    ##################  File and Edit Operations  ##################
    

    def new_file(self,text_area,win):

        text = text_area.get(1.0,"end-1c")
        if text != '':
            self.save_current()
        else:
            start_new()
            text_area.delete(1.0, END)
            global current_file
            current_file = None
            win.title(f'Shopping List New File')


    def save_file(self,text_area,win):

        global current_file
        filepath=asksaveasfilename(filetypes=[('Text Files','*.txt'),('All Files','*.*')])
        if not filepath:
            return
        with open(filepath, 'w') as output_file:
            text = text_area.get(1.0,END)
            output_file.write(text)
        win.title(f'Shopping List {filepath}')
        current_file = filepath



    def open_file(self,text_area,win):
            text_area.delete(1.0, END)
            global current_file
            filepath=askopenfilename(filetypes=[('Text Files','*.txt'),('All Files','*.*')])
            if not filepath:
                return
            with open(filepath, 'r') as input_file:
                text=input_file.read()
                text_area.insert(END, text)
            win.title(f"Shopping List - {filepath}")
            current_file = filepath


    def save_current(self):
        save_current = Toplevel()
        save_current.title("Save File")

        sav_frame=Frame(save_current)
        sav_frame.pack()
        sav_frame.columnconfigure(1,weight=1)
        sav_frame.rowconfigure(4,weight=1)

        tl_btn_grp_frame = Frame(sav_frame)
        tl_btn_grp_frame.grid(row=3,column=0,padx=10,pady=10)
        tl_btn_grp_frame.columnconfigure(2, weight=1)
        tl_btn_grp_frame.rowconfigure(1,weight=1)

        notice_label = Label(sav_frame,text="Do you want to save the current list?",font=('arial','11','bold'))
        notice_label.grid(row=0,column=0,padx=5,pady=5,sticky=EW)

        sav_btn = Button(tl_btn_grp_frame,text="Save",command=lambda:self.save_file(win_display_area,win),width=15,padx=5,pady=5)
        sav_btn.grid(row=0,column=0)

        cont_btn = Button(tl_btn_grp_frame,text="Continue without saving",command=lambda:self.new_file(win_display_area,win),padx=5,pady=5)
        cont_btn.grid(row=0,column=1)


    def delete_items(self,win_frame_right):

        edit_win = Toplevel(win)
        edit_win.title("Edit List")

        edit_win_frame = Frame(edit_win)
        edit_win_frame.grid(row=0,column=0,padx=5,pady=5)

        j=len(list)+1
        edit_win_frame.columnconfigure(0,weight=1)
        edit_win_frame.columnconfigure(1,weight=1,)
        edit_win_frame.rowconfigure(j, weight=1)

        label_frame = Frame(edit_win_frame,padx=5,pady=5)
        label_frame.grid(row=0,column=0)
        del_label = Label(label_frame,text="Delete From List")
        del_label.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky=N)
        
        dyn_label_text = []

        for k,v in self.list.items():
            text = ''
            text+= f"{v['item']}"
            dyn_label_text.append(f'{k}')
            dyn_label_text.append(text)

        ######### initialize the checkbox variables and pass them to exec globals()
        for c in range(1,len(dyn_label_text)+1):
            chk_btn_src =f'chk_state{c}'
            exec(chk_btn_src,globals().update({f'chk_state{c}':BooleanVar()}))

        ##  appending Key and Item to the list used here - used in conjuction with delete
        ##  i % 2 -> display only the Item
        row_count = 0
        for i in range(1,len(dyn_label_text)):
            row_count+=1 ### <- row_count used to place the Delete button at
                        ###  the bottom of the Edit Items window
            if i % 2 != 0: 
                exec(f'edit_item_cb{i} = Checkbutton(edit_win,justify="left",variable=chk_state{i})')
                exec(f"edit_item_cb{i}.grid(row=i,column=0,padx=5,pady=5,sticky=SW)")
            
                exec(f"edit_item_label{i} = Label(edit_win,text=dyn_label_text[{i}],justify='left')")
                exec(f"edit_item_label{i}.grid(row=i,column=1,padx=5,pady=5,sticky=SW)")

        def commit_delete():
            for i in range(1,len(dyn_label_text)):
                exec(f'this = chk_state{i}.get()',globals())
                if this == True:
                        this_key = dyn_label_text[i-1]
                        self.list.pop(this_key)
            self.show_list(win_display_area)
            edit_win.destroy()

        conf_del_btn = Button(edit_win,text="Delete",command=commit_delete,justify='center')
        conf_del_btn.grid(row=row_count+1,column=1,sticky=EW,padx=5,pady=5)

    def edit_categories(self):

        edit_cat_win = Toplevel(win)
        edit_cat_win.title("Edit Categories")

        edit_cat_win_frame = Frame(edit_cat_win)
        edit_cat_win_frame.grid(row=0,column=0,padx=5,pady=5)

        j=len(list)+1
        edit_cat_win_frame.columnconfigure(0,weight=1)
        #edit_cat_win_frame.columnconfigure(1,weight=0)
        edit_cat_win_frame.rowconfigure(j, weight=0)

        label_frame = Frame(edit_cat_win_frame,padx=5,pady=5)
        label_frame.grid(row=0,column=0)
        del_label = Label(label_frame,text="Edit Categories\nSelect to delete or enter new category")
        del_label.grid(row=0,column=0,columnspan=2,padx=10,pady=10,sticky=N)

        category_text = []

        for category in categories:
            text = ''
            text+= category
            category_text.append(text)
            print(category_text)
        ######### initialize the checkbox variables and pass them to exec globals()
        for c in range(1,len(category_text)+1):
            chk_btn_src =f'cat_chk_state{c}'
            exec(chk_btn_src,globals().update({f'cat_chk_state{c}':BooleanVar()}))

        ##  appending Key and Item to the list used here - used in conjuction with delete
        ##  i % 2 -> display only the Item
        row_count = 0
        for i in range(1,len(category_text)):
            row_count+=1 ### <- row_count used to place the Delete button at
                        ###  the bottom of the Edit Items window
            exec(f'edit_cat_cb{i} = Checkbutton(edit_cat_win_frame,justify="left",width=1,variable=cat_chk_state{i})')
            exec(f"edit_cat_cb{i}.grid(row=i,column=0,padx=5,pady=5,sticky='w')")
        
            exec(f"edit_cat_label{i} = Label(edit_cat_win_frame,text=category_text[{i}],justify='left')")
            exec(f"edit_cat_label{i}.grid(row=i,column=1,padx=5,pady=5,sticky='w')")

        def commit_edit_cat():
            new_cat = add_category.get()
            if new_cat !='':
                categories.append(new_cat)
            for i in range(1,len(category_text)):
                exec(f'this = cat_chk_state{i}.get()',globals())
                if this == True:
                    this_key = category_text[i]
                    categories.remove(this_key)
            close_window()
        
        def close_window():
            edit_cat_win.destroy()

        add_category_label = Label(edit_cat_win_frame,text="Enter New Category: ")
        add_category_label.grid(row=row_count+2,column=0)
        
        add_category = Entry(edit_cat_win_frame)
        add_category.grid(row=row_count+2,column=1,sticky=EW,padx=5,pady=5)
        
        cat_edit_btn = Button(edit_cat_win_frame,text="Submit",command=commit_edit_cat,justify='center')
        cat_edit_btn.grid(row=row_count+1,column=1,sticky=EW,padx=5,pady=5)

        cat_done_btn = Button(edit_cat_win_frame,text="Done/Cancel",width=15,command=close_window)
        cat_done_btn.grid(row=row_count+1,column=0,padx=5,pady=5)

            
    def show_details(self,text_area):
        text_area.delete(1.0, END)
        text=''
        for k,v in list.items():
            text+=f"Item: {v['item']}\n"
            text+=f"Quantity: {v['quantity']}\n"
            text+=f"Price: {v['price']}\n"
            text+=f"Category: {v['category']}\n\n"
        win_display_area.insert(1.0,text)

    def show_list(self,text_area):
        text_area.delete(1.0, END)
        text=''
        for k,v in self.list.items():
            text+=f"{v['item']}\n"
        win_display_area.insert(1.0,text)


    def list_update(self):
        global item_count
        if item_input.get() !='':
            item_count+=1
            self.item = item_input.get()
            self.category = clicked.get()
            self.price = price_input.get()
            self.quantity = quant_input.get()
            self.list.update({"item"+str(item_count):{
                    'item':self.item,
                    'quantity':self.quantity,
                    'price':self.price,
                    'category':self.category
                }})
        self.delete_items
        item_input.delete(0,END)
        price_input.delete(0,END)
        quant_input.delete(0,END)
        quant_input.insert(0,"1")
        item_input.focus_set()
        self.show_list(win_display_area)

    def take_input(self):
        global win
        global current_file
        global item_input
        global price_input
        global quant_input
        global win_display_area
        global start_new
        global clicked
        

    ######################  Start Main Tk Window  ####################################

        win = Tk()
        win.title("Shopping List")
        
        win.columnconfigure(0,weight=0)
        win.columnconfigure(1,weight=1)
        win.rowconfigure(0,weight=1)

        win_frame_left = Frame(win,relief=RAISED,bd=2)
        win_frame_left.grid(row=0,column=0,padx=10,pady=10,sticky=NW)

        win_frame_right = Frame(win,background="#fff")
        win_frame_right.grid(row=0,column=1,padx=10,pady=10,sticky=NSEW)

        win_display_area = Text(win_frame_right)
        win_display_area.grid(row=0,column=1,padx=10,pady=10,sticky=NSEW)

        item_input_label = Label(win_frame_left,text="Item:")
        item_input_label.grid(row=0,column=0)
        item_input = Entry(win_frame_left)
        item_input.grid(row=0,column=1)

        quant_input_label =Label(win_frame_left,text="Quantity")
        quant_input_label.grid(row=1,column=0)
        quant_input = Spinbox(win_frame_left,from_=1,to=10)
        quant_input.grid(row=1,column=1,sticky=EW)

        price_input_label =Label(win_frame_left,text="Price")
        price_input_label.grid(row=2,column=0)
        price_input = Entry(win_frame_left)
        price_input.insert(0,"$")
        price_input.grid(row=2,column=1,sticky=EW)

        clicked=StringVar()
        clicked.set(categories[0])

        cat_label = Label(win_frame_left,text="Category")
        cat_label.grid(row=4,column=0)
        cat_select = OptionMenu(win_frame_left, clicked, *categories)
        cat_select.grid(row=4,column=1,sticky=EW)
        
        win_submit = Button(win_frame_left,text="Save (Or press <Enter>)",command=self.list_update,padx=5,pady=5)
        win_submit.grid(row=5,column=0,columnspan=2,sticky=EW)

        """ Binding the <Enter> key to the main window
            so we can just press the <Enter> key to udate  """
        win.bind('<Return>', lambda x:self.list_update())

        win_display = Button(win_frame_left,text="Show List",command=lambda:self.show_list(win_display_area),padx=5,pady=5)
        win_display.grid(row=6,column=0,columnspan=2,sticky=EW)

        win_display = Button(win_frame_left,text="Item Details",command=lambda:self.show_details(win_display_area),padx=5,pady=5)
        win_display.grid(row=7,column=0,columnspan=2,sticky=EW)

        win_display = Button(win_frame_left,text="Delete From List",command=lambda:self.delete_items(win_display_area),padx=5,pady=5)
        win_display.grid(row=8,column=0,columnspan=2,sticky=EW)

        edit_cat_btn = Button(win_frame_left,text="Edit Categories",command=self.edit_categories,justify='center')
        edit_cat_btn.grid(row=9,column=0,columnspan=2,sticky=EW,padx=5,pady=5)

        win_quit = Button(win_frame_left,text="Quit",command=lambda:exit(),padx=5,pady=5)
        win_quit.grid(row=10,column=0,columnspan=2,sticky=EW)

    ###################  Set Initial Focus
        item_input.focus_set()

        ###  Set padding on all widgets ###
        for widget in win_frame_left.winfo_children():
            widget.grid_configure(padx=10,pady=(5))    

        win.mainloop()

    ################################################### End Tk()



if __name__ == '__main__':
    my_cart = Cart()