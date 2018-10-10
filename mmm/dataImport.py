# Notebook - Tab 1
import tkinter as tk
from tkinter import filedialog
import pandas as pd

from mmm.functions import *
from mmm.moneyManager import *

class DataImportTab(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._frame = None
        self.impDF = pd.DataFrame()
        self.switch_frame(DataImportTab_Frame1)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def openFile(self):
        self.master.master.attributes("-topmost", False)
        self.fname = filedialog.askopenfilename(initialdir = os.path.abspath(os.getcwd() + "/../"),title = "Select file",filetypes = [("csv files","*.csv")])
        self.master.master.attributes("-topmost", True)
        self.update()
        try:
            self.impDF = import_transFileUFCU(self.fname)
            isAccountId = True
        except:
             try:
                 self.impDF = import_histFileUFCU(self.fname,0)
                 isAccountId = False
             except:
                 self.impDF = pd.DataFrame()
                 isAccountId = None
        return isAccountId
# ==================first frame for DataImportTab=========================================================
class DataImportTab_Frame1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.openButton = tk.Button(self, text='Open', command=lambda: master.switch_frame(DataImportTab_Frame2))
        self.openButton.grid (row = 0, column = 2,padx=5,sticky=tk.W)
        if len(master.impDF)>0:
            newDF = pd.concat([master.impDF , master.master.master.DF], ignore_index=True)
            newDF = newDF.drop_duplicates(subset=['account', 'trans_id',"amount"], keep="last").reset_index(drop=True)
            master.master.master.DF = newDF.sort_values("trans_id")
            self.fname = ""
            master.impDF = pd.DataFrame()
            status = "Status: Data imported, press Open to import a new file"
            master.master.master._frame.update_notebook()

        else:
            status ="Status: Press Open to select a file"
        self.statusLabel  = tk.Label (self, text = status,fg ="green" )
        self.statusLabel.grid (row = 0, column = 0, columnspan=1, sticky=tk.W, padx=0)

# ==================second frame for DataImportTab=========================================================
class DataImportTab_Frame2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        isAccountId = master.openFile()
        if len(master.impDF)>0:
            self.sampleText = tk.Text(self, width =130, height=6, wrap=None)
            self.sampleText.insert(tk.END, master.impDF.head(5).to_string())
            self.sampleText.grid (row = 2, column = 0,padx=20,pady=10,columnspan=6,rowspan=5,sticky=tk.W)
            if isAccountId==True:
                status = "Status: File Preview, press Download to import the data"
            else:
                status = "Status: File Preview, Warning: Account id missing set by default to 0 (ex:31858870)"
                self.e1_value = tk.IntVar()
                self.e1_value.set(0)
                self.accountId = tk.Entry (self,textvariable=self.e1_value)
                self.accountIdLabel  = tk.Label (self, text = "Insert account id then press download",fg="red")
                self.accountId.grid (row = 14, column = 2,padx=20)
                self.accountIdLabel.grid (row = 14, column = 0,padx=20)
                master.impDF = import_histFileUFCU(master.fname, self.e1_value.get())
            self.submitButton = tk.Button(self, text = "Download", command=lambda: master.switch_frame(DataImportTab_Frame1))
            self.submitButton.grid(row = 16, column = 4, sticky = "W",pady=30)
        else:
            status = "Status: "+master.fname+" Format not recognized, select another file"
        self.statusLabel  = tk.Label (self, text = status, fg ="green")
        self.statusLabel.grid (row = 0, column = 0,sticky=tk.W,padx=0)
        self.openButton = tk.Button(self, text='Open', command=lambda: master.switch_frame(DataImportTab_Frame2))
        self.openButton.grid (row = 0, column = 2,padx=5,sticky=tk.W)
