'''Created on 25 Apr 2017 - Latest Update: ~~ 04/10/17 ~~
@author: Harrison Baillie - SteelPaladin'''
from tkinter import *
from tkinter import messagebox
import imaplib, smtplib, email, linecache
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
global prefwindowopen
prefwindowopen=False

def Preferences():
    print("Preferences")

def Login():
    root_3=Tk()
    gui_3=logonWindow(root_3)
    root_3.mainloop()

class logonWindow:
    def __init__(self, root):
        global checkvariable
        checkvariable=False
        def enter():
            global user, passw
            user=(self.entries[0].get())
            passw=(self.entries[1].get())
            if checkvariable == True:
                usercredentials=open('UsrCrdn.txt','w')
                usercredentials.write(str(self.entries[0].get()+"\n"))
                usercredentials.write(str(self.entries[1].get()+"\n"))
                usercredentials.close()
            self.vet=True
            try:
                mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
                mail.login(user,passw)
                mail.select("INBOX")
            except:
                SMTPAuthenticationError
                messagebox.showerror("Authentication","Unable to login.")
                self.vet=False
            if self.vet==True:
                messagebox.showinfo('Login','User successfully logged in')
                self.root.destroy() #Destroying the login window
        def checkCommand():
            global checkvariable
            if checkvariable == False:
                checkvariable=True
            else:
                checkvariable=False
        self.root=root
        root.title('MailPy - Login')
        root.iconbitmap('MailPy Logo.ico')
        root.resizable(False,False)
        root.geometry('300x125')
        self.label_text=["Email Address","Password"]
        self.user_ent=Entry(root)
        self.entries=[]
        for i in range(len(self.label_text)):
            self.l=Label(root,text=(self.label_text[i])).pack(side=TOP,fill=X)
            if i == 1:
                self.e=Entry(root,show='*',justify=CENTER)
                self.e.pack(side=TOP,fill=X)
                self.entries.append(self.e)
            else:
                self.e=Entry(root,justify=CENTER)
                self.e.pack(side=TOP,fill=X)
                self.entries.append(self.e)
        self.c1=Checkbutton(root, text="Remember Me",command=checkCommand).pack(side=LEFT)
        self.b1=Button(root, text="ENTER",command=enter).pack(side=RIGHT)

class newMail:
    def __init__(self, root):
        def Send():
            try:
                content=(self.textEntry.get(0.0,END))
                mail=smtplib.SMTP('smtp.gmail.com',587)
                mail.ehlo()
                mail.starttls()
                mail.login(user, passw)
                msg=MIMEMultipart()
                msg['From']=str(user)
                msg['To']=str(self.entries[0].get())
                msg['Subject']=str(self.entries[1].get())
                msg.attach(MIMEText(message,'plain'))
                mail.close()
            except:
                TimeoutError
                messagebox.showerror("Message Send","Unable to send message. Check your network.")
        self.root=root
        root.resizable(False,False)
        root.geometry('600x600')
        root.title('New Mail')
        self.label_text=["Recipient:","Subject:"]
        self.entries=[]
        for i in range(len(self.label_text)):
            self.l=Label(root,text=(self.label_text[i])).pack(side=TOP)
            self.e=Entry(root,justify=CENTER).pack(side=TOP,fill=X)
            self.entries.append(self.e)
        self.newmailmenu=Menu(root)
        self.newmailmenu.add_command(label="Send",command=Send)
        self.textEntry=Text(root,width=500,height=500)
        self.textEntry.pack()
        root.config(menu=self.newmailmenu)

def New():
    root_2=Tk()
    gui_2=newMail(root_2)
    root_2.mainloop()

class mainApp:
    def __init__(self, root):
        self.mail_button_list=[]
        self.message_list=[]
        def getPayload(x):
            self.textDisplay.delete(1.0,END)
            self.textDisplay.insert(END, x.get_payload(None))
        def retrieveMail():
            for i in range(len(self.mail_button_list)):
                self.mail_button_list[i].destroy()
            try:
                rv, data = self.mail.search(None, "All")
                if rv != "OK":
                    messagebox.showerror("Message Retrieval","Unable to retreive messages")
                i=int(0) #i must be used as a variable in the loop as num fails to work within the lambda command.
                for num in data[0].split():
                    rv, data= self.mail.fetch(num, "(RFC822)")
                    if rv != "OK":
                        messagebox.showerror("Message Retrieval","Error retrieving messages")
                    self.msg=email.message_from_bytes(data[0][1])
                    self.message_list.append(self.msg)          #i=i tells i to be retrieved as it is when declared, not after the loop.
                    self.b=Button(self.nst_frame, text=((num, self.msg["Subject"])),command=lambda i=i:getPayload(self.message_list[i]))
                    self.mail_button_list.append(self.b)
                    i+=1 #Incrementing i every time the loop develops
                for i in range(len(self.mail_button_list)):
                    self.mail_button_list[i].pack(side=TOP,fill=X)
            except:
                UnboundLocalError,imaplib.IMAP4.error
                messagebox.showerror("Message Retrieval","Unable to retrive messages.")

        self.root=root
        root.title('MailPy')
        root.geometry('720x600')
        root.resizable(False,False)
        root.iconbitmap('MailPy Logo.ico')
        self.mainmenu=Menu(root)
        self.menus=[]
        self.menuLabels=["File","Edit"] #Menu labels for mainmemnu bar
        self.subMenus=[['New','Login','retrieveMail'],
                       ['Preferences']]
        for i in range(len(self.menuLabels)):
            try:
                self.menux=Menu(self.mainmenu)
                for j in range(len(self.subMenus[i])):
                    try:
                            self.menux.add_command(label=str((self.subMenus[i])[j]),command=eval((self.subMenus[i])[j]))
                    except:
                        IndexError
                self.mainmenu.add_cascade(label=str(self.menuLabels[i]),menu=self.menux)
                self.menus.append(self.menux)
            except:
                IndexError
        root.config(menu=self.mainmenu)

        def configScroll(event):
            self.nst_canvas.configure(scrollregion=((self.nst_canvas).bbox(ALL)),width=335,height=540)

        #CREATING THE FRAME FOR VIEWING EMAIL CONTENT.
        self.viewframe=Frame(root,height=590,width=350,relief=GROOVE,bd=1)
        self.viewframe.pack(side=RIGHT)
        self.viewframe.pack_propagate(0) #Tells the frame not to let its children control its size.
        self.textDisplay=Text(self.viewframe,height=590)
        self.textDisplay.pack()

        self.mainframe=Frame(root,relief=GROOVE,width=265,height=600,bd=1)
        self.mainframe.pack(side=LEFT)
        self.nst_canvas=Canvas(self.mainframe,relief=GROOVE,bd=1,width=335)
        self.nst_frame=Frame(self.nst_canvas,width=335)
        self.scrollbar=Scrollbar(self.mainframe,orient=VERTICAL,command=self.nst_canvas.yview)
        self.nst_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        self.nst_canvas.pack(side=LEFT)
        self.nst_canvas.create_window((0,0),height=-1,width=335,window=self.nst_frame,anchor=NW)
        self.nst_frame.bind("<Configure>",configScroll) #Binding the nested frame to scrollbar.

        user=linecache.getline("UsrCrdn.txt", 1)
        passw=linecache.getline("UsrCrdn.txt",2)
        vet=True
        try:    #Attempting auto-login
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.mail.login(user,passw)
            self.mail.select("INBOX")
        except:     #Catching authentication error
            SMTPAuthenticationError #SPECIFIES THE AUTHENTICATION ERROR TO CATCH.
            messagebox.showerror("Authentication","Unable to login.\nCheck your Google security settings.")
            vet=False
        if vet==True:
            messagebox.showinfo('Login','User successfully logged in')
            retrieveMail()

root=Tk()
gui=mainApp(root)
root.mainloop()
