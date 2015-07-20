#!/usr/bin/python
# coding=utf-8
''' Copyright © 2015 Revathy Narayanan 


   This program is released under the "MIT license".
   Please see the file LICENSE in this distribution for
   license terms. '''

import os, sys
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



class MyApp(App):
	title="Time Tracker" 	#Text on the title bar 
	
	def build(self):
		Window.size = (480, 640)	
		b = FloatLayout()
		global btn1
		btn1 = ToggleButton(text='START', group='state', size_hint=(.2,.012),pos=(200,500))
		btn1.bind(on_press=MyApp.start_timer)
		btn2 = ToggleButton(text='ADD COMMENTS', group='state', size_hint=(.3,.012),pos=(50,100))
		btn2.bind(on_press=MyApp.comment_pop)
		btn3 = ToggleButton(text='VIEW TIMESHEET', group='state', size_hint=(.3,.012),pos=(300,100))
		btn3.bind(on_press=MyApp.timesheet_pop)
	
		
		global l1
		
		l1 = Label (text="Begin to track time\n")
		
	
		b.add_widget(btn1)
		b.add_widget(btn2)
		b.add_widget(btn3)
		b.add_widget(l1)
		
		return b 
		
	def start_timer(instance):
		
		if(btn1.state=='down'):
			btn1.text='STOP'
			global t1
			t1 = datetime.now().replace(microsecond=0)
			l1 .text ="Timer started...\nStart Time: "+ datetime.strftime(t1,'%H:%M:%S')
			
		else:
			btn1.text='START'
			t2 = datetime.now().replace(microsecond=0)
			t=t2-t1
			l1 .text ="Time Spent on task \n %02d:%02d:%02d" % (t.seconds/3600,(t.seconds/60)%60,t.seconds%60)
			
	'''def cal_time(t):
		
	
		hr=t.seconds/3600
		mins=(t.seconds/60)%60
		sec=t.seconds%60
		return (hr,mins,sec)
		'''

	def comment_pop(instance):
		
		f=FloatLayout()
		popup = Popup(title='Task Desciption',
		content=f,
		size_hint=(1.0, 0.6), size=(400, 400))
		btn1=Button(text='SAVE',size_hint=(0.2,0.1),pos=(popup.width-350,popup.height-250))
		btn2=Button(text='CANCEL',size_hint=(0.2,0.1),pos=(popup.width-50,popup.height-250))
		
		t=TextInput(pos=(popup.width-388,popup.height-200),size_hint=(1,0.75))
		f.add_widget(t)
		f.add_widget(btn1)
		f.add_widget(btn2)
		popup.open()
		btn1.bind(on_press=popup.dismiss)
		btn2.bind(on_press=popup.dismiss)
		
		
	def timesheet_pop(instance):
		
			b=BoxLayout()
			popup = Popup(title='Timesheet',
			content=b)
			btn1=Button(text='CLOSE',size_hint=(0.2,0.075),pos=(popup.width-350,popup.height-250))
			
			l=Label(text="Under Construction")
			b.add_widget(l)
			b.add_widget(btn1)
			
			popup.open()
			btn1.bind(on_press=popup.dismiss)
			
		
		
		
		
	
			

			
		

		
		
if __name__ == '__main__':
	MyApp().run() #method to start