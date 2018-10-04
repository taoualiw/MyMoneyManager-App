#!/usr/local/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
from dataImport import *
from dataEdition import *
from dataStats import *
from params import *
import os
import pdb;
import sys;

# Root class to create the interface and define the controller function to switch frames
class MoneyManagerApp(tk.Tk):
    def importExistingData(self):
        #---------------
        if not os.path.exists(path_myfiles):
            os.mkdir(path_myfiles)
            print("Directory " , path_myfiles ,  " Created ")
        try:
            myDF = pd.read_csv(path_myfiles+"/"+"myDF.csv")
            print(" Importing Existing Data ")
        except:
            print("Initializing Summary Data Frame...")
            myDF = pd.DataFrame()
            myDF = myDF.reindex(columns = ["account","date","trans_id","payee","amount",'categoryGroup','category'])
        #display(myDF.head())
        #---------
        try:
            myCategDF = pd.read_csv(path_myfiles+"/"+"myCategDF.csv")
            print(" ")
            print("Importing Categorization Data Frame ")
        except:
            print("Initializing Category Data Frame...")
            try:
                myCategDF = pd.read_csv(os.path.abspath(os.getcwd() + "/../Resources")+"/"+"myCategDF.csv")
            except:
                myCategDF = pd.read_csv(os.path.abspath(os.getcwd() + "../resources/myCategDF.csv"))
                #myCategDF = myCategDF.reindex(columns = ['payee','categoryGroup','category'])
            #myCategDF.to_csv(path_myfiles+"/"+"myCategDF.csv",index=False)
        return myDF, myCategDF
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.attributes("-topmost", True)
        self.title('My Money Manager')
        self.geometry('1500x500')
        DF, CategDF = self.importExistingData()
        self.DF = DF.copy()
        self.CategDF = CategDF.copy()
        self.switch_frame(MoneyManagerNoteBook)

    # controller function
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# sub-root to contain the Notebook frame and a controller function to switch the tabs within the notebook
class MoneyManagerNoteBook(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.notebook = ttk.Notebook()
        self.DataImportTab = DataImportTab(self.notebook)
        self.DataEditionTab = DataEditionTab(self.notebook)
        self.DataStatsTab = DataStatsTab(self.notebook)
        self.notebook.add(child =self.DataImportTab, text="Data Import")
        self.notebook.add(child =self.DataEditionTab, text="Data Edition")
        self.notebook.add(child =self.DataStatsTab, text="Data Stats")
        self.notebook.pack()
    def update_notebook(self):
        new_frame = DataEditionTab(self.notebook)
        newCategDF = self.master.DF[["payee","categoryGroup","category"]].loc[self.master.DF.category!="To categorize"]
        self.master.CategDF  = pd.concat([newCategDF , self.master.CategDF], ignore_index=True).drop_duplicates().reset_index(drop=True)
        self.DataEditionTab.destroy()
        self.DataEditionTab = new_frame
        new_frame = DataStatsTab(self.notebook)
        self.DataStatsTab.destroy()
        self.DataStatsTab = new_frame
        self.notebook.add(child =self.DataEditionTab, text="Data Edition")
        self.notebook.add(child =self.DataStatsTab, text="Data Stats")
        self.notebook.pack()
        self.master.DF.to_csv(path_myfiles+"/"+"myDF.csv",index=False)
        self.master.CategDF.to_csv(path_myfiles+"/"+"myCategDF.csv",index=False)

# Notebook - Tab 3

if __name__ == "__main__":
     #pdb.set_trace();
     Root = MoneyManagerApp()
     Root.mainloop()
