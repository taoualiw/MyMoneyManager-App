import tkinter as tk
import pandas as pd
from functools import partial
import numpy as np
np.set_printoptions(precision=2)
pd.set_option("precision",2)
from mmm.functions import *
from mmm.moneyManager import *

class DataStatsTab(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._frame = None
        self.e1_value = tk.StringVar()
        self.e1_value.set(" ")
        self.switch_frame(DataStatsTab_Frame1)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()



# ==================first frame for DataImportTab=========================================================
class DataStatsTab_Frame1(tk.Frame):
    def show_category(self,category):
        name = category
        df = df_CategoryGroup(self.DF,category)
        self.update_text(df.T,name)

    def show_balance(self):
        name = "Balance"
        df_in = df_Income(self.DF)
        df_out = df_Outcome(self.DF)
        df = df_Balance(df_in,df_out)
        self.update_text(df.T,name)


    def show_income(self):
        name = "Income"
        df = df_Income(self.DF)
        self.update_text(df.T,name)


    def show_outcome(self):
        df = df_Outcome(self.DF)
        name = "Outcome"
        self.update_text(df.T,name)


    def update_text(self,df,name):
        self.nameText.destroy()
        self.sampleText.destroy()
        self.nameText = tk.Label (self, text = name, fg ="green",font=('Courier', 16, 'bold'))
        self.nameText.grid (row = 0, column = 5,sticky=tk.W,padx=0)
        self.sampleText = tk.Text(self, width =140, height=30, wrap=None)
        self.sampleText.insert(tk.END, df.to_string().split('\n')[0]+'\n',"HEAD")
        for i in range(len(df)):
            if i==0: continue
            self.sampleText.insert(tk.END, df.to_string().split('\n')[i]+'\n')
        self.sampleText.insert(tk.END, df.to_string().split('\n')[len(df)]+'\n',"AVG")
        self.sampleText.tag_config('AVG', foreground='black',font=('Courier', 12, 'bold'),background="gray65")
        self.sampleText.tag_config('HEAD', foreground='black',font=('Courier', 12, 'bold'))
        #self.sampleText.insert(tk.END, df.to_string())
        self.sampleText.grid (row = 1, column = 2,padx=25,pady=5,columnspan=6,rowspan=15,sticky=tk.W)

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.DF = self.master.master.master.DF.copy()
        self.DF.amount = self.DF.amount.round(2)
        categList = ["Income","Immediate Obligations", "Occasional Obligations", "General Expenses","Entertainment","Refundable","Travel", "To categorize"]
        self.nameText = tk.Label (self, text = "", fg ="green")
        self.nameText.grid (row = 0, column = 5,padx=25,pady=5,columnspan=6,rowspan=15,sticky=tk.W)
        self.sampleText = tk.Text(self, width =140, height=30, wrap=None)
        self.sampleText.grid (row = 1, column = 2,padx=25,pady=5,columnspan=6,rowspan=15,sticky=tk.W)
        if len(self.DF)>0:
            self.DF = self.DF.sort_values("trans_id")
            self.DF['month'] = pd.DatetimeIndex(self.DF['date']).strftime("%B %Y")
            self.show_balance()
            #
            #------------------------
            self.IncomeButton = tk.Button(self, text = "Income", command = self.show_income)
            self.IncomeButton.grid(row = 0, column = 0,padx=5, pady = 5,sticky=tk.W)
            #self.IncomeButton.config(state="disabled")
            #--------------------------------
            self.OutcomeButton = tk.Button(self, text = "Outcome", command = self.show_outcome)
            self.OutcomeButton.grid(row = 1, column = 0,padx=5, pady = 5,sticky=tk.W)
            #-----------------------
            self.BalanceButton = tk.Button(self, text = "Balance", command = self.show_balance)
            self.BalanceButton.grid(row = 2, column = 0,padx=5, pady = 5,sticky=tk.W)
            #-------------------------------
            i=3
            self.cButton = {}
            for category in categList[1:]:
                self.cButton[i] = tk.Button(self, text=category, command= partial(self.show_category,category))
                self.cButton[i].grid(row = i+1, column = 0,padx=5, pady = 5,sticky=tk.W)
                i=i+1
        else:
            self.sampleText.insert(tk.END, "No stats, Empty Data")


# ==================second frame for DataImportTab=========================================================
class DataStatsTab_Frame2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
