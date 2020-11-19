import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import cv2 as cv
import os, random, string, smtplib, time, mysql.connector
import numpy as np
from PIL import Image, ImageTk
import datetime
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

global mydb
# test1 = StringVar()
# test2 = StringVar()
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "face_user", 
    autocommit = True
    ) 

def update():
    if(text1A.get() == "" or text2A.get() == ""):
        messagebox.showerror('Result', 'Please fill the form')
    else:
        mycursor = mydb.cursor()
        admin_update = ("UPDATE test_name SET Test_Morning = %s, Test_Noon = %s WHERE Test_ID = 1001")
        mycursor.execute(admin_update,[(text1A.get()), (text2A.get())])
        messagebox.showinfo('Result', 'Update Success')


AdminWindow = Tk()
nw, nh = AdminWindow.winfo_screenwidth(), AdminWindow.winfo_screenheight()
AdminWindow.geometry("%dx%d+0+0" % (nw, nh))
# window.destroy()   
AdminWindow.title("Edit Page")

lb1 = tk.Label(AdminWindow, text="Test 1 : ", 
    font=("Times", 50))
lb1.place(x=10, y=10)
text1A = tk.Entry(AdminWindow, width=30, bd=5, 
    font=("Times", 40))
text1A.place(x=350, y=20, height=60)

lb2 = tk.Label(AdminWindow, text="Test 2 : ", 
    font=("Times", 50))
lb2.place(x=10, y=120)
text2A = tk.Entry(AdminWindow, width=30, bd=5, 
     font=("Times", 40))
text2A.place(x=350, y=135, height=60)

admin_btn = tk.Button(AdminWindow, text="Change", 
    font=("Times", 40), bg="green", fg="White", command=update)
admin_btn.place(x=530, y=570)

AdminWindow.mainloop()