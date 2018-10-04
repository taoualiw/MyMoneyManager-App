import tkinter as tk
import pandas as pd
from functools import partial

from functions import *
from moneyManager import *

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
        df = df_CategoryGroup(self.DF,category)
        self.update_text(df.T)

    def show_balance(self):
        df_in = df_Income(self.DF)
        df_out = df_Outcome(self.DF)
        df = df_Balance(df_in,df_out)
        self.update_text(df.T)


    def show_income(self):
        df = df_Income(self.DF)
        self.update_text(df.T)


    def show_outcome(self):
        df = df_Outcome(self.DF)
        self.update_text(df.T)


    def update_text(self,df):
        self.sampleText.destroy()
        self.sampleText = tk.Text(self, width =140, height=30, wrap=None)
        self.sampleText.insert(tk.END, df.to_string())
        self.sampleText.grid (row = 0, column = 2,padx=25,pady=5,columnspan=6,rowspan=15,sticky=tk.W)
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.DF = self.master.master.master.DF.copy()
        categList = ["Income","Immediate Obligations", "Occasional Obligations", "General Expenses","Entertainment","Refundable","Travel", "To categorize"]
        self.sampleText = tk.Text(self, wrap=None)
        self.sampleText.grid (row = 0, column = 2,padx=25,pady=5,columnspan=6,rowspan=15,sticky=tk.W)
        if len(self.DF)>0:
            self.DF = self.DF.sort_values("trans_id")
            self.DF['month'] = pd.DatetimeIndex(self.DF['date']).strftime("%B %Y")
            self.show_income()
            #------------------------
            self.IncomeButton = tk.Button(self, text = "Income", command = self.show_income)
            self.IncomeButton.grid(row = 0, column = 0,padx=5, pady = 5,sticky=tk.W)
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
