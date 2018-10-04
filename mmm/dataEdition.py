import tkinter as tk
import pandas as pd
from functools import partial

from functions import *
from moneyManager import *
from params import *


class DataEditionTab(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._frame = None
        self.e1_value = tk.StringVar()
        self.e1_value.set(" ")
        self.switch_frame(DataEditionTab_Frame1)

    def switch_frame(self, frame_class,*event):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def applyLearnedCaregories(self):
        for label in self.master.master.CategDF.payee.values:
                self.master.master.DF = assign_learned_categories(self.master.master.DF, self.master.master.CategDF,label)
        self.switch_frame(DataEditionTab_Frame1)

# ==================first frame for DataImportTab=========================================================
class DataEditionTab_Frame1(tk.Frame):
    def select_clear_states(self):
            states = self.all_states.get()

            if states == 0:
                for i in range(len(self.Vars)):
                    self.Vars[i].set(0)
            if states == 1:
                for i in range(len(self.Vars)):
                    self.Vars[i].set(1)


    def state(self):
              return map((lambda var: var.get()), self.Vars)


    def create_checkButton(self,name):
        var = tk.IntVar()
        var.set(0)
        checkbox = tk.Checkbutton(self, text =name, variable=var, anchor=tk.W)
        checkbox.config(font=("Courier", 12))# depending on the font white spaces might be unequally evaluated
        return checkbox, var


    def create_allcheckButtons(self):
        checkButtons = []
        Vars = []
        if self.listTransToView[0]!= "Empty DataFrame":
            self.all_states = tk.IntVar()
            #--------------
            self.select_allButton = tk.Checkbutton(self, text = "", variable = self.all_states,anchor=tk.W, command = self.select_clear_states)
            self.header = tk.Label(self,text=self.listTransToView[0])
            self.header.config(font=("Courier", 12))
            #-------
            self.yscrollbar = tk.Scrollbar(self,orient="vertical")
            self.text = tk.Text(self,height=10,relief="groove",width=5+len(self.listTransToView[0]),borderwidth=0, highlightthickness=0,wrap="none",yscrollcommand=self.yscrollbar.set)
            self.yscrollbar.config(command=self.text.yview)
            for i in range(len(self.listTransToView)):
                if i==0:continue
                checkButton, var = self.create_checkButton(self.listTransToView[i])
                Vars.append(var)
                checkButtons.append(checkButton)
                self.text.window_create("end", window=checkButton)
                self.text.insert("end", "\n")
            self.text.configure(state="disabled")
            #---------------------------------------
            self.yscrollbar.grid(row=4, column=1, padx=0, sticky=tk.W, ipady=40)
            self.text.grid(row =4, column = 0,rowspan=5, sticky=tk.W, pady=0, padx=5)
            self.select_allButton.grid(row = 3, column = 0,padx=5, pady = 10,sticky=tk.W)
            self.header.grid(row = 3, column = 0,sticky=tk.W,padx=25,pady=10)
        else:
            self.text = tk.Text(self,height=10, width=100,relief="groove",borderwidth=0, highlightthickness=0,wrap="none")
            self.text.insert("end", "No transactions to view" )
            self.text.grid(row =4, column = 0,rowspan=5,sticky=tk.W,pady=0,padx=5)
        return Vars, checkButtons

    def remove_checkbuttons(self):
        # Remove the checkbuttons you want
        for chk_bx in self.checkButtons:
            chk_bx.destroy()


    def search_df(self):
        DF = self.master.master.master.DF.copy()
        res = pd.DataFrame(DF.to_string(index=False).split('\n')[1:])[0].str.contains(self.master.e1_value.get(),na=False, #ignore the cell's value is Nan
                                   case=False)
        self.search_result = DF.loc[res]
        self.listTransToView = self.search_result.to_string(index=False).split('\n')
        self.Vars, self.checkButtons = self.create_allcheckButtons()

    def saveName(self):
        searchRes = self.search_result.index.values
        states = np.array([self.Vars[i].get() for i in range(len(self.Vars))])
        selected = searchRes[states==1]
        if len(selected)>0:
            cg = ""
            for tup in categMenuOption:
                if self.selectvar.get() in list(tup):
                    cg = tup[0]
            if self.selectvar.get()=="To categorize": cg = "To categorize"
            for ind in selected:
                self.master.master.master.DF.loc[ind,"category"] = self.selectvar.get()
                self.master.master.master.DF.loc[ind,"categoryGroup"] = cg
            print("category updated to: ",self.selectvar.get() ,"for payee including :",self.searchField.get())
        #self._frame.destroy()
        #self.__init__(self, master)
        self.master.master.master._frame.update_notebook()
        self.master.master.master._frame.notebook.select(self.master.master.master._frame.DataEditionTab)

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.searchButton  = tk.Button(self, width=20, text='Search',   command=partial(master.switch_frame,DataEditionTab_Frame1))
        self.searchField = tk.Entry (self,textvariable=master.e1_value)

        self.searchField.bind("<Return>", partial(master.switch_frame,DataEditionTab_Frame1))
        self.searchButton.grid   (row = 2, column = 0,sticky="W")
        self.searchField.grid   (row = 2, column = 0,sticky="W",padx=200)
        #===========================================
        self.categAutoButton = tk.Button(self, width=20, text='Apply Learned Categories', command=master.applyLearnedCaregories)
        self.categAutoButton.grid   (row = 2, column = 0,padx=400,sticky="W")
        #==========================================
        self.search_df()
        #self.Vars, self.checkButtons = self.create_allcheckButtons()
        #============================================
        self.selectvar = tk.StringVar(value="To categorize")
        self.menubutton = tk.Menubutton(self, textvariable=self.selectvar , indicatoron=True,
                                   borderwidth=2, relief="raised", width=20)
        self.main_menu = tk.Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.main_menu)
        for item in categMenuOption:
            menu = tk.Menu(self.main_menu, tearoff=False)
            self.main_menu.add_cascade(label=item[0], menu=menu)
            for value in item[1:]:
                menu.add_radiobutton(value=value, label=value, variable=self.selectvar)
        self.menubutton.grid(row=15,column=0,pady=30,sticky = "W")
        #=======================================
        self.submitButton = tk.Button(self, text = "Submit", command = self.saveName)
        self.submitButton.grid(row = 16, column = 0, sticky = "W",pady=30)
# ==================second frame for DataImportTab=========================================================
class DataEditionTab_Frame2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
