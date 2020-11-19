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
# import FREOP_Admin

#window
window = Tk()  
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))  
window.title('Login')
window.iconbitmap('C:/opencv/login.ico')  

global std_id, passwds, f_result, tst_pass, today
today = date.today()
std_id = StringVar()
passwds = StringVar()
f_result = StringVar()
f_result.set("")

class admin_page():
    # global mydb, test1, test2
    # test1 = StringVar()
    # test2 = StringVar()
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "face_user", 
        autocommit = True
    ) 

    # def update():
    #     if(test1.get() == "" or test2.get() == ""):
    #         messagebox.showerror('Result', 'Please fill the form')
    #     else:
    #         mycursor = mydb.cursor()
    #         admin_update = ("UPDATE test_name SET Test_Morning = %s, Test_Noon = %s WHERE Test_ID = 1001")
    #         mycursor.execute(admin_update,[(test1.get()), (test2.get())])
    #         messagebox.showinfo('Result', 'Update Success')

    def edit_page():
        if(std_id.get()=="" or passwds.get()==""):
            messagebox.showerror('Result', 'Please fill the form')
        else :
            while True:
                mycursor = mydb.cursor()
                find_user = ("select * from admin_table where A_ID = %s and A_Password = %s")
                # score_user = ("select Examination from stu_table where StudentId = %s and password = %s")
                mycursor.execute(find_user,[(std_id.get()), (passwds.get())])
                result = mycursor.fetchall()
                
                if result :
                    # AdminWindow = Tk()
                    # nw, nh = AdminWindow.winfo_screenwidth(), AdminWindow.winfo_screenheight()
                    # AdminWindow.geometry("%dx%d+0+0" % (nw, nh))
                    # window.destroy()   
                    # AdminWindow.title("Edit Page")

                    # lb1 = tk.Label(AdminWindow, text="Test 1 : ", 
                    #     font=("Times", 50))
                    # lb1.place(x=10, y=10)
                    # text1A = tk.Entry(AdminWindow, width=30, bd=5, 
                    #     textvariable = test1, font=("Times", 40))
                    # text1A.place(x=350, y=20, height=60)

                    # lb2 = tk.Label(AdminWindow, text="Test 2 : ", 
                    #     font=("Times", 50))
                    # lb2.place(x=10, y=120)
                    # text2A = tk.Entry(AdminWindow, width=30, bd=5, 
                    #     textvariable = test2, font=("Times", 40))
                    # text2A.place(x=350, y=135, height=60)

                    # admin_btn = tk.Button(AdminWindow, text="Change", 
                    #     font=("Times", 40), bg="green", fg="White", command=admin_page.update)
                    # admin_btn.place(x=530, y=570)

                    # AdminWindow.mainloop()
                    # execfile('FREOP_Admin.py')
                    os.system('py FREOP_Admin.py')
                else : 
                    messagebox.showerror('Message Box', 'Wrong Student ID or Password')
                break

class secure_page():
    global mydb
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "face_user"
        )        
    def cam_bonus():
        if(text1.get()=="" or text2.get()==""):
            messagebox.showinfo('Result', 'Please fill the form')
        else :
            while True:
                mycursor = mydb.cursor()
                find_user = ("select * from stu_table where StudentId = %s and password = %s")
                mycursor.execute(find_user, [(std_id.get()), (passwds.get())])
                result = mycursor.fetchall()

                if result :
                    camCursor = mydb.cursor() 
                    camCursor.execute("SELECT Name from stu_table where StudentId = %s", [(std_id.get())])
                    c_name = camCursor.fetchone()
                    c_name = '' + ''.join(c_name)

                    faceCascade = cv.CascadeClassifier("C:/opencv/haarcascade_frontalface_default.xml")
                    clf = cv.face.LBPHFaceRecognizer_create()
                    clf.read("C:/opencv/" + c_name + ".xml")

                    video_capture = cv.VideoCapture(0)
                    
                    def draw_boundary(img, classifier, ScaleFactor, minNeighbors, color, text, clf):
                        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #make image gray
                        features = classifier.detectMultiScale(gray_image, ScaleFactor, minNeighbors) #get face in cam

                        coords = []

                        for(x,y,w,h) in features:
                            cv.rectangle(img, (x,y), (x+w, y+h), color, 2) #create rectangle
                            id, pred = clf.predict(gray_image[y:y+h, x:x+w]) #predict face or see the similarity by using 2 values id & pred
                            confidence = float(100*(1-pred/300)) #distance

                            if confidence > 80:
                                if id == True:
                                    cv.putText(img,c_name + ": Match",(x, y-5), 
                                        cv.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv.LINE_AA)
                                    f_result.set("Match")
                            else:
                                cv.putText(img,"UNKNOWNS",(x, y-5), 
                                    cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv.LINE_AA)
                                f_result.set("Not Match")
                            break

                            coords = [x,y,w,h]
                        return coords

                    def recognize(img, clf, faceCascade):
                        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "face", clf)
                        return img

                    while True:
                        ret, img = video_capture.read()
                        img = recognize(img, clf, faceCascade)
                        cv.imshow("face detection", img)

                        if cv.waitKey(1) & 0xFF == 13 :
                            break

                    video_capture.release()
                    cv.destroyAllWindows()
                else : 
                    messagebox.showerror('Message Box', 'Wrong Student ID or Password')
                break

class login_page():
    global em_code
    global mydb
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "face_user"
    )       

    em_gen = []
    for i in range(2):
        # f_id = (std_id.get())
        filelist = random.choice(string.digits)
        symbol = random.choice(string.punctuation)
        alphabet = random.choice(string.ascii_letters)
        # p_gen.append(f_id)
        em_gen.append(symbol)
        em_gen.append(filelist)
        em_gen.append(alphabet)
    em_code = "".join(str(x) for x in em_gen)

    def mail_gen():
        mycursor = mydb.cursor()
        find_user = ("select * from stu_table where StudentId = %s and password = %s")
        mycursor.execute(find_user, [(std_id.get()), (passwds.get())])
        result = mycursor.fetchall()

        if(text1.get()=="" or text2.get()==""):
            messagebox.showinfo('Result', 'Please fill the form')
        elif(result):
            mail_menu = mydb.cursor() 
            mail_menu.execute("SELECT Email from stu_table where StudentId = %s and password = %s", [(std_id.get()), (passwds.get())])
            mail_address = mail_menu.fetchone()

            smtplibmail = smtplib.SMTP("smtp.gmail.com", 587)
            smtplibmail.ehlo()
            smtplibmail.starttls()
            smtplibmail.login("systempu2020@gmail.com", "quajctrgqatdvmxh")
            smtplibmail.sendmail("systempu2020@gmail.com", mail_address, em_code)
            smtplibmail.quit()

            messagebox.showinfo("Admin", "Your Passcode have been sent to your email")
            print(em_code)
        else:
            messagebox.showerror('Message Box', 'Wrong Student ID or Password')

    def tst_scdl():
        if(text1.get()=="" or text2.get()==""):
            messagebox.showerror('Result', 'Please fill the form')
        # if(text1.get()=="" or text2.get()=="" or text3.get()=="" or text4.get()==""):
        #     messagebox.showerror('Result', 'Please fill the form')
        # if(text1.get()=="" or text2.get()=="" or text4.get()==""):
        #     messagebox.showerror('Result', 'Please fill the form')
        # elif(text3.get()=="Not Match"):
        #     messagebox.showerror('Result', 'Face not recognized')
        # elif(text4.get() != em_code):
        #     messagebox.showerror('Result', 'Passcode not recognized')
        else :
            while True:
                mycursor = mydb.cursor()
                # myadmin = mydb.cursor(buffered=True)
                find_user = ("select * from stu_table where StudentId = %s and password = %s")
                # schedule_admin = ("select * from test_name WHERE Test_ID = 1001")
                mycursor.execute(find_user,[(std_id.get()), (passwds.get())])
                # myadmin.execute(schedule_admin)
                # sched = myadmin.fetchall()
                result = mycursor.fetchall()
                
                if result :
                    newWindow = Tk()
                    nw, nh = newWindow.winfo_screenwidth(), newWindow.winfo_screenheight()
                    newWindow.geometry("%dx%d+0+0" % (nw, nh))
                    window.destroy()   
                    newWindow.title("Option Page")

                    myadmin = mydb.cursor(buffered=True)
                    schedule_admin = ("select * from test_name WHERE Test_ID = 1001")
                    myadmin.execute(schedule_admin)
                    sched = myadmin.fetchall()

                    Ntbk = Notebook(newWindow)
                    Ntbk.pack()

                    def clock():
                        time_now = time.strftime("%H:%M:%S")
                        c_time.config(text=time_now)
                        c_time.after(1000, clock)

                    sch_tab = tk.Frame(Ntbk, width=nw, height=nw)
                    sch_tab.pack(fill="both", expand=10)

                    welcome_lbl = tk.Label(sch_tab, text="Examination Schedule", 
                        font=("Times", 50, "bold"), fg="blue")
                    welcome_lbl.place(x=nw*0.29, y=10)

                    rule_lbl0 = tk.Label(sch_tab, text="Rule : ", font=("Times", 20), fg="Black")
                    rule_lbl0.place(x=10, y=nh*0.1)

                    rule_lbl1 = tk.Label(sch_tab, text="1. Test Question vary depend on time", 
                        font=("Times", 15, "italic"), fg="red")
                    rule_lbl1.place(x=nw*0.05, y=nh*0.15)

                    rule_lbl2 = tk.Label(sch_tab, text="2. Once clicked finish, the result is immediate", 
                        font=("Times", 15, "italic"), fg="red")
                    rule_lbl2.place(x=nw*0.05, y=nh*0.185)

                    for z in sched:
                        test_name1 = tk.Label(sch_tab, text=z[1], 
                            font=("Times", 30), fg="Blue")
                        test_name1.place(x=nw*0.2, y=nh*0.4)

                        test_time1 = tk.Label(sch_tab, text="06:00 - 12:00", 
                            font=("Times", 30), fg="Blue")
                        test_time1.place(x=nw*0.3, y=nh*0.5)

                        test_name2 = tk.Label(sch_tab, text=z[2], 
                            font=("Times", 30), fg="Blue")
                        test_name2.place(x=nw*0.7, y=nh*0.4)

                        test_time2 = tk.Label(sch_tab, text="12:01 - 18:00", 
                            font=("Times", 30), fg="Blue")
                        test_time2.place(x=nw*0.7, y=nh*0.5)

                    bio_tab = tk.Frame(Ntbk, width=nw, height=nw)
                    bio_tab.pack(fill="both", expand=1)

                    for x in result:
                        Label(bio_tab, text="Name : "  + x[1], 
                            font=("Times", 30), anchor=W).place(x=400, y=90)
                        Label(bio_tab, text="Faculty : "  + x[2], 
                            font=("Times", 30), anchor=W).place(x=400, y=150)
                        Label(bio_tab, text="Email : "  + x[7], 
                            font=("Times", 30), anchor=W).place(x=400, y=210)
                        Label(bio_tab, text="Examination : " + x[5], 
                            font=("Times", 30), anchor=W).place(x=400, y=270)

                    c_time = tk.Label(bio_tab, text="", font=("Times",40), fg="white", bg="red", 
                        borderwidth=5, relief="raised")
                    c_time.place(x=10, y=10)

                    c_day = tk.Label(bio_tab, text=today, font=("Times",40), fg="white", bg="blue", 
                        borderwidth=5, relief="raised")
                    c_day.place(x=510, y=10)

                    lpage_btn = tk.Button(bio_tab, text="Test", font=("Times", 40), bg="green", 
                                fg="White", borderwidth=5, relief="raised", command=lambda:[newWindow.destroy(), test_page.path_opt()])
                    lpage_btn.place(x=nw*0.45, y=nh*0.7)

                    mpage_btn = tk.Button(bio_tab, text="Report", font=("Times", 40), bg="White", 
                                fg="black", borderwidth=5, command=lambda:[newWindow.destroy(), report_page.report_main()])
                    mpage_btn.place(x=nw*0.6, y=nh*0.7)

                    clock()
                    Ntbk.add(sch_tab, text="Exam Schedule")
                    Ntbk.add(bio_tab, text="Preparation")
                    newWindow.mainloop()
                else : 
                    messagebox.showerror('Message Box', 'Wrong Student ID or Password')
                break

class test_page():
    global mydb
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "face_user",
            autocommit=True
        )
    def path_opt():
        mycursor = mydb.cursor()
        update_time = ("UPDATE stu_table SET Test_Time = NOW() WHERE StudentID = %s and password=%s")
        mycursor.execute(update_time,[(std_id.get()), (passwds.get())])
        
        current_H = time.strftime("%H:%M:%S")
        if(current_H >= "06:00:00" and current_H <= "11:59:59"):
           test_page.TestCal()
        elif(current_H >= "12:00:00" and current_H <= "24:00:00"):
            test_page.TestAi()
    
    def TestCal():
        root = Tk() 
        sall = StringVar()
        QA1 = tk.BooleanVar()
        QA2 = tk.BooleanVar()

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))  
        root.title('Login')
        root.iconbitmap('C:/opencv/login.ico')  

        mycursor = mydb.cursor()
        update_time = ("UPDATE stu_table SET Score = %s, Examination = 'Artificial Intelligent' WHERE StudentID = %s and password=%s")

        def counter():
            if(QA1.get() == True):
                sall.set(sall.get() + "100")
                mycursor.execute(update_time,[(100), (std_id.get()), (passwds.get())])
                Btn_res.config(state=DISABLED, bg="gray", fg="black")
                Btn_rpt.config(state=NORMAL, bg="blue", fg="white")
            else:
                sall.set(sall.get() + "0")
                mycursor.execute(update_time,[(0), (std_id.get()), (passwds.get())])
                Btn_res.config(state=DISABLED, bg="gray", fg="black")
                Btn_rpt.config(state=NORMAL, bg="blue", fg="white")

        Q1 = tk.Label(root, text="1. 1 + 1 = ", font=("Times", 40)).place(x=450, y=50)
        Q1A = tk.Checkbutton(root, text="A. 2", font=("Times", 28), variable=QA1).place(x=30, y=120)
        Q1B = tk.Checkbutton(root, text="B. 1", font=("Times", 28)).place(x=550, y=120)
        Q1C = tk.Checkbutton(root, text="C. 5", font=("Times", 28)).place(x=970, y=120)

        Btn_res = tk.Button(root, text="Finish", command=counter, font=("Times", 40), bg="Green", fg="white")
        Btn_res.place(x=560, y=450) 

        Btn_rpt = tk.Button(root, text="Finish", command=lambda:[root.destroy(),report_page.report_main()], 
            font=("Times", 40), bg="gray", fg="black", state=DISABLED)
        Btn_rpt.place(x=760, y=450) 


        Label(root, text="Total:", font=("Times", 40)).place(x=400, y=300)
        Label(root, textvariable=sall, font=("Times", 40)).place(x=600, y=300)

        root.mainloop()

    def TestAI():
        root = Tk() 
        sall = StringVar()
        QA1 = tk.BooleanVar()
        QA2 = tk.BooleanVar()

        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))  
        root.title('Login')
        root.iconbitmap('C:/opencv/login.ico')  

        mycursor = mydb.cursor()
        update_time = ("UPDATE stu_table SET Score = %s, Examination = 'Computer Graphic Animation' WHERE StudentID = %s and password=%s")

        def counter():
            if(QA1.get() == True):
                sall.set(sall.get() + "100")
                mycursor.execute(update_time,[(100), (std_id.get()), (passwds.get())])
                Btn_res.config(state=DISABLED, bg="gray", fg="black")
                Btn_rpt.config(state=NORMAL, bg="blue", fg="white")
            else:
                sall.set(sall.get() + "0")
                mycursor.execute(update_time,[(0), (std_id.get()), (passwds.get())])
                Btn_res.config(state=DISABLED, bg="gray", fg="black")
                Btn_rpt.config(state=NORMAL, bg="blue", fg="white")

        Q1 = tk.Label(root, text="1. What is Tkinter", font=("Times", 40)).place(x=450, y=50)
        Q1A = tk.Checkbutton(root, text="A. Guided User Interface", font=("Times", 28), variable=QA1).place(x=30, y=120)
        Q1B = tk.Checkbutton(root, text="B. Variable", font=("Times", 28)).place(x=550, y=120)
        Q1C = tk.Checkbutton(root, text="C. Function", font=("Times", 28)).place(x=970, y=120)

        Btn_res = tk.Button(root, text="Finish", command=counter, font=("Times", 40), bg="Green", fg="white")
        Btn_res.place(x=560, y=450) 

        Btn_rpt = tk.Button(root, text="Report", command=lambda:[root.destroy(),report_page.report_main()], 
            font=("Times", 40), bg="white", fg="blue", state=DISABLED)
        Btn_rpt.place(x=760, y=450) 

        Label(root, text="Total:", font=("Times", 40)).place(x=400, y=300)
        Label(root, textvariable=sall, font=("Times", 40)).place(x=600, y=300)

        root.mainloop()

class report_page():
    mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "face_user",
            autocommit=True
        )

    def report_main():
        mail_window = Tk()
        nw, nh = mail_window.winfo_screenwidth(), mail_window.winfo_screenheight()
        mail_window.geometry("%dx%d+0+0" % (nw, nh))
        mail_window.title("Option Page")

        mycursor = mydb.cursor()
        find_user = ("select * from stu_table where StudentId = %s and password = %s")
        mycursor.execute(find_user,[(std_id.get()), (passwds.get())])
        result = mycursor.fetchall()

        welcome_lbl = tk.Label(mail_window, text="FREOP Result", 
            font=("Times", 50, "italic"), fg="blue")
        welcome_lbl.place(x=nw*0.35, y=10)

        for x in result:
            Label(mail_window, text="Name : "  + x[1], 
                font=("Times", 30), anchor=W).place(x=400, y=90)
            Label(mail_window, text="Faculty : "  + x[2], 
                font=("Times", 30), anchor=W).place(x=400, y=150)
            Label(mail_window, text="Email : "  + x[7], 
                font=("Times", 30), anchor=W).place(x=400, y=210)
            Label(mail_window, text="Examination : " + x[5], 
                font=("Times", 30), anchor=W).place(x=400, y=270)
            Label(mail_window, text="Examination : " + x[8], 
                font=("Times", 30), anchor=W).place(x=400, y=330)

        g_pdf = tk.Button(mail_window, text="Generate", font=("Times", 40), bg="green", 
                    fg="White", borderwidth=5, relief="raised", command=report_page.generate_send)
        g_pdf.place(x=nw*0.2, y=nh*0.7)

        s_pdf = tk.Button(mail_window, text="Send", font=("Times", 40), bg="blue", 
                    fg="white", borderwidth=5, relief="raised", command=report_page.send_pdf)
        s_pdf.place(x=nw*0.45, y=nh*0.7)


        mail_window.mainloop()

    def generate_send():
        global today
        today = time.strftime("%d, %B %Y")
        mycursor = mydb.cursor()
        find_user = ("select * from stu_table where StudentId = %s and password = %s")
        mycursor.execute(find_user,[(std_id.get()), (passwds.get())])
        result = mycursor.fetchall()

        for z in result:
            fileName = z[1] + '.pdf'
            title = z[1] 

        def USer_Profile(pdf):
            pdf.drawString(70, 680, "Name") 
            pdf.drawString(170, 680, ":")
            pdf.drawString(70, 660, "Student ID")
            pdf.drawString(170, 660, ":")
            pdf.drawString(70, 640, "Study Program")
            pdf.drawString(170, 640, ":")
            pdf.drawString(70, 620, "Test-Time")
            pdf.drawString(170, 620, ":")

            
            for x in result:
                pdf.setFont('Times-Bold', 15)
                pdf.drawString(190, 680, x[1])
                pdf.drawString(190, 660, str(x[0]))
                pdf.drawString(190, 640, x[2] + " / " + x[3])
                pdf.drawString(190, 620, str(x[6]))

        def logo(pdf):
            pdf.drawInlineImage('C:/opencv/PU.jpg', 120, 720, width=80, height=50)
            
            pdf.setFillColorRGB(0, 0, 200)
            pdf.setFont("Times-Bold", 30)
            pdf.drawCentredString(258, 745, 'President')

            pdf.setFillColorRGB(255, 0, 0)
            pdf.setFont("Times-Bold", 30)
            pdf.drawCentredString(395, 745, 'University ')

        def main_body(pdf):
            proof = 'This Letter is a proof that user participate in FREOP test. The result of user test is shown below : '

            for x in result:
                pdf.setFont("Times-Bold", 13)
                pdf.drawString(220, 525, x[5])
                pdf.drawString(220, 505, x[8])
            
            pdf.setFont("Times-Roman", 12.7)
            pdf.drawString(70, 555, proof)
            pdf.drawString(170, 525, "Subject :")
            pdf.drawString(170, 505, "Score : ")
            

        #PDF Title
        pdf = canvas.Canvas(fileName)
        pdf.setTitle(title)
        # drawMyRuler(pdf)
        main_body(pdf)
        USer_Profile(pdf)
        logo(pdf)

        #PDF Body
        pdfmetrics.registerFont(TTFont('font2', 'A_Signature.ttf'))
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont('font2', 25)
        pdf.drawString(460, 340, "Thoriq")

        pdf.setFont('Times-Roman', 12)
        pdf.drawString(430, 410, str(today))
        pdf.drawString(430, 380, 'Acknowledge by,')
        pdf.drawString(430, 300, 'Achmad Thoriq Almuhdor')
        pdf.drawString(430, 270, 'Creator of FREOP App')


        pdf.setFont('Times-Bold', 15)
        pdf.drawString(250, 725, "FREOP Test Result")

        pdf.line(430, 320, 560, 320)
        pdf.line(70, 710, 560, 710)
        pdf.save()
        messagebox.showinfo('Result', 'PDF have been generated')

    def send_pdf():
        pdf_db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "face_user"
        )

        mail_menu = pdf_db.cursor() 
        mail_menu.execute("SELECT * from stu_table where StudentId = %s and password = %s", [(std_id.get()), (passwds.get())])
        mail_address = mail_menu.fetchall()

        for z in mail_address:
            email_user = 'systempu2020@gmail.com'
            email_password = 'quajctrgqatdvmxh'
            email_send = z[7]
            filename= z[1]+'.pdf'

            subject = 'FREOP Test Result'

            #Setup the MIME
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject

            #The body and the attachments for the mail
            body = 'Here is your FREOP result : '
            msg.attach(MIMEText(body,'plain'))
            attachment  =open(filename,'rb')

            part = MIMEBase('application','octet-stream') #header attach
            part.set_payload((attachment).read())
            encoders.encode_base64(part) #encode the attachment
            part.add_header('Content-Disposition',"attachment; filename= "+filename)

            #Create SMTP session for sending the mail
            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(email_user,email_password)


            server.sendmail(email_user,email_send,text)
            messagebox.showinfo('INFO', 'PDF File have been sent to your email')
            server.quit()

lb1 = tk.Label(window, text="Student ID : ", 
    font=("Times", 50))
lb1.place(x=10, y=10)
text1 = tk.Entry(window, width=30, bd=5, 
    textvariable = std_id, font=("Times", 40))
text1.place(x=350, y=20, height=60)

lb2 = tk.Label(window, text="Password : ", 
    font=("Times", 50))
lb2.place(x=10, y=120)
text2 = tk.Entry(window, width=30, bd=5, 
    textvariable = passwds, font=("Times", 30), show="*")
text2.place(x=350, y=135, height=60)

lb3 = tk.Label(window, text="Face : ", 
    font=("Times", 50))
lb3.place(x=10, y=230)
text3 = tk.Entry(window, width=30, bd=5, 
    textvariable = f_result, font=("Times", 30), state=DISABLED)
text3.place(x=350, y=245, height=60)

b_face = tk.Button(window, text="Recog", 
    font=("Times", 24), bg="Blue", fg="White", command=secure_page.cam_bonus, width=10)
b_face.place(x=970, y=245)

lb4 = tk.Label(window, text="Match : ", 
    font=("Times", 50))
lb4.place(x=10, y=340)
text4 = tk.Entry(window, width=30, bd=5, 
    font=("Times", 30))
text4.place(x=350, y=355, height=60)

mail_btn = tk.Button(window, text="Email", 
    font=("Times", 24), bg="Blue", fg="White", command=login_page.mail_gen, width=10)
mail_btn.place(x=970, y=355)

login_btn = tk.Button(window, text="Student", 
    font=("Times", 40), bg="green", fg="White", command=login_page.tst_scdl)
login_btn.place(x=330, y=570)

admin_btn = tk.Button(window, text="Admin", 
    font=("Times", 40), bg="green", fg="White", command=admin_page.edit_page)
admin_btn.place(x=730, y=570)

c_label = tk.Label(window, text="", 
    font=("Helvetica", 48), fg="green")
c_label.place(x=400, y=400)

window.mainloop()