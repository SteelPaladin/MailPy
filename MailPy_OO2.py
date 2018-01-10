'''Created on 25 Apr 2017 - Latest Update: ~~ 01/12/17 ~~
@author: Harrison Baillie - SteelPaladin'''
from tkinter import *
from tkinter import messagebox
import imaplib, smtplib, email, linecache
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

hextable = ['41','42','43','44','45','46','47','48','49','4A','4B','4C','4D',
            '4E','4F','50','51','52','53','54','55','56','57','58','59','5A',
            '61','62','63','64','65','66','67','68','69','6A','6B','6C','6D','6E',
            '6F','70','71','72','73','74','75','76','77','78','79','7A','40']
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            'a','b','c','d','e','f','g','h','i','j','k','l','m',
            'n','o','p','q','r','s','t','u','v','w','x','y','z','@']

#Encryption/Decryption working, for some reason the @/40 character is not being recognised in either one, or both of these processes.

def hexEncrypt(passw):
    try:
        newpass=['0x']
        for i in range(len(passw)):
            curval=passw[i]
            print("RUNNING",curval)
            for j in range(len(alphabet)):
                if curval == alphabet[j]:
                    newpass.append(hextable[j])
                    print(hextable[j])
    except:
        IndexError
    return (''.join(newpass))

def hexDecrypt(passw):
    try:
        newpass=[]
        for i in range(len(passw)):
            #I don't even know what the fuck happened here.
            if i == 0:
                curval=str((passw[i])+(passw[i+1]))
            else:
                curval=str((passw[i*2])+(passw[(i*2)+1]))
            for j in range(len(hextable)):
                if curval == hextable[j]:
                    newpass.append(alphabet[j])
                    print(alphabet[j])
    except:
        IndexError
    return (''.join(newpass))


def changeServer(domain):
    global domain_name #Globalising the domain name variable
    domain_name=domain
    f=open('UsrCrdn.txt','w').close() #Wiping current user data
    messagebox.showinfo("Server Change", ("You have altered your server domain to,",domain_name,".\nPlease log in again."))

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
                usercredentials.write(hexEncrypt(str(self.entries[0].get())))
                usercredentials.write("\n")
                usercredentials.write(hexEncrypt(str(self.entries[1].get())))
                usercredentials.close()
            self.vet=True
            try:
                mail = imaplib.IMAP4_SSL(domain_name, '993')
                mail.login(user,passw)
                mail.select("INBOX")
            except:
                SMTPAuthenticationError
                messagebox.showerror("Authentication","Vet Failed.\nUnable to Login.")
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
                mail=smtplib.SMTP(domain_name,'587')
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
        self.menuLabels=["File","Edit","Mail"] #Menu labels for mainmemnu bar
        self.subMenus=[['New','Login'],
                       ['MailServer'],
                       ['retrieveMail']]
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
        self.servermenu=Menu(self.mainmenu)
        self.servermenu.add_command(label='Gmail',command=lambda:changeServer('smtp.gmail.com'))
        self.servermenu.add_command(label='Hotmail',command=lambda:changeServer('smtp.live.com')) #Lambdas are used here to allowfor parameter parsing
        self.menus[2].add_cascade(label='Mail Servers',menu=self.servermenu) #Adding a secondary cascade to the MailServers option

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
        #~~~~~~~~~~~~~~~~~~~~Hexadecimal Cipher~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        user=hexDecrypt(linecache.getline("UsrCrdn.txt", 1))
        passw=hexDecrypt(linecache.getline("UsrCrdn.txt",2))
        print(user,passw)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        vet=True
        try:    #Attempting auto-login
            self.mail = imaplib.IMAP4_SSL(domain_name, '993')
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
