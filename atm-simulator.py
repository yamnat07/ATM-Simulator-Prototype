from tkinter import *
import re,json,csv,os
from datetime import datetime,timedelta
from PIL import Image, ImageTk
from tkinter import messagebox
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("customers.json","r") as file:
    data=json.load(file)

window=Tk()
window.title("ATM Simulator")
window.geometry("800x500")
window.resizable(False,False)
img=Image.open("bank_logo_supreme.png").resize((580,500))
bg=ImageTk.PhotoImage(img)
screen=Canvas(window,width=800,height=500,highlightthickness=0,bg="white")
screen.pack()
screen.image=bg
small=ImageTk.PhotoImage(Image.open("bank_logo_supreme.png").resize((190,109)))
screen.small=small

def csv_save(info):
    with open("log.csv","a",newline="") as file:
        writer=csv.writer(file)
        writer.writerow(info)
def date_time():
    dt=datetime.now()
    da=dt.date().strftime("%d-%B-%Y")
    ti=dt.time().strftime("%I:%M:%S %p")
    return da,ti
def save(data):
    with open("customers.tmp","w") as file:
        json.dump(data,file,indent=4)
    os.replace("customers.tmp","customers.json")
def clear():
    screen.delete("all")
    for w in page_widgets:
        w.destroy()
    screen.create_image(400,70,image=small)

def withdraw():
    clear()
    screen.create_text(280,170,text="Account No.:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    acc_widget=Entry(screen,font=("arial",20),justify="center")
    acc_widget.place(x=290,y=150,width=240,height=40)
    
    screen.create_text(280,250,text="PIN:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    pin_widget=Entry(screen,font=("arial",20),justify="center",show="*")
    pin_widget.place(x=290,y=230,width=240,height=40)
    
    screen.create_text(280,330,text="Amount (₹):",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    amt_widget=Entry(screen,font=("arial",20),justify="center")
    amt_widget.place(x=290,y=310,width=240,height=40)
    amount_pattern=r"[0-9]+(\.[0-9]{1,2})?"
    def confirm():
        acc=acc_widget.get()
        pin=pin_widget.get()
        amt=amt_widget.get()
        if not acc and not pin and not amt:
            messagebox.showwarning("Warning","Please Fill all the fields!")
        elif not acc:
            messagebox.showwarning("Warning","Please Fill the Account No. field!")
        elif not pin:
            messagebox.showwarning("Warning","Please Fill the Pin field!")
        elif not amt:
            messagebox.showwarning("Warning","Please Fill the Amount field!")
        elif acc not in data:
            messagebox.showwarning("Warning","Incorrect Account Number!")
        elif pin!=data[acc]["pin"]:
            messagebox.showwarning("Warning","Incorrect Pin Entered!")
        elif not re.fullmatch(amount_pattern,amt) or float(amt)==0:
            messagebox.showwarning("Warning","Enter a valid amount to withdraw!")
        elif float(amt)>data[acc]["balance"]:
            messagebox.showinfo("Balance Not Sufficient",f"Available Balance:{data[acc]["balance"]:,.2f}")
        else:
            final_amt=float(amt)
            messagebox.showinfo("Transaction in process","Please wait while your Transaction is being Processed!")
            data[acc]["balance"]=round(data[acc]["balance"]-final_amt,2)
            save(data)
            date,Time=date_time()
            info=[date,Time,f"Account No.:{acc}",f"Money Withdrawn:{final_amt}"]
            csv_save(info)
            time.sleep(5)
            messagebox.showinfo("Success",f"Transaction Completed!\nBalance Remaining:₹{data[acc]["balance"]:,.2f}")
            screen.delete("text")
            acc_widget.destroy()
            pin_widget.destroy()
            amt_widget.destroy()
            ok_bttn.destroy()
            screen.delete("all")
            page_widgets[:]=list(main())
    ok_bttn=Button(screen,text="Confirm",font=("arial",14,"bold"),fg="white",bg="#003893",
        activeforeground="white",activebackground="#FF7A00",command=confirm)
    ok_bttn.place(x=290,y=395,width=110,height=40)

def deposit():
    clear()
    screen.create_text(280,170,text="Account No.:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    acc_widget=Entry(screen,font=("arial",20),justify="center")
    acc_widget.place(x=290,y=150,width=240,height=40)
    
    screen.create_text(280,250,text="PIN:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    pin_widget=Entry(screen,font=("arial",20),justify="center",show="*")
    pin_widget.place(x=290,y=230,width=240,height=40)
    
    screen.create_text(280,330,text="Amount (₹):",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    amt_widget=Entry(screen,font=("arial",20),justify="center")
    amt_widget.place(x=290,y=310,width=240,height=40)
    amount_pattern=r"[0-9]+(\.[0-9]{1,2})?"
    def confirm():
        acc=acc_widget.get()
        pin=pin_widget.get()
        amt=amt_widget.get()
        if not acc and not pin and not amt:
            messagebox.showwarning("Warning","Please Fill all the fields!")
        elif not acc:
            messagebox.showwarning("Warning","Please Fill the Account No. field!")
        elif not pin:
            messagebox.showwarning("Warning","Please Fill the Pin field!")
        elif not amt:
            messagebox.showwarning("Warning","Please Fill the Amount field!")
        elif acc not in data:
            messagebox.showwarning("Warning","Incorrect Account Number!")
        elif pin!=data[acc]["pin"]:
            messagebox.showwarning("Warning","Incorrect Pin Entered!")
        elif not re.fullmatch(amount_pattern,amt) or float(amt)==0:
            messagebox.showwarning("Warning","Enter a valid amount to deposit!")
        else:
            final_amt=float(amt)
            messagebox.showinfo("Transaction in process","Please wait while your Transaction is being Processed!")
            data[acc]["balance"]=round(data[acc]["balance"]+final_amt,2)
            save(data)
            date,Time=date_time()
            info=[date,Time,f"Account No.:{acc}",f"Money Deposited:{final_amt}"]
            csv_save(info)
            time.sleep(5)
            messagebox.showinfo("Success",f"Transaction Completed!\nUpdated Balance:₹{data[acc]["balance"]:,.2f}")
            screen.delete("text")
            acc_widget.destroy()
            pin_widget.destroy()
            amt_widget.destroy()
            ok_bttn.destroy()
            screen.delete("all")
            page_widgets[:]=list(main())
    ok_bttn=Button(screen,text="Confirm",font=("arial",14,"bold"),fg="white",bg="#003893",
        activeforeground="white",activebackground="#FF7A00",command=confirm)
    ok_bttn.place(x=290,y=395,width=110,height=40)

def check_balance():
    clear()
    screen.create_text(280,170,text="Account No.:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    acc_widget=Entry(screen,font=("arial",20),justify="center")
    acc_widget.place(x=290,y=150,width=240,height=40)
        
    screen.create_text(280,250,text="PIN:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    pin_widget=Entry(screen,font=("arial",20),justify="center",show="*")
    pin_widget.place(x=290,y=230,width=240,height=40)
    def confirm():
            acc=acc_widget.get()
            pin=pin_widget.get()
            if not acc and not pin:
                messagebox.showwarning("Warning","Please Fill all the fields!")
            elif not acc:
                messagebox.showwarning("Warning","Please Fill the Account No. field!")
            elif not pin:
                messagebox.showwarning("Warning","Please Fill the Pin field!")
            elif acc not in data:
                messagebox.showwarning("Warning","Incorrect Account Number!")
            elif pin!=data[acc]["pin"]:
                messagebox.showwarning("Warning","Incorrect Pin Entered!")
            else:
                messagebox.showinfo("Processing","Please Wait while the operation is under Process!")
                date,Time=date_time()
                info=[date,Time,f"Account No.:{acc}","Checked Balance"]
                csv_save(info)
                time.sleep(5)
                messagebox.showinfo("Amount Balance Fetched",f"Available Balance:₹{data[acc]["balance"]:,.2f}")
                screen.delete("text")
                acc_widget.destroy()
                pin_widget.destroy()
                ok_bttn.destroy()
                screen.delete("all")
                page_widgets[:]=list(main())
    ok_bttn=Button(screen,text="Confirm",font=("arial",14,"bold"),fg="white",bg="#003893",
            activeforeground="white",activebackground="#FF7A00",command=confirm)
    ok_bttn.place(x=290,y=395,width=110,height=40)

def change_pin():
    clear()
    screen.create_text(280,140,text="Account No.:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    acc_widget=Entry(screen,font=("arial",20),justify="center")
    acc_widget.place(x=290,y=120,width=240,height=40)
            
    screen.create_text(270,220,text="Old PIN:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    pin_widget=Entry(screen,font=("arial",20),justify="center",show="*")
    pin_widget.place(x=290,y=200,width=240,height=40)

    screen.create_text(270,300,text="New PIN:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    new_pin_widget=Entry(screen,font=("arial",20),justify="center",show="*")
    new_pin_widget.place(x=290,y=280,width=240,height=40)

    screen.create_text(270,380,text="Confirm New PIN:",font=("arial",16,"bold"),fill="#0a1f4e",anchor="e",tags="text")
    cnf_pin_widget=Entry(screen,font=("arial",20),justify="center",show="*")
    cnf_pin_widget.place(x=290,y=360,width=240,height=40)
    pin_pattern=r"[0-9]{4}"
    def confirm():
        acc=acc_widget.get()
        pin=pin_widget.get()
        new_pin=new_pin_widget.get()
        new_pin_cnf=cnf_pin_widget.get()
        if not acc and not pin and not new_pin and not new_pin_cnf:
            messagebox.showwarning("Warning","Please Fill all the fields!")
        elif not acc:
            messagebox.showwarning("Warning","Please Fill the Account No. field!")
        elif not pin:
            messagebox.showwarning("Warning","Please Fill the Pin field!")
        elif acc not in data:
            messagebox.showwarning("Warning","Incorrect Account Number!")
        elif pin!=data[acc]["pin"]:
            messagebox.showwarning("Warning","Incorrect Old Pin Entered!")
        elif not re.fullmatch(pin_pattern,new_pin) or not re.fullmatch(pin_pattern,new_pin_cnf) or not (re.fullmatch(pin_pattern,new_pin) and re.fullmatch(pin_pattern,new_pin_cnf)):
            messagebox.showwarning("Warning","Please enter a 4 Digit PIN in both New and Confirm PIN fields!")
        elif new_pin==new_pin_cnf==pin:
            messagebox.showwarning("Warning","Please Enter a unique pin different from current PIN!")
        elif new_pin!=new_pin_cnf:
            messagebox.showwarning("Warning","The new PIN and the Confirmed PIN must be same!")
        else:
            messagebox.showinfo("Processing","Please Wait while the operation is under Process!")
            data[acc]["pin"]=new_pin
            save(data)
            date,Time=date_time()
            info=[date,Time,f"Account No.:{acc}","PIN Changed"]
            csv_save(info)
            time.sleep(5)
            messagebox.showinfo("PIN changed","Your current PIN has been changed successfully!")
            screen.delete("text")
            acc_widget.destroy()
            pin_widget.destroy()
            ok_bttn.destroy()
            new_pin_widget.destroy()
            cnf_pin_widget.destroy()
            screen.delete("all")
            page_widgets[:]=list(main())
    ok_bttn=Button(screen,text="Confirm",font=("arial",14,"bold"),fg="white",bg="#003893",
                activeforeground="white",activebackground="#FF7A00",command=confirm)
    ok_bttn.place(x=290,y=430,width=110,height=40)
def main():
    screen.create_image(0,0,image=bg,anchor="nw")
    with_bttn=Button(screen,text="Withdraw",font=("arial",20,"bold"),fg="white",bg="red"
        ,activeforeground="black",activebackground="green",command=withdraw)
    with_bttn.place(x=581,y=0,width=220,height=60)

    depo_bttn=Button(screen,text="Deposit",font=("arial",20,"bold"),fg="white",bg="red"
        ,activeforeground="black",activebackground="green",command=deposit)
    depo_bttn.place(x=581,y=61,width=220,height=60)

    bala_bttn=Button(screen,text="Check Balance",font=("arial",20,"bold"),fg="white",bg="red"
        ,activeforeground="black",activebackground="green",command=check_balance)
    bala_bttn.place(x=581,y=122,width=220,height=60)

    pin_change_bttn=Button(screen,text="Change PIN",font=("arial",20,"bold"),fg="white",bg="red"
        ,activeforeground="black",activebackground="green",command=change_pin)
    pin_change_bttn.place(x=581,y=183,width=220,height=60)
    return with_bttn,pin_change_bttn,bala_bttn,depo_bttn
page_widgets=list(main())
window.mainloop()