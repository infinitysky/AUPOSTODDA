import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_444=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_444["font"] = ft
        GLabel_444["fg"] = "#333333"
        GLabel_444["justify"] = "center"
        GLabel_444["text"] = "DB Connection"
        GLabel_444.place(x=50,y=90,width=109,height=30)

        GLineEdit_133=tk.Entry(root)
        GLineEdit_133["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_133["font"] = ft
        GLineEdit_133["fg"] = "#333333"
        GLineEdit_133["justify"] = "left"
        GLineEdit_133["text"] = "localhost\sqlexpress2008r2"
        GLineEdit_133.place(x=190,y=90,width=269,height=30)

        GLabel_45=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_45["font"] = ft
        GLabel_45["fg"] = "#333333"
        GLabel_45["justify"] = "center"
        GLabel_45["text"] = "User Name"
        GLabel_45.place(x=50,y=140,width=90,height=30)

        GLineEdit_510=tk.Entry(root)
        GLineEdit_510["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_510["font"] = ft
        GLineEdit_510["fg"] = "#333333"
        GLineEdit_510["justify"] = "left"
        GLineEdit_510["text"] = "sa"
        GLineEdit_510.place(x=190,y=140,width=271,height=30)

        GLabel_483=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_483["font"] = ft
        GLabel_483["fg"] = "#333333"
        GLabel_483["justify"] = "center"
        GLabel_483["text"] = "label"
        GLabel_483.place(x=50,y=200,width=70,height=25)

        GLineEdit_62=tk.Entry(root)
        GLineEdit_62["borderwidth"] = "1px"
        GLineEdit_62["cursor"] = "star"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_62["font"] = ft
        GLineEdit_62["fg"] = "#333333"
        GLineEdit_62["justify"] = "left"
        GLineEdit_62["text"] = "0000"
        GLineEdit_62.place(x=190,y=190,width=272,height=30)
        GLineEdit_62["show"] = "undefined"

        GButton_141=tk.Button(root)
        GButton_141["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_141["font"] = ft
        GButton_141["fg"] = "#000000"
        GButton_141["justify"] = "center"
        GButton_141["text"] = "Start"
        GButton_141.place(x=70,y=390,width=90,height=45)
        GButton_141["command"] = self.GButton_141_command

        GButton_867=tk.Button(root)
        GButton_867["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_867["font"] = ft
        GButton_867["fg"] = "#000000"
        GButton_867["justify"] = "center"
        GButton_867["text"] = "Test DB Connection"
        GButton_867.place(x=250,y=390,width=90,height=45)
        GButton_867["command"] = self.GButton_867_command

        GButton_309=tk.Button(root)
        GButton_309["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_309["font"] = ft
        GButton_309["fg"] = "#000000"
        GButton_309["justify"] = "center"
        GButton_309["text"] = "Close"
        GButton_309.place(x=420,y=390,width=90,height=45)
        GButton_309["command"] = self.GButton_309_command

    def GButton_141_command(self):
        print("command")


    def GButton_867_command(self):
        print("command")


    def GButton_309_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
