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
#from kivy.uix.scatter import Scatter
#from kivy.uix.floatlayout import FloatLayout # for resolution
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from datetime import datetime
from kivy.graphics import Color, Rectangle




class MyApp(App):
	title="Time Tracker" 	#Text on the title bar 
	
	def build(self):
			
		b = GridLayout(cols=2,spacing=100, padding=30)
		btn1 = ToggleButton(text='START', group='state', size_hint=(.22, .1),pos_hint={'x':.3, 'y':.7},pos=(1,1))
		btn1.bind(on_press=MyApp.start_timer)
	
		btn2 = ToggleButton(text='STOP', group='state', state='down',size_hint=(.22, .1),pos_hint={'x':.3, 'y':.7},pos=(1,2))
		btn2.bind(on_press=MyApp.stop_timer)
		global l1
		
		l1 = Label (text="Begin to track time\n")
		
		l2 = Label(text="comments\n")
		b.add_widget(btn1)
		
		b.add_widget(btn2)
		b.add_widget(l1)
		b.add_widget(l2)
		return b 
		
	def start_timer(instance):
		global t1
		t1 = datetime.now().replace(microsecond=0)
		l1 .text ="Timer started...\nStart Time: "+ datetime.strftime(t1,'%H:%M:%S')
	
	def stop_timer(instance):
		t2 = datetime.now().replace(microsecond=0)
		t=t2-t1
		l1 .text ="Time Spent on task : %d" %t.seconds +" seconds"
		
if __name__ == '__main__':
	MyApp().run() #method to start