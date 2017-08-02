'''Created on 25 Apr 2017
@author: Harrison Baillie - SteelPaladin'''
from tkinter import * #IMPORTING THE TKINTER GUI MODULE
import imaplib, smtplib, email, linecache #IMPORTING NETWORKING MODULES & MODULES TO READ SPECIFIC LINES
from smtplib import SMTPAuthenticationError
global prefwindowopen
prefwindowopen=False

#FUNCTION THAT LOGS INTO THE GMAIL SERVER
def Login():
    root_3=Tk()
    gui_3=logonWindow(root_3)
    root_3.mainloop()
        
def Preferences():
    root_4=Tk()
    gui_4=preferencesWindow(root_4)
    root_4.mainloop()
    
class errorWindow:
    def __init__(self, root):
        def destroy():
            self.root.destroy()
        self.root=root
        root.title("ERROR")
        root.iconbitmap('MailPy Logo.ico')
        root.geometry('300x200')
        root.resizable(False,False)
        self.text=Text(root,width=300,height=200)
        self.desButton=Button(root,text="OK",command=destroy)
        self.desButton.pack(side=BOTTOM,fill=X)
        self.text.pack()

class preferencesWindow:
    def __init__(self, root):
        self.root=root
        root.title("MailPy - Preferences")
        root.iconbitmap('MailPy Logo.ico')
        root.geometry('400x420')
        root.resizable(False,False)

class logonWindow:
    def __init__(self, root):
        global checkvariable
        checkvariable=False
        def enter():
            global user, passw
            user=str(self.e1.get())
            passw=str(self.e2.get())
            if checkvariable == True:
                usercredentials=open("UsrCrdn.txt","w")
                usercredentials.write(str(self.e1.get()+"\n")) #STORING THE USERS EMAIL ADDRESS
                usercredentials.write(str(self.e2.get()+"\n")) #STORING THE USERS PASSWORD
                usercredentials.close()
            try:    #ATTEMPTS TO LOGIN TO THE GMAIL SERVER WITH THE ENTERED CREDENTIALS
                mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
                mail.login(user,passw)
                mail.select("INBOX")
            except:     #CATCHES AN AUTHENTICATION ERROR TO STOP THE PROGRAM CRASHING.
                SMTPAuthenticationError #SPECIFIES THE AUTHENTICATION ERROR TO CATCH.
                root_5=Tk() #CREATES AN ERROR MESSAGE
                gui_5=errorWindow(root_5)
                gui_5.text.insert(END, "Unable to login.")  #SPECIFIES THE ERROR MESSAGE TO MATCH THE ERROR.
                root_5.mainloop()
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
        #ENTRY WIDGET TO ENTER USER'S EMAIL ADDRESS
        self.l1=Label(root,text="Email Address:").pack(side=TOP,fill=X)
        self.e1=Entry(root)
        self.e1.pack(side=TOP,fill=X)
        #ENTRY WIDGET TO ENTER USER'S PASSWORD
        self.l2=Label(root,text="Password:").pack(side=TOP,fill=X)
        self.e2=Entry(root)
        self.e2.pack(side=TOP,fill=X)
        #CREATES A 'Remember Me' OPTION FOR THE PROGRAM TO MEMORISE THE USER'S CREDENTIALS
        self.c1=Checkbutton(root, text="Remember Me",command=checkCommand).pack(side=LEFT)
        self.b1=Button(root, text="ENTER",command=enter).pack(side=RIGHT)

class newMail:
    def __init__(self, root):
        def Send():
            content=(self.textEntry.get(0.0,END))
            mail=smtplib.SMTP('smtp.gmail.com',587, timeout=120)
            mail.ehlo()
            mail.starttls()
            mail.login(user, passw)
            mail.sendmail(user,(self.recipient.get()),(self.textEntry).get())
            mail.close()
        self.root=root
        root.title("New Mail")
        root.iconbitmap('MailPy Logo.ico')
        root.geometry('500x500')
        root.resizable(False,False)
        self.l1=Label(root, text="Recipient:").pack(side=TOP)
        self.recipient=Entry(root).pack()
        self.l2=Label(root, text="Subject:").pack(side=TOP)
        self.subject=Entry(root).pack()
        self.newmailmenu=Menu(root)
        self.newmailmenu.add_command(label="Send",command=Send)
        self.textEntry=Text(root,width=500,height=500)
        self.textEntry.pack()
        root.config(menu=self.newmailmenu)

def New():
    root_2=Tk()
    gui_2=newMail(root_2)
    root_2.mainloop()

#CREATING A CLASS FOR THE MAIN APP WINDOW
class mainApp:
    def __init__(self, root):
        self.mail_button_list=[]
        #FUNCTION TO RETRIEVE ALL MAIL FROM USER'S INBOX
        def retrieveMail():
            #LOOP WHICH DESTROYS ALL CURRENTLY DISPLAYED EMAILS WITHIN THE FRAME
            for i in range(len(self.mail_button_list)):
                self.mail_button_list[i].destroy()
            rv, data = self.mail.search(None, "All")
            if rv != "OK":
                root_5=Tk()
                gui_5=errorWindow(root_5)
                gui_5.text.insert(END, "Unable to retrieve messages.")
                root_5.mainloop()
            for num in data[0].split():
                rv, data= self.mail.fetch(num, "(RFC822)")
                if rv != "OK":
                    root_5=Tk()
                    gui_5=errorWindow(root_5)
                    gui_5.text.insert(END, "Error retrieving messages.")
                    root_5.mainloop()
                self.msg=email.message_from_bytes(data[0][1])
                self.b=Button(self.nst_frame, text=str((num, self.msg["Subject"])))
                self.mail_button_list.append(self.b)
                self.b.pack(side=TOP,fill=X)
                
        self.root=root
        root.title('MailPy')
        root.geometry('720x600')
        root.resizable(False,False)
        root.iconbitmap('MailPy Logo.ico')
        #CREATING A MENU BAR
        self.mainmenu=Menu(root)
        self.menus=[]
        self.menuLabels=["File","Edit"] #MENU LABELS FOR THE MENU BAR
        for i in range(len(self.menuLabels)): #FOR LOOP WHICH ASSIGNS THE LABEL TO THE MENU BAR
            menux=Menu(self.mainmenu) #CREATES A PLACEHOLDER MENU OPTION
            self.mainmenu.add_cascade(label=str(self.menuLabels[i]),menu=menux)
            self.menus.append(menux) #ASSIGNING THE PLACEHOLDER AS AN OBJECT INTO A LIST FOR FUTURE REFERENCE.
        self.fileOptions=["New","Login","retrieveMail"] #LIST OF ITEMS TO BE PUT IN THE File CASCADE
        for i in range(len(self.fileOptions)):
            self.menus[0].add_command(label=str(self.fileOptions[i]),command=eval(self.fileOptions[i]))
        self.editOptions=["Preferences"] #LIST OF ITEMS TO BE PUT IN THE Edit CASCADE
        for i in range(len(self.editOptions)):
            self.menus[1].add_command(label=str(self.editOptions[i]),command=eval(self.editOptions[i]))
        root.config(menu=self.mainmenu) #CONFIGURING THE GUI TO RECOGNISE THE MENU BAR.

        #FUNCTION TO CONFIGURE THE WINDOW SCROLLBAR
        def configScroll(event):
            self.nst_canvas.configure(scrollregion=((self.nst_canvas).bbox(ALL)),width=335,height=540)
                
        #CREATING THE FRAME FOR VIEWING EMAIL CONTENT.
        self.viewframe=Frame(root,height=590,width=335,relief=GROOVE,bd=1)
        self.viewframe.pack(side=RIGHT)
        
        #CREATING THE FRAME TO LIST RECEIVED EMAILS
        self.mainframe=Frame(root,relief=GROOVE,width=350,height=710,bd=1)
        self.mainframe.pack(side=LEFT)
        self.nst_canvas=Canvas(self.mainframe,relief=GROOVE,bd=1,width=335)
        self.nst_frame=Frame(self.nst_canvas,width=335)
        #CREATING A SCROLLBAR
        self.scrollbar=Scrollbar(self.mainframe,orient=VERTICAL,command=self.nst_canvas.yview)
        self.nst_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT,fill=Y)
        
        self.nst_canvas.pack(side=LEFT)
        self.nst_canvas.create_window((0,0),height=-1,width=335,window=self.nst_frame,anchor=NW)
        
        self.nst_frame.bind("<Configure>",configScroll)
        #CREATING 30 BUTTONS AS TEST EMAILS FOR DEBUGGING.
        
        user=linecache.getline("UsrCrdn.txt", 1)
        passw=linecache.getline("UsrCrdn.txt",2)
        try:    #ATTEMPTS TO LOGIN TO THE GMAIL SERVER WITH THE ENTERED CREDENTIALS
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.mail.login(user,passw)
            self.mail.select("INBOX")
        except:     #CATCHES AN AUTHENTICATION ERROR TO STOP THE PROGRAM CRASHING.
            SMTPAuthenticationError #SPECIFIES THE AUTHENTICATION ERROR TO CATCH.
            root_5=Tk() #CREATES AN ERROR MESSAGE WINDOW
            gui_5=errorWindow(root_5)
            gui_5.text.insert(END, "Unable to login.\nCheck your Google security settings.")  #SPECIFIES THE ERROR MESSAGE TO MATCH THE ERROR.
            root_5.mainloop()
        retrieveMail()

root=Tk()
gui=mainApp(root)
root.mainloop()