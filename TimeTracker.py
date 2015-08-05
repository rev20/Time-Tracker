#!/usr/bin/python
# coding=utf-8
''' Copyright © 2015 Revathy Narayanan 


   This program is released under the "MIT license".
   Please see the file LICENSE in this distribution for
   license terms. '''

import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from datetime import datetime
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window 
from kivy.uix.popup import Popup
import kivy.core.text.markup
from kivy.properties import BooleanProperty
from kivy.uix.dropdown import DropDown
import sqlite3 as lite
import sys
from functools import partial
from kivy.graphics import BorderImage
from kivy.uix.scrollview import ScrollView
import re 
import smtplib
from kivy.properties import NumericProperty
import csv


from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class MyApp(FloatLayout):
	def __init__(self, **kwargs):
		super(MyApp,self).__init__(**kwargs)
		Window.size = (480, 640)
		with self.canvas:
			BorderImage(border=(10, 10, 10,10),source='time.jpg',size=(480,640))
		
	
			
	
		global btn1
		btn1 = ToggleButton(text='START', group='state', size_hint=(.2,.012),pos=(200,350))
		btn1.bind(on_press=MyApp.start_timer)
		global btn2
		btn2 = ToggleButton(text='LOG TASK', group='state', size_hint=(.3,.012),pos=(20,50),disabled=True)
		btn2.bind(on_press=MyApp.comment_pop)
		btn3 = Button(text='VIEW TIMESHEET',size_hint=(.3,.012),pos=(330,50))
		btn3.bind(on_press=MyApp.timesheet_pop)
		btn4 = Button(text='MAIL TIMESHEET', group='state', size_hint=(.3,.012),pos=(330,550))
		btn4.bind(on_press=MyApp.mail_pop)
	
		
		global l1
		
		l1 = Label (text="\n Begin to track time\n")
		
	
		self.add_widget(btn1)
		self.add_widget(btn2)
		self.add_widget(btn3)
		self.add_widget(btn4)

		self.add_widget(l1)
		
	
		
	def start_timer(instance):
				
		if(btn1.state=='down'):
			btn1.text='STOP'
			btn2.disabled= True
			
			global t1
			t1 = datetime.now().replace(microsecond=0)
			l1 .text ="Timer started...\nStart Time: "+ datetime.strftime(t1,'%H:%M:%S')
			
		else:
			btn1.text='START'
			btn2.disabled= False
			t2 = datetime.now().replace(microsecond=0)
			t=t2-t1
			
			global time_spent
			l1 .text ="Time Spent on task \n %02d:%02d:%02d" % (t.seconds/3600,(t.seconds/60)%60,t.seconds%60)
			time_spent="%02d:%02d:%02d" % (t.seconds/3600,(t.seconds/60)%60,t.seconds%60)
			
	'''def cal_time(t):
		
	
		hr=t.seconds/3600
		mins=(t.seconds/60)%60
		sec=t.seconds%60
		return (hr,mins,sec)
		'''

	def comment_pop(instance):
		max_chars = NumericProperty(20)
		f=FloatLayout()
		global popup1
		popup1 = Popup(title='Task Desciption',
		content=f,
		size_hint=(1.0, 0.6), size=(400, 400))
		g=GridLayout(cols=2,row_force_default=True, row_default_height=40)
		global msg
		msg=Label(text="Please enter the task and comment to save the task \n")
		g.add_widget(Label(text="TASK",pos=(400,600)))
		global task
		task=TextInput(size_hint=(1,0.75),write_tab=False,text_size=(2,None))
		
		
		g.add_widget(Label(text="COMMENTS",pos=(400,400)))
		global comment
		comment=TextInput(size_hint=(1,0.75),write_tab=False)
		g.add_widget(msg)
		g.add_widget(task)
		g.add_widget(comment)
		
		
		btn1=Button(text='SAVE',size_hint=(0.2,0.1),pos=(popup1.width-350,popup1.height-250))
		btn1.bind(on_press=partial(MyApp.update_timesheet))
		btn2=Button(text='CANCEL',size_hint=(0.2,0.1),pos=(popup1.width-50,popup1.height-250))
		f.add_widget(btn1)
		f.add_widget(btn2)
		f.add_widget(g)
		popup1.open()
		btn2.bind(on_press=popup1.dismiss)
		
	
		
	def timesheet_pop(self):
			
			popup = Popup(title='Timesheet')
			b=BoxLayout(orientation='vertical')
			s = ScrollView()
			global tslabel
			tslabel=Label(size_hint_y=None,line_height=1.5,valign="top", text="|_ID_|______DATE______|___TIME_SPENT____|_____TASK_________|")
			tslabel.bind(texture_size=tslabel.setter('size'))
			btn1=Button(text='CLOSE',size_hint=(.4,.022))
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
				  tslabel.text=tslabel.text+"\n   "+str(row[0]).center(4)+"      "+str(row[1])+"  "+str(row[2]).center(34)+"  "+str(row[3])

			if con: 
			
					con.close()
			
			
			

			
			
			
	@staticmethod
	def update_timesheet(instance):
		
		if (task.text==""):
				msg.text="Task field cannot be left blank"
				task.focus=True 
				
				return
		
		
		
		
		date_now=datetime.today().strftime("%m/%d/%Y")
		con=lite.connect('/Users/revathy/Applications/TimeTracker.db')
		with con:

			cur=con.cursor()
			cur.execute("INSERT INTO Timesheet (Task_Date,Task,Comments,Time) VALUES (?,?,?,?)",(date_now,task.text,comment.text,time_spent))
		
		
		if con: 
				con.close()
				
		popup1.dismiss()
		
	def mail_pop(self):
	
		f=FloatLayout()
		global popup2
		popup2 = Popup(title='Mail Timesheet',content=f,
		size_hint=(1.0, 0.6), size=(400, 400))
		g=GridLayout(cols=2,row_force_default=True, row_default_height=40)
		global msg
		msg=Label(text="Enter a vail mail id :")
		g.add_widget(Label(text="MAIL ID ",pos=(400,600)))
		global mail_id
		mail_id=TextInput(size_hint=(1,0.75),write_tab=False)
		g.add_widget(msg)
		g.add_widget(mail_id)
		btn1=Button(text='MAIL',size_hint=(0.2,0.1),pos=(popup2.width-350,popup2.height-250))
		btn1.bind(on_press=(MyApp.mail_timesheet))
		btn2=Button(text='CANCEL',size_hint=(0.2,0.1),pos=(popup2.width-50,popup2.height-250))
		f.add_widget(btn1)
		f.add_widget(btn2)
		f.add_widget(g)
		popup2.open()
		btn2.bind(on_press=popup2.dismiss)
	
	def mail_timesheet(self):
	#	if (mail_id.text=="" or (not re.match("[^@]+@[^@]+\.[^@]+", mail_id.text))):
	#			msg.text="Please enter a Valid Email Id "
	#			mail_id.focus=True 
			
			
			
	    con=lite.connect('/Users/revathy/Applications/TimeTracker.db')
	    with con:
				
				cur=con.cursor()
				ts_data=cur.execute("SELECT ID, TASK_DATE, TIME, TASK FROM Timesheet")


		
			
	    with open('timetracker.csv', 'wb') as fp:
			 timesheet = csv.writer(fp, delimiter=',')
			 timesheet.writerow(["|_ID_|______DATE______|___TIME_SPENT____|_____TASK_________|"])
			 timesheet.writerows(ts_data)
			  #timesheet.close()'''

		

		
		
		

		
		
				
				
				
class TimeTracker(App):
	def build(self):
		title="Time Tracker" 	#Text on the title bar
		return MyApp()
		 
		
		
		
		
		
	
			

			
		

		
if __name__ == '__main__':
	TimeTracker().run() #method to start