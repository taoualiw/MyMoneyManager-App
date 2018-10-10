import pandas as pd
import os
import numpy as np
np.set_printoptions(precision=2)

def import_transFileUFCU(path_transfilename):
    df = pd.read_csv(path_transfilename)
    acc = df.account_id.values
    df["account"]= [acc[i] for i in range(len(acc))]
    df["date"] = pd.DatetimeIndex(df['posted_at']).strftime("%m/%d/%y")
    day = pd.DatetimeIndex(df['posted_at']).strftime("%y%m%d")
    dayrank = (df.groupby(['date']).cumcount() + 1).values
    df["trans_id"] = [int(day[i]+np.str(dayrank[i])) for i in range(len(day))]
    df["payee"] = df.original_name.values
    trans_type  = np.array(df.transaction_type.values)
    trans_type[trans_type=="Credit"] = 1
    trans_type[trans_type=="Debit"] = -1
    df["amount"] = df.amount.values*trans_type
    df = df[["account","date","trans_id","payee","amount"]]
    df['categoryGroup'] = ["To categorize"]*len(df)
    df['category'] = ["To categorize"]*len(df)
    df = df.sort_values("trans_id")
    return df


def import_histFileUFCU(path_histfilename,account_id):
    df = pd.read_csv(path_histfilename,header=None)
    df.columns = ["date","payee","amount","balance"]
    df[df.columns[2:4]] = df[df.columns[2:4]].replace('[\$,]', '', regex=True).astype(float)
    df = df.sort_index(ascending=False)
    day = pd.DatetimeIndex(df['date']).strftime("%y%m%d")
    df["date"] = pd.DatetimeIndex(df['date']).strftime("%m/%d/%y")
    dayrank = (df.groupby(['date']).cumcount() + 1).values
    df["trans_id"] = [int(day[i]+np.str(dayrank[i])) for i in range(len(day))]
    df["account"]= [account_id]*len(df)
    df['categoryGroup'] = ["To categorize"]*len(df)
    df['category'] = ["To categorize"]*len(df)
    df = df[["account", "date", "trans_id", "payee", "amount", "categoryGroup","category"]]
    return df

def df_Income(myDF):
    c = "Income"
    monthList = myDF.month.drop_duplicates().values
    pattern = r'.*UT\sPayroll.*'
    myDF = myDF.replace(pattern, "UT Payroll",regex=True)
    dfc = myDF.loc[myDF.categoryGroup==c].groupby(["month","payee"])["amount"].sum().unstack(level=0)
    dfc = dfc.reindex(columns=monthList)
    #if correct: dfc = correct_forPayrollDelay(dfc)
    dfc.loc['Total']= dfc.sum()
    avg = dfc.mean(numeric_only=True, axis=1)
    tot = dfc.sum(numeric_only=True, axis=1)
    df = myDF.groupby(["month","categoryGroup"])["amount"].sum().unstack(level=0)
    dfc["Average"] = avg
    dfc["Total"] = tot
    return dfc
def df_Outcome(myDF):
    monthList = myDF.month.drop_duplicates().values
    categList = ["Income","Immediate Obligations", "Occasional Obligations", "General Expenses","Entertainment","Refundable","To categorize"]
    #if not excludeTravel:
    #   categList.append("Travel")
    df = myDF.groupby(["month","categoryGroup"])["amount"].sum().unstack(level=0)
    df = df[monthList]
    df = df.reindex(categList[1:])
    df.loc['Total']= df.sum()
    avg = df.mean(numeric_only=True, axis=1)
    tot = df.sum(numeric_only=True, axis=1)
    df["Average"] = avg
    df["Total"] = tot
    return df
def df_Balance(df_in,df_out):
    df_in_out = df_in.copy()
    df_in_out.loc["Total Income"] = df_in.loc["Total"]
    df_in_out.loc["Total Outcome"] = df_out.loc["Total"]
    df_in_out = df_in_out.loc[["Total Income","Total Outcome"]]
    #df_in_out.loc["Balance"] = df_in_out.sum()
    return df_in_out
def df_CategoryGroup(myDF,c):
    monthList = myDF.month.drop_duplicates().values
    dfc = myDF.loc[myDF.categoryGroup==c]
    if len(dfc)>0:
        dfc = dfc.groupby(["month","category"])["amount"].sum().unstack(level=0)
        dfc = dfc.reindex(columns=monthList)
        dfc.loc['Total']= dfc.sum()
        avg = dfc.mean(numeric_only=True, axis=1)
        tot = dfc.sum(numeric_only=True, axis=1)
        df = myDF.groupby(["month","categoryGroup"])["amount"].sum().unstack(level=0)
        dfc["Average"] = avg
        dfc["Total"] = tot
    return dfc

def categMenuOptions(myCategDF):
    cg = list(myCategDF.categoryGroup.drop_duplicates().values)
    categMenuOption = []
    for i in range(len(cg)):
        op = list(myCategDF.category[myCategDF.categoryGroup==cg[i]].drop_duplicates().values)
        op = tuple([cg[i]]+op+["To categorize"])
        categMenuOption.append(op)
    categMenuOption = tuple(categMenuOption)
    return categMenuOption
#------
def search_rows(DF, name, column ="payee"):
    DF = DF.reset_index(drop=True)
    return DF[DF[column].str.contains(name,regex=False)].index.values
def assign_learned_categories(DF, categoryDF, payee):
    rows = search_rows(categoryDF, payee)
    if len(rows)==1:
        cg = categoryDF.iloc[rows].iloc[0].categoryGroup
        c = categoryDF.iloc[rows].iloc[0].category
        rows = search_rows(DF, payee)
        for r in rows:
            if DF.iloc[r,6]=="To categorize":
                DF.iloc[r,6] = c
                DF.iloc[r,5] = cg
    return DF
#-----
