#!/usr/bin/python
# coding=utf-8
'''The MIT License (MIT)

Copyright (c) 2015 Revathy Narayanan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. '''

import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from datetime import datetime
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
import kivy.core.text.markup
from kivy.properties import BooleanProperty
from kivy.uix.dropdown import DropDown
from kivy.graphics import BorderImage
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import csv
import sqlite3 as lite
import sys
import re
import smtplib
import os
import sys


class MyApp(FloatLayout):
	""" Creates a Float Layout with  widgets and methods necessary
	    for the Time Tracker application . """


	def __init__(self, **kwargs):
		super(MyApp,self).__init__(**kwargs)
		Window.size = (480, 640)
		with self.canvas:
			BorderImage(border=(10, 10, 10,10),source='time.jpg',size=(480,640))
		global btn1
		btn1 = ToggleButton(text=' START ', bold=True,group='state', size_hint=(.25,.022),
							pos=(190,380),border=(40,0,40,0))
		btn1.bind(on_press=MyApp.start_timer)
		global btn2
		btn2 = ToggleButton(text='LOG TASK', group='state', size_hint=(.25,.012),
							pos=(20,50),disabled=True,border=(20,0,20,0))
		btn2.bind(on_press=MyApp.comment_pop)
		btn3 = Button(text='VIEW TIMESHEET',size_hint=(.29,.012),pos=(335,50),
					  border=(20,0,20,0))
		btn3.bind(on_press=MyApp.timesheet_pop)
		btn4 = Button(text='MAIL TIMESHEET', group='state', size_hint=(.29,.012),
					  pos=(335,550),border=(20,0,20,0))
		btn4.bind(on_press=MyApp.mail_pop)
		btn5 = Button(text='READ ME', group='state', size_hint=(.25,.012),
					  pos=(20,550),border=(20,0,20,0))
		btn5.bind(on_press=MyApp.readme_pop)
		global l1
		l1 = Label (bold=True)
		self.add_widget(btn1)
		self.add_widget(btn2)
		self.add_widget(btn3)
		self.add_widget(btn4)
		self.add_widget(btn5)
		self.add_widget(l1)



	def start_timer(instance):
		""" Adds a toggle design to the START/STOP button
		and calculates time difference between the start and corresponding
		stop event"""

		if(btn1.state=='down'):
			btn1.text='STOP'
			btn2.disabled= True

			global t1
			t1 = datetime.now().replace(microsecond=0)
			l1.text ="           ...Timer ON ...\n     START TIME: "
			l1.text += datetime.strftime(t1,'%H:%M:%S')

		else:
			btn1.text='START'
			btn2.disabled= False
			t2 = datetime.now().replace(microsecond=0)
			t=t2-t1

			global time_spent
			l1 .text ="       ...TIME SPENT... \n             "
			l1.text +="%02d:%02d:%02d" % (t.seconds/3600,(t.seconds/60)%60,t.seconds%60)
			time_spent="%02d:%02d:%02d" % (t.seconds/3600,(t.seconds/60)%60,t.seconds%60)



	def comment_pop(instance):
		""" Creates a Popup to Log Task into timesheet  """

		con=lite.connect('/Users/revathy/Applications/TimeTracker.db')
		with con:
		    cur=con.cursor()
		    cur.execute("SELECT DISTINCT TASK FROM Timesheet ORDER BY TASK ")
		    rows = cur.fetchall()
		    task_list=['OTHER']
		    for row in rows:
				task_list.append(row[0])
		if con:
		    con.close()
		f=FloatLayout()
		global popup1
		popup1 = Popup(title='Task Desciption',
		content=f,
		size_hint=(1.0, 0.6), size=(400, 400))
		g=GridLayout(cols=2,row_force_default=True, row_default_height=40,
					 padding=(1,0,1,0))
		g.add_widget(Label(text="SELECT TASK ",pos=(400,800)))
		global task
		task=TextInput(size_hint=(1,0.75),write_tab=False,text_size=(2,None))
		dropdown = DropDown()
		for index in range(len(rows)+1):
		    btn = Button(text=task_list[index], size_hint_y=None, height=44)
		    btn.bind(on_release=lambda btn: dropdown.select(btn.text))
		    dropdown.add_widget(btn)
		global mainbutton
		mainbutton = Button(text='TASK', size_hint=(None, None),size=(100, 44),
							pos_hint={'center_x': .5, 'center_y': .5})
		mainbutton.bind(on_release=dropdown.open)
		dropdown.bind(on_select=MyApp.select_task)
		g.add_widget(mainbutton)
		g.add_widget(Label(text="ADD TASK",pos=(400,600)))
		g.add_widget(task)
		g.add_widget(Label(text="COMMENTS",pos=(400,400)))
		global comment
		comment=TextInput(size_hint=(1,0.75),write_tab=False)
		g.add_widget(comment)
		global msg
		msg=Label(text="Please enter the task and comment to save the task \n",
				  pos=(popup1.width-350,popup1.height-200))
		comment.bind(on_text=
					 msg.setter("Please enter the task and comment to save the task \n"))
		btn1=Button(text='SAVE',size_hint=(0.2,0.1),pos=(popup1.width-350,
					popup1.height-250))
		btn1.bind(on_press=MyApp.update_timesheet)
		btn2=Button(text='CANCEL',size_hint=(0.2,0.1),
					pos=(popup1.width-50,popup1.height-250))
		f.add_widget(msg)
		f.add_widget(btn1)
		f.add_widget(btn2)
		f.add_widget(g)
		popup1.open()
		btn2.bind(on_press=popup1.dismiss)



	def select_task(self,*args):
		""" Overrides dropdown's on_select method to populate selected task"""
		setattr(mainbutton, 'text', args[0])
		setattr(task, 'text',  args[0])


	def timesheet_pop(self):
		"""Popup to display the Timesheet"""

		popup = Popup(title='Timesheet')
		b=BoxLayout(orientation='vertical')
		s = ScrollView()
		global tslabel
		tslabel=Label(size_hint_y=None,line_height=1.5,valign="top",
					  text="|_ID_|______DATE______|___TIME_SPENT____|_____TASK_________|")
		tslabel.bind(texture_size=tslabel.setter('size'))
		btn1=Button(text='CLOSE',size_hint=(1,.06))
		s.add_widget(tslabel)
		b.add_widget(s)
		b.add_widget(btn1)
		popup.content=b
		popup.open()
		btn1.bind(on_press=popup.dismiss)

		con=lite.connect('/Users/revathy/Applications/TimeTracker.db')
		with con:
				cur=con.cursor()
				cur.execute("SELECT ID, TASK_DATE, TIME, TASK FROM Timesheet")
				rows = cur.fetchall()
				for row in rows:
				  tslabel.text=tslabel.text+"\n   "
				  tslabel.text+=str(row[0]).center(4)+"      "+str(row[1])
				  tslabel.text+="  "+str(row[2]).center(34)+"  "+str(row[3])
		if con:
				con.close()



	def update_timesheet(instance):
		"""Invoked inside comment_pop()"""
		"""Updates database with Task entries made by user"""

		if (task.text==""):
				msg.text="Task field cannot be left blank"
				task.focus=True

				return
		date_now=datetime.today().strftime("%m/%d/%Y")
		con=lite.connect('/Users/revathy/Applications/TimeTracker.db')
		with con:
			cur=con.cursor()
			sqlinsert="INSERT INTO Timesheet "
			cur.execute(sqlinsert + "(Task_Date,Task,Comments,Time) VALUES (?,?,?,?)",
					   (date_now,task.text.upper(),comment.text,time_spent))
		if con:
				con.close()

		popup1.dismiss()


	def mail_pop(self):
		"""Popup with features to mail timesheet """

		f=FloatLayout()
		global popup2
		popup2 = Popup(title='Mail Timesheet',content=f,
		size_hint=(1.0, 0.6), size=(400, 400))
		g=GridLayout(cols=1,row_force_default=True,
					 row_default_height=40,pos_hint={'center_x':.5})
		global msg
		msg=Label(text="ENTER AN EMAIL ID")
		global mail_id
		mail_id=TextInput(write_tab=False)
		g.add_widget(msg)
		g.add_widget(mail_id)
		btn1=Button(text='MAIL',size_hint=(0.2,0.1),
					pos=(popup2.width-350,popup2.height-250) )
		btn1.bind(on_press=(MyApp.mail_timesheet))
		btn2=Button(text='CLOSE',size_hint=(0.2,0.1),
					pos=(popup2.width-50,popup2.height-250))
		f.add_widget(btn1)
		f.add_widget(btn2)
		f.add_widget(g)
		popup2.open()
		btn2.bind(on_press=popup2.dismiss)

	def mail_timesheet(self):
	    """ Invoked inside mail_pop . Establishes SMTP link to email Timesheet """

	    msg.text=" ENTER AN EMAIL ID "

	    if (mail_id.text=="" or (not re.match("[^@]+@[^@]+\.[^@]+", mail_id.text))):
			msg.text="PLEASE ENTER A VALID EMAIL ID "
			mail_id.focus=True
			return

	    con=lite.connect('/Users/revathy/Applications/TimeTracker.db')
	    with con:
			cur=con.cursor()
			ts_data=cur.execute("SELECT ID, TASK_DATE, TIME, TASK FROM Timesheet")

	    with open('timetracker.csv', 'wb') as fp:
			timesheet = csv.writer(fp, delimiter=',')
			timesheet.writerow(["ID","  DATE   ","    TIME_SPENT ", "  TASK  "])
			timesheet.writerows(ts_data)


	    toaddrs=mail_id.text
	    emsg = MIMEMultipart()
	    emsg["To"] = toaddrs
	    emsg["From"] = 'timetrackerpro@gmail.com'
	    emsg["Subject"] = 'Time Tracker - Timesheet Update'
	    f =file('timetracker.csv')
	    attachment= MIMEText(f.read())
	    attachment.add_header('Content-Disposition', 'attachment',
	    					   filename='timetracker.csv')
	    emsg.attach(attachment)

	    # Credentials (if needed)
	    username = 'timetrackerpro@gmail.com'
	    password = 'tracktimepy'

	    # The actual mail send
	    server = smtplib.SMTP('smtp.gmail.com:587')
	    server.ehlo()
	    server.starttls()
	    server.login(username,password)
	    server.sendmail('timetrackerpro@gmail.com',toaddrs,emsg.as_string())
	    server.quit()
	    msg.text='MAIL SENT'

	def readme_pop(self):
		""" Readme """

		popup = Popup(title='README')
		b=BoxLayout(orientation='vertical')
		s = ScrollView()
		global tslabel
		tslabel=Label(size_hint_y=None,line_height=1.5,valign="top",
					  text="UNder CONstruction")
		tslabel.bind(texture_size=tslabel.setter('size'))
		btn1=Button(text='CLOSE',size_hint=(1,.06))
		s.add_widget(tslabel)
		b.add_widget(s)
		b.add_widget(btn1)
		popup.content=b
		popup.open()
		btn1.bind(on_press=popup.dismiss)


class TimeTracker(App):
	""" The Root Canvas """
	def build(self):
		title="Time Tracker" 	#Text on the title bar
		if not os.path.exists("TimeTracker.db"):
		    con=lite.connect('TimeTracker.db')
		    with con:
		        cur=con.cursor()
		        cur.execute("CREATE TABLE Timesheet(Id INTEGER PRIMARY KEY, Task_Date TEXT, Task TEXT NOT NULL , Comments TEXT , Time TEXT)")


		    if con:
		        con.close()

		return MyApp()


if __name__ == '__main__':
	TimeTracker().run() #method to start
