import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import sys
import os
import pyodbc 
import pandas as pd
import numpy as np








def processLinkedList(unprocessedExcelData1, NewExcelDataFrame):
    x=0
    for x in range(len(unprocessedExcelData1)):
        print(x ," / ",len(unprocessedExcelData1))
        if  unprocessedExcelData1.iloc[x]["barcode"] == unprocessedExcelData1.iloc[x]["S_barcode"]:
            tempReadData = unprocessedExcelData1.iloc[x]
            tempReadData = tempReadData.to_frame()
            tempReadData = tempReadData.transpose()
            NewExcelDataFrame = pd.concat([NewExcelDataFrame, tempReadData],ignore_index=True)
            
            
            
        elif unprocessedExcelData1.iloc[x]["barcode"] != unprocessedExcelData1.iloc[x]["S_barcode"]:
            # found = unprocessedExcelData1[unprocessedExcelData1['barcode'].str.contains(unprocessedExcelData1.iloc[x]["barcode"] )]
            # checkTimes= found.count()
            # print(found.count())

            # if unprocessedExcelData1.iloc[x]["barcode"] in unprocessedExcelData1['barcode'].values:
            #     tempReadData = unprocessedExcelData1.iloc[x]
            #     tempReadData["barcode"] = unprocessedExcelData1.iloc[x]["S_barcode"]
            #     tempReadData = tempReadData.to_frame()
            #     tempReadData = tempReadData.transpose()
            #     NewExcelDataFrame = pd.concat([NewExcelDataFrame, tempReadData],ignore_index=True)
                

            # else:
            #     tempReadData = unprocessedExcelData1.iloc[x]
            #     tempReadData = tempReadData.to_frame()
            #     tempReadData = tempReadData.transpose()
            #     NewExcelDataFrame = pd.concat([NewExcelDataFrame, tempReadData],ignore_index=True)

            #     tempReadData = unprocessedExcelData1.iloc[x]
            #     tempReadData["barcode"] = unprocessedExcelData1.iloc[x]["S_barcode"]
            #     tempReadData = tempReadData.to_frame()
            #     tempReadData = tempReadData.transpose()
            #     NewExcelDataFrame = pd.concat([NewExcelDataFrame, tempReadData],ignore_index=True)
            
            tempReadData = unprocessedExcelData1.iloc[x]
            tempReadData = tempReadData.to_frame()
            tempReadData = tempReadData.transpose()
            NewExcelDataFrame = pd.concat([NewExcelDataFrame, tempReadData],ignore_index=True)
            tempReadData = unprocessedExcelData1.iloc[x]
            tempReadData["barcode"] = unprocessedExcelData1.iloc[x]["S_barcode"]
            tempReadData = tempReadData.to_frame()
            tempReadData = tempReadData.transpose()
            NewExcelDataFrame = pd.concat([NewExcelDataFrame, tempReadData],ignore_index=True)

    NewExcelDataFrame.drop_duplicates(subset=['barcode'],keep='first')
    return NewExcelDataFrame
                

def processUnlinkedList(unprocessedExcelData2, NewExcelDataFrame):
    y=0
    for y in range(len(unprocessedExcelData2)):
        print(y ," / ",len(unprocessedExcelData2))
        tempReadData = unprocessedExcelData2.iloc[y]
        tempReadData = tempReadData.to_frame()
        tempReadData = tempReadData.transpose()
        NewExcelDataFrame = pd.concat([NewExcelDataFrame, tempReadData],ignore_index=True)

    NewExcelDataFrame.drop_duplicates(subset=['barcode'],keep='first')
    return NewExcelDataFrame







def processProductWithBarCode(connect_string):
    PassSQLServerConnection = pyodbc.connect(connect_string)

    linkedQuery = "SELECT top 50 Stock.*, StockBarcode.stock_id AS S_stock_id, StockBarcode.barcode AS S_barcode FROM Stock, StockBarcode WHERE Stock.stock_id = StockBarcode.stock_id order by Stock.stock_id"

    NonLinkedQuery = "SELECT top 50 Stock.* FROM Stock WHERE Stock.stock_id NOT IN ( SELECT Stock.stock_id FROM Stock, StockBarcode WHERE Stock.stock_id = StockBarcode.stock_id) "

    SqlResult1 = pd.read_sql_query(linkedQuery, PassSQLServerConnection)
    SqlResult2 = pd.read_sql_query(NonLinkedQuery, PassSQLServerConnection)

    print(SqlResult1.dtypes)
   
    # unprocessedExcelData1 = SqlResult1.astype(str)
    # unprocessedExcelData2 = SqlResult2.astype(str)
    unprocessedExcelData1 = SqlResult1
    unprocessedExcelData2 = SqlResult2
    


   

    NewExcelDataFrame = pd.DataFrame()
  

    print("total Linke rows: ")
    print(len(unprocessedExcelData1))

    
    print("total unlinked rows: ")
    print(len(unprocessedExcelData2))
  


    NewExcelDataFrame=processLinkedList(unprocessedExcelData1,NewExcelDataFrame)
    NewExcelDataFrame=processUnlinkedList(unprocessedExcelData2,NewExcelDataFrame)

   

    print("total rows: ")
    print(len(NewExcelDataFrame))
    NewExcelDataFrame=NewExcelDataFrame.astype(str)
    
    
    NewExcelDataFrame.drop_duplicates(subset=['barcode'],keep='first', ignore_index=True)
    print("Export to new excel")
    NewExcelDataFrame.to_excel(r'export_dataframe.xlsx', index = True, header=True)
    print("Process completed")

    #print("Start convert to DDA")
    #DDAExcel = pd.DataFrame()
    #DDADataTemplete = pd.read_excel('DDA_Templet.xlsx', index_col=None,dtype = str)
    #DDAExcel=DDADataTemplete.astype("string")

    #DDAExcel = convertToDDAExcel(NewExcelDataFrame,DDAExcel)

    #DDAExcel.to_excel(r'outPut.xls', index = False, header=True)
    messagebox.showinfo(title="Process Completed",message="Data Process Completed")

    
def ConnectionTest(connect_string):
    connectionTestResult = 0
   
    PassSQLServerConnection = pyodbc.connect(connect_string)

    print(connect_string)
    try:
        PassSQLServerConnection = pyodbc.connect(connect_string)
        print("{c} is working".format(c=connect_string))
        PassSQLServerConnection.close()
        connectionTestResult = 1
    except pyodbc.Error as ex:
        #print("{c} is not working".format(c=connect_string))
        messagebox.showerror(title="Error", message="{c} is not working")

    return connectionTestResult


def inforProcess(DBSource,DBUsername,DBPassword,DBName):
    connectionTestResult=0
    connect_string = 'DRIVER={SQL Server}; SERVER='+DBSource+'; DATABASE='+DBName+'; UID='+DBUsername+'; PWD='+ DBPassword
    if DBName=="":
        messagebox.showerror(title="Error", message="DB Name Field is Empty!!")
        connectionTestResult = 0
    else:
        connectionTestResult=ConnectionTest(connect_string)

    if connectionTestResult==1:
        print("next")
        processProductWithBarCode(connect_string)

    else:
        print("error")







class App:
    def __init__(self, root):
        #setting title
        root.title("AUPOS Converter")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_DB_Source=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_DB_Source["font"] = ft
        GLabel_DB_Source["fg"] = "#333333"
        GLabel_DB_Source["justify"] = "left"
        GLabel_DB_Source["text"] = "DB Connection"
        GLabel_DB_Source.place(x=50,y=90,width=90,height=30)

        DBSource_Box=tk.Entry(root)
        DBSource_Box["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        DBSource_Box["font"] = ft
        DBSource_Box["fg"] = "#333333"
        DBSource_Box["justify"] = "left"
        DBSource_Box.insert(0,'localhost\sqlexpress2008r2')
        #DBSource_Box["text"] = "localhost\sqlexpress2008r2"
        
        DBSource_Box.place(x=190,y=90,width=275,height=30)

        DB_UserName_Label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        DB_UserName_Label["font"] = ft
        DB_UserName_Label["fg"] = "#333333"
        DB_UserName_Label["justify"] = "left"
        DB_UserName_Label["text"] = "User Name"
        DB_UserName_Label.place(x=50,y=140,width=90,height=30)

        DB_UserName_Box=tk.Entry(root)
        DB_UserName_Box["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        DB_UserName_Box["font"] = ft
        DB_UserName_Box["fg"] = "#333333"
        DB_UserName_Box["justify"] = "left"
        #DB_UserName_Box["text"] = "sa"
        DB_UserName_Box.insert(0,'sa')
        DB_UserName_Box.place(x=190,y=140,width=275,height=30)

        DB_Password_Label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        DB_Password_Label["font"] = ft
        DB_Password_Label["fg"] = "#333333"
        DB_Password_Label["justify"] = "left"
        DB_Password_Label["text"] = "Password"
        DB_Password_Label.place(x=50,y=200,width=90,height=25)

        DB_Password_Box=tk.Entry(root)
        DB_Password_Box["borderwidth"] = "1px"
        
        ft = tkFont.Font(family='Times',size=10)
        DB_Password_Box["font"] = ft
        DB_Password_Box["fg"] = "#333333"
        DB_Password_Box["justify"] = "left"
        #DB_Password_Box["text"] = "0000"
        DB_Password_Box.insert(0,'0000')
        DB_Password_Box.place(x=190,y=200,width=275,height=30)
        DB_Password_Box["show"] = "*"

        
        
        DB_Name_Label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        DB_Name_Label["font"] = ft
        DB_Name_Label["fg"] = "#333333"
        DB_Name_Label["justify"] = "left"
        DB_Name_Label["text"] = "DB Name"
        DB_Name_Label.place(x=50,y=260,width=90,height=25)

        DB_Name_Box=tk.Entry(root)
        DB_Name_Box["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        DB_Name_Box["font"] = ft
        DB_Name_Box["fg"] = "#333333"
        DB_Name_Box["justify"] = "left"    
        DB_Name_Box.place(x=190,y=260,width=275,height=30)
        DB_Name_Box.insert(0,'AUPOS_F')
 









         #-----------------Functions---------------------------------
        def getDBSource():
            result=DBSource_Box.get()
            return result
           
            
        def getDBUsername():
            result=DB_UserName_Box.get()
            return result
      
        def getDBPassword():
            result=DB_Password_Box.get()
            return result
        
        def getDBName():
            result=DB_Name_Box.get()
            return result
      
        
        def StartConversionProcess():
            DBSource=getDBSource()
            username=getDBUsername()
            password=getDBPassword()
            databaseName=getDBName()
            #inforProcess(DBSource,DBUsername,DBPassword,DBName):
            inforProcess(DBSource,username,password,databaseName)
            

        def testDBSource():
            DBSource=getDBSource()
            username=getDBUsername()
            password=getDBPassword()
            databaseName=getDBName()
            connect_string = 'DRIVER={SQL Server}; SERVER='+DBSource+'; DATABASE='+databaseName+'; UID='+username+'; PWD='+ password
            PassSQLServerConnection = pyodbc.connect(connect_string)
            if databaseName=="":
                messagebox.showerror(title="Error", message="DB Name Field is Empty!!")
            else:
                try:
                    PassSQLServerConnection = pyodbc.connect(connect_string)
                    print("{c} is working".format(c=connect_string))
                    PassSQLServerConnection.close()
                except pyodbc.Error as ex:
               
                    print("{c} is not working".format(c=connect_string))
                    messagebox.showerror(title="Error", message="{c} is not working")
          
            




            
            


            
            
        
        
        

            















        



            
#--------------Button Actions-------------------------
        Star_Button=tk.Button(root)
        Star_Button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Star_Button["font"] = ft
        Star_Button["fg"] = "#000000"
        Star_Button["justify"] = "center"
        Star_Button["text"] = "Start"
        Star_Button.place(x=70,y=390,width=90,height=45)
        Star_Button["command"] = StartConversionProcess

        TEST_Button=tk.Button(root)
        TEST_Button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        TEST_Button["font"] = ft
        TEST_Button["fg"] = "#000000"
        TEST_Button["justify"] = "center"
        TEST_Button["text"] = "Test DB Connection"
        TEST_Button.place(x=250,y=390,width=90,height=45)
        TEST_Button["command"] = testDBSource

        Close_Button=tk.Button(root)
        Close_Button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Close_Button["font"] = ft
        Close_Button["fg"] = "#000000"
        Close_Button["justify"] = "center"
        Close_Button["text"] = "Close"
        Close_Button.place(x=420,y=390,width=90,height=45)
        Close_Button["command"] = self.Close_Button_command
       
        




#----------------Not in use--------------------------------
    def Star_Button_command(self):
        print("Star_Button_command")
    def TEST_Button_command(self):
        print("command")
    def Close_Button_command(self):
        print("Exit")
        exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()