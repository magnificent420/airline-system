from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import tkinter.messagebox as message
from gtts import gTTS
import pygame
import os 
import random
import subprocess
conn=sqlite3.connect("airline.db")
cur=conn.cursor()
# flights
cur.execute(''' CREATE TABLE IF NOT EXISTS flights(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   flight_number VARCHAR NOT NULL,
   origin VARCHAR NOT NULL,
   destination VARCHAR NOT NULL,
   departure_time VARCHAR NOT NULL,
   arrival_time VARCHAR NOT NULL        

)''')
# passengers
cur.execute(''' CREATE TABLE IF NOT EXISTS passengers(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name VARCHAR NOT NULL,
   gender VARCHAR NOT NULL,
   age VARCHAR NOT NULL,
   passport_number VARCHAR NOT NULL,
   contact VARCHAR NOT NULL       

)''')
# bookings
cur.execute(''' CREATE TABLE IF NOT EXISTS bookings(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   passenger_id INTEGER NOT NULL,
   flight_id INTEGER NOT NULL,
   age VARCHAR NOT NULL,
   seat_number VARCHAR NOT NULL,
   FOREIGN KEY(passenger_id) REFERENCES passengers(id),        
   FOREIGN KEY(flight_id) REFERENCES flights(id)        

)''')
admin=Tk()
admin.config(bg="#5e546e")
admin.geometry('1000x500+200+0')
admin.title("Admin Dashboard")
admin.resizable(0,0)
# spath="images/dash.jpg"
# simg=ImageTk.PhotoImage(Image.open(spath))
# img=Label(admin,image=simg, bg="#5e546e", width=300, height=100)
# img.image=simg
# img.place(x=0,y=0)
spath="images/airline.jpg"
simg1=ImageTk.PhotoImage(Image.open(spath))
img1=Label(admin,image=simg1, bg="#5e546e")
img1.image=simg1
img1.place(x=0,y=100)
def text_to_speech(text):
  tts=gTTS(text=text, lang='en')
  audio_file="flight_info.mp3"
  tts.save(audio_file)
  pygame.mixer.init()
  pygame.mixer.music.load(audio_file)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
     continue
  pygame.mixer.quit()
  os.remove(audio_file)


def add():
    flight_number=entf.get()
    origin=ento.get()
    departure_time=entd.get()
    arrival_time=enta.get()
    destination=entds.get()
    if flight_number and origin and destination and departure_time and arrival_time:
        conn=sqlite3.connect("airline.db")
        cur=conn.cursor()

        cur.execute(''' INSERT INTO flights(flight_number, origin, destination, departure_time, arrival_time) VALUES (?,?,?,?,?)''' ,(flight_number,origin,destination,departure_time,arrival_time))
        conn.commit()
        conn.close()
        message.showinfo("success","Flight added successfully")
        flight_info=f"Flight {flight_number}from {origin} to {destination} has been successfully added. Departure at {departure_time} and arrival at{arrival_time}."
# text_to_speech method
        text_to_speech(flight_info)
        entf.delete(0,END)
        ento.delete(0,END)
        entd.delete(0,END)
        entds.delete(0,END)
        enta.delete(0,END)
    else:
       message.showinfo("Alert", "please fill the form above")



def search():
   flight_number=entf.get()

   if flight_number:
      conn=sqlite3.connect('airline.db')
      cur=conn.cursor()
      cur.execute(''' SELECT flight_number, origin,destination,departure_time,arrival_time from flights WHERE flight_number=?
                  ''',(flight_number,))
      result=cur.fetchone()
      conn.close()
      if result:
         ento.insert(0,result[1])
         entd.insert(0,result[2])
         entds.insert(0,result[3])
         enta.insert(0,result[4])
         flight_info=f"flight{result[0]} from {result[1]} to {result[2]} depart at {result[3]} and arrive at {result[4]}."
         text_to_speech(flight_info)
      else:
         message.showinfo("Not Found", "No flight found with that flight number please ensure you book a flight")
   else:
    message.showinfo("Alert", "please enter a flight number to search")
def delete():
   flight_number=entf.get()
   if flight_number:
      conn=sqlite3.connect('airline.db')
      cur=conn.cursor()
      cur.execute(''' DELETE from  flights WHERE flight_number=?
                  ''',(flight_number,))
      conn.commit()
      conn.close()
      if cur.rowcount:
         message.showinfo('success','flight successfully deleted')
      else:
         message.showinfo('Alert', "flight number is not found")
   else:
      message.showinfo('Alert', "please enter a flight number to delete")
def update():
   flight_number=entf.get()
   origin=ento.get()
   destination=entds.get()
   departure_time=entd.get()
   arrival_time=enta.get()
   if flight_number and origin and destination and departure_time and arrival_time:
      conn=sqlite3.connect('airline.db') 
      cur=conn.cursor()
      cur.execute(''' update flights
                  set origin=?, destination=?,departure_time=?, arrival_time=?
                  where flight_number=?
                   ''',(origin,destination,departure_time,arrival_time,flight_number))
      conn.commit()
      conn.close()
      if cur.rowcount:
         message.showinfo('success','flight successfully updated')
      else:
         message.showinfo('Alert', "flight number is not found")
   else:
      message.showinfo('Alert', "please enter a flight number to update")
      flight_info=f"Flight {flight_number}from {origin} to {destination} has been successfully added. Departure at {departure_time} and arrival at{arrival_time}."
# text_to_speech method
      text_to_speech(flight_info)
      entf.update(0,END)
      ento.update(0,END)
      entd.update(0,END)
      entds.update(0,END)
      enta.update(0,END)
def user():
   subprocess.Popen(["python", "user.py"])

# lbl=Label(admin, text="Admin Panel", font=("sanserif",50, "bold"), bg="#5e546e", fg="#fff", underline=6, )
# lbl.place(x=20,y=0)
lbluser=Label(admin, text="click the button below to access user dashboard", font=("sanserif",12), bg="#5e546e", fg="red",)
lbluser.place(x=20,y=80)
btnuser=Button(admin,text="click me", bg="gray", fg="white", border=0, command=user)
btnuser.place(x=200,y=100)


lbl=Label(admin, text="Admin Panel", font=("sanserif",50, "bold"), bg="#5e546e", fg="#fff", underline=6, )
lbl.place(x=0,y=0)
right_frame=Frame(admin,width=500,height=1000, bg="gray")
l1=Label(right_frame, text="Flight Number:", font=("sanserif",12, "bold"), bg="gray", fg="white")
l1.place(x=50, y=100)
entf=Entry(right_frame, width=50)
entf.place(x=180, y=100)
right_frame.pack(side="right")

l2=Label(right_frame, text="Origin:", font=("sanserif",12, "bold"), bg="gray", fg="white")
l2.place(x=50, y=130)
ento=Entry(right_frame, width=50)
ento.place(x=180, y=130)
right_frame.pack(side="right")

l3=Label(right_frame, text="Departure Time:", font=("sanserif",12, "bold"), bg="gray", fg="white")
l3.place(x=50, y=160)
entd=Entry(right_frame, width=50)
entd.place(x=180, y=160)
right_frame.pack(side="right")

l4=Label(right_frame, text="Arrival Time:", font=("sanserif",12, "bold"), bg="gray", fg="white")
l4.place(x=50, y=190)
enta=Entry(right_frame, width=50,disabledbackground="gray")
enta.place(x=180, y=190)
right_frame.pack(side="right")

l5=Label(right_frame, text="Destination:", font=("sanserif",12, "bold"), bg="gray", fg="white")
l5.place(x=50, y=220)
entds=Entry(right_frame, width=50)
entds.place(x=180, y=220)
right_frame.pack(side="right")

btnadd=Button(right_frame, text="Add Flight", font=("sanserif",14, "bold"),fg="white", bg="black", command=add)
btnadd.place(x=180, y=250)

btnsearch=Button(right_frame,text="Search Flight", font=("sanserif",14, "bold"),fg="white", bg="black", command=search)
btnsearch.place(x=300, y=250)

btnupdate=Button(right_frame,text="Update Flight", font=("sanserif",14, "bold"),fg="white", bg="black",command=add)
btnupdate.place(x=180, y=300)

btndelete=Button(right_frame,text="Delete Flight", font=("sanserif",14, "bold"),fg="white", bg="red",command=delete)
btndelete.place(x=320, y=300)
right_frame.pack(side="right")

btnclose=Button(right_frame,text="close APP", font=("sanserif",14, "bold"),fg="white", bg="red",command=admin.destroy)
btnclose.place(x=320, y=350)
right_frame.pack(side="right")

admin.mainloop()