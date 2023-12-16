import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address,port))
print("Client Connected!")

class Gui():
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400,height=300)
        self.pls=Label(self.login, text="Enter your name to login....", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.2)

        self.LabelName=Label(self.login, text="Name: ", font="Helvetica 12")
        self.LabelName.place(relheight=0.2, relx=0.1, rely=0.3)

        self.nameenter = Entry(self.login, font="Helvetica 10")
        self.nameenter.place(relheight=0.1, relx=0.35, rely=0.35, relwidth=0.5)
        self.nameenter.focus()

        self.go=Button(self.login, text="Login", font="Helvetica 7", command=lambda:self.goAhead(self.nameenter.get()))
        self.go.place(relheight=0.05, relwidth=0.25, relx=0.4, rely=0.7)

        self.window.mainloop()
    def chatwindow(self,name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chatroom")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=800, height=800, bg="black")
        self.labelHead = Label(self.window,bg="gray", fg="white", text="Welcome " + self.name, font="Helvetica 14", pady=20)
        self.labelHead.place(relwidth=1)
        self.line = Label(self.window, width=750, bg="white")
        self.line.place(relwidth=1, relheight=0.012, rely=0.07)
        self.textCons = Text(self.window, height=2, width=45, bg="gray", fg="white", padx=10, pady=10)
        self.textCons.place(relheight=0.75, relwidth=1, rely=0.08)
        self.labelBottom = Label(self.window, bg="black", height=160)
        self.labelBottom.place(relwidth=1, rely=0.825)
        self.entryMessage = Entry(self.labelBottom, bg="gray", fg="white", font="Helvetica 15")
        self.entryMessage.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMessage.focus()
        self.sendButton = Button(self.labelBottom, text="Send", font="Helvetica 17")
        self.sendButton.place(relx=0.77, rely=0.008, relheight= 0.06, relwidth=0.22)
        self.textCons.config(cursor="arrow")
        self.scrollbar = Scrollbar(self.textCons)
        self.scrollbar.place(relheight=1, relx=0.95)
        self.scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state= DISABLED)

    def sendButton(self, message):
        self.textCons.config(state= DISABLED)
        self.message = msg
        self.entryMessage.delete(0,END)
        send = Thread(target=self.write)
        send.start()
    def showMessage(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
    def goAhead(self,name):
        self.login.destroy()
        self.chatwindow(name)
        rcv = Thread(target=self.receive)
        rcv.start()
    def receive(self):
        while True:
            try:
                message=client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMessage(message)
            except:
                print("An Error Occured! ")
                client.close()
                break

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message=(f"{self.name} : {self.msg}")
            client.send(message.encode('utf-8'))
            self.showMessage(message)
            break
chatapp = Gui()