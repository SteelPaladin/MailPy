'''Created on 25 Apr 2017 - Latest Update: ~~ 13/03/18 ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NOTES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Develop auto-login. - DONE
'@' symbol not being recognised in hextable. Had this issue before, what do?
Does David remember?
@author: Harrison Baillie - SteelPaladin - www.github.com/SteelPaladin'''
from tkinter import *
from tkinter import messagebox
import imaplib, smtplib, email, linecache, os.path, binascii
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#List containing ASCII characters
alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','@']
#List containing hexadecimal variables.
hextable=['61','62','63','64','65','66','67','68','69','6A','6B','6C','6D','6E','6F','70','71','72','73','74','75','76','77','78','79','7A','40']

def hexEncrypt(passw):
    global alphabet, hextable
    try:
        newpass=['0x']
        for i in range(len(passw)):
            curval=passw[i]
            for j in range(len(alphabet)):
                if curval == alphabet[j]:
                    newpass.append(hextable[j])
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
    except:
        IndexError
    return (''.join(newpass))

'''
def hexEncrypt(passw):
    newpass=[]
    for i in passw:
        en = format(ord(i), "x")
        newpass.append(en)
        print(en)
    return (''.join(newpass))

def hexDecrypt(passw):
    newpass= ''
    for i in range(int(len(passw)/2)):
        de = re.findall(r'.{1,2}', passw, re.DOTALL)
    newpass = newpass+str(''.join(de))
    print(newpass)
    a = binascii.unhexlify(str(newpass.strip()))
    a = a.decode()
    print(a)
    return a'''


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Logon(username,password):
    '''username=gui_login.e.get()
    password=gui_login.e1.get()'''
    try:
        m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        m.login(username,password)
        m.select('"[Gmail]/All Mail"')
        check=True
    except:
        SMTPAuthenticationError
        check=False
    if check == False:
        return messagebox.showerror("Authentication","Unable to Login.")
    else:
        success=True
        gui_login.root.destroy()
        if rememberme == True:
            f=open('UsrCrdn.txt','w')
            f.write(hexEncrypt(username))
            f.write("\n")
            f.write(hexEncrypt(password))
            f.close()
        return messagebox.showinfo("Authentication","Logged In.")
    
def Login():
    global gui_login
    root_login=Tk()
    gui_login=LoginWindow(root_login)
    root_login.mainloop()

rememberme=False
def setRemember():
    global rememberme
    if rememberme == True:
        rememberme=False
    else:
        rememberme=True

class LoginWindow:
    def __init__(self, root):
        global username, password
        self.root=root
        root.title('MailPy - Login')
        #root.iconbitmap('MailPy Logo.ico')
        root.geometry('300x125')
        root.resizable(False, False)
        self.label_text=["Email Address","Password"]
        self.user_ent=Entry(root)
        self.entries=[]
        self.l=Label(root,text=(self.label_text[0])).pack(side=TOP,fill=X)
        
        self.e=Entry(root,justify=CENTER)
        self.e.pack(side=TOP,fill=X)
        self.l=Label(root,text=(self.label_text[1])).pack(side=TOP,fill=X)
        
        self.e1=Entry(root,show='*',justify=CENTER)
        self.e1.pack(side=TOP,fill=X)
        
        self.c1=Checkbutton(root, text="Remember Me",command=setRemember).pack(side=LEFT)
        #                                                Parsing logon function with entry windows as parameters
        self.b1=Button(root, text="ENTER", command=lambda:Logon(self.e1.get(),self.e2.get())).pack(side=RIGHT)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Compose():
    root= Tk()
    gui=newMail(root)
    root.mainloop()

class newMail:
    def __init__(self, root):
        def Send():
            self.content=(self.textEntry.get(0.0,END))
            self.msg=MIMEMultipart()
            self.msg['From']=username
            self.msg['To']=self.rec.get()
            self.msg['Subject']=self.sub.get()
            self.msg.attach(MIMEText(self.content,'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(username, password)
            text=self.msg.as_string()
            server.sendmail(username, self.rec.get(), text)
            server.quit()
            #messagebox.showerror("Sending","Unable to send message.")
        self.root=root
        root.resizable(False,False)
        root.geometry('600x600')
        root.title('New Mail')
        self.label_text=["Recipient:","Subject:"]
        
        self.reclabel=Label(root,text="Recipient:").pack(fill=X)
        self.rec=Entry(root,justify=CENTER)
        self.rec.pack(fill=X)
        self.sublabel=Label(root,text="Subject:").pack(fill=X)
        self.sub=Entry(root,justify=CENTER)
        self.sub.pack(fill=X)
        
        self.newmailmenu=Menu(root)
        self.newmailmenu.add_command(label="Send",command=Send)
        self.textEntry=Text(root,width=500,height=500)
        self.textEntry.pack()
        root.config(menu=self.newmailmenu)


class mainApp:
    def __init__(self, root):
        self.mail_button_list=[]
        self.message_list=[]
        def getPayload(x):
            self.textDisplay.delete(1.0,END)
            self.textDisplay.insert(END, x.get_payload(None))
        def retrieveMail():
            self.mail=imaplib.IMAP4_SSL('imap.gmail.com','993')
            self.mail.login(username,password)
            self.mail.select("INBOX")
            for i in range(len(self.mail_button_list)):
                self.mail_button_list[i].destroy()
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
            '''except:
                UnboundLocalError,imaplib.IMAP4.error
                messagebox.showerror("Message Retrieval","Unable to retrive messages.")'''

        self.root=root
        root.title('MailPy')
        root.geometry('720x600')
        root.resizable(False,False)
        #root.iconbitmap('MailPy Logo.ico')
        self.mainmenu=Menu(root)
        self.menus=[]
        self.menuLabels=["File","Edit","Mail"] #Menu labels for mainmemnu bar
        self.subMenus=[['Compose'],
                       [],
                       ['retrieveMail','Login']]
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
        Logon(user, passw) #Auto-Login attempt
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


root=Tk()
gui=mainApp(root)
root.mainloop()





















