#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import tcp_server
import Adafruit_DHT

def send_message(message):
	#print('send_message')
	tcp_server.message_queue_out.put(message)

def message_handler(type_string, name_string, in_value):

	global name
	global num		
	global value

	for i in num:
		if name_string==name[i]:
			if type_string=='w':
				value[i]=in_value
				set_time[i]=time.time()
				print('Wrote ' + str(in_value) + ' to ' + name[i])
			
			if type_string=='r':
				if stype[i]=='HI' or stype[i]=='TI':
					send_message('!i!'+name[i]+'!'+"{:.1f}".format(value[i]) +'$\n')
				else:
					send_message('!i!'+name[i]+'!'+str(int(value[i]))+'$\n')
				print('Answered read message!')
			

def init():
	
	# use P1 header pin numbering convention
	GPIO.setmode(GPIO.BOARD)

	global name
	global num		
	global stype
	global value
	global aux_value
	global aux_value2
	global aux_value3	
	global aux_value4
	global pin1
	global pin2
	global pin3	
	global set_time
	
	#		0	  1	      2		  3 	   4	    5        6        7        8        9        10        11
	name=		['LI_GR', 'LI_GR_L1', 'LI_GR_L2', 'DO_GR', 'ZE_GR', 'ZE_G2', 'T1_GR', 'TI_GR', 'HI_GR', 'TI_G2', 'HI_G2',  'DA_GR']
	num=		range(12)	
	stype=		['LI',	  'LI',	      'LI',	  'DO',	   'LI',    'LI',    'TA',    'TI',    'HI',    'TI',    'HI',     'DA']
	value=		[0,	  0,	      0,	  0,	   0,	    0,	     0,	      0,       0,       0,       0,        0]
	aux_value=	[0,	  0,	      0,	  0,	   0,	    0,	     0,	      0,       0,       0,       0,        0]
	aux_value2=	[0,	  0,	      0,	  0,	   0,	    0,	     0,	      0,       0,       0,       0,        0]
	aux_value3=	[0,	  0,	      0,	  0,	   0,	    0,	     0,	      8,       7,       10,      9,        0]
	aux_value4=	[0,	  0,	      0,	  0,	   0,	    0,	     0,	      600,     600, 	610,	 610,      0]
	pin1=		[3,	  5,	      7,	  36,	   15,	    16,	     40,      18,      18,	17,	 17,       8]
	pin2=		[0,	  0,	      0,	  37,	   0,	    0,	     0,	      0,       0,       0,       0,        15]
	pin3=		[0,	  0,	      0,	  38,	   0,	    0,	     0,	      0,       0,       0,       0,        16]
	set_time=	[0,	  0,	      0,	  0,	   0,	    0,	     0,	      0,       0,       0,       0,        0]



	for i in num:
		if stype[i]=='LI':
			GPIO.setup(pin1[i], GPIO.OUT, initial=1)
		
		
		if stype[i]=='DO':
			GPIO.setup(pin1[i], GPIO.IN)
			GPIO.setup(pin2[i], GPIO.IN)
			GPIO.setup(pin3[i], GPIO.IN)

		if stype[i]=='DA':
			GPIO.setup(pin1[i], GPIO.OUT, initial=1)
			GPIO.setup(pin2[i], GPIO.OUT, initial=1)
			GPIO.setup(pin3[i], GPIO.OUT, initial=1)

		
		
		
		if stype[i]=='TA':
			GPIO.setup(pin1[i], GPIO.IN)
	
	
	

def update():

	global name
	global stype
	global value
	global aux_value
	global aux_value2
	global aux_value3
	global aux_value3
	global pin1
	global pin2
	global pin3
	global set_time


	for i in num:

		#print('Update: ' + name[i])		

		if stype[i]=='LI':
			#print(name[i] + ' ' + str(value[i]))
			if value[i]==0 and aux_value[i]==1:
				GPIO.output(pin1[i], True)
				aux_value[i]=0
				send_message('!w!'+name[i]+'!'+str(int(value[i]))+'$\n');
			if value[i]==1 and aux_value[i]==0:
				GPIO.output(pin1[i], False)
				aux_value[i]=1
				send_message('!w!'+name[i]+'!'+str(int(value[i]))+'$\n');
			
			if value[i]!=1 and value[i]!=0:
				if aux_value[i]==0:
					GPIO.output(pin1[i], False)
					aux_value[i]=1
					value[i]=1
					print('Toggled on ' + name[i] + ' .')
				else:
					GPIO.output(pin1[i], True)
					aux_value[i]=0
					value[i]=0
					print('Toggled off ' + name[i] + ' .')
				send_message('!w!'+name[i]+'!'+str(int(value[i]))+'$\n');




		if stype[i]=='DO':
			
			#auslesen=> aux, bei anderung nachricht senden 
			a = not(GPIO.input(pin1[i]))
			b = not(GPIO.input(pin2[i]))
			c = not(GPIO.input(pin3[i]))
			new_aux=0
			if a==1: new_aux=1
			if b==1: new_aux=-1
			if c==1: new_aux=0
			if aux_value[i]!=new_aux and new_aux==aux_value4[i]:
				print('door changed from')
				print(aux_value[i])
				print(new_aux)
				if aux_value[i]==-1:
					aux_value2[i]=1
				if aux_value[i]==1:
					aux_value3[i]=1 
				aux_value[i]=new_aux
				send_message('!w!'+name[i]+'!'+str(int(value[i]))+'$\n');
			else:
				aux_value3[i]=0 
				aux_value2[i]=0
			
			if time.time()>set_time[i]:
				aux_value4[i]=new_aux
				set_time[i]=time.time()+0.1
			
			#regenerien:
			value[i]=aux_value[i]

		if stype[i]=='TA':
			input_value = not(GPIO.input(pin1[i]))
			#print('input_value ' + name[i] + ' ' + str(input_value))	
			
			if aux_value2[i]==1 and aux_value[i]==0 and input_value==1:
				value[i]=1
				print('Positive edge on ' + name[i] + ' .')
			else:
				value[i]=0

			if aux_value2[i]==input_value:
				aux_value[i]=input_value
			
			if time.time()>set_time[i]:
				aux_value2[i]=input_value
				set_time[i]=time.time()+0.1
			
			
			
						
			

		if stype[i]=='DA':
			if value[i]==0: 
				GPIO.output(pin1[i], False)
				aux_value2[i]=time.time()+0.3
				print('Tor stop.')
				value[i]=-3
			if value[i]==-1: 
				GPIO.output(pin2[i], False)
				aux_value3[i]=time.time()+0.3
				print('Tor zu.')
				value[i]=-3
			if value[i]==1: 
				GPIO.output(pin3[i], False)
				aux_value4[i]=time.time()+0.3
				print('Tor auf.')
				value[i]=-3
			
			if aux_value2[i]<time.time():
					GPIO.output(pin1[i], True)

			if aux_value3[i]<time.time():
					GPIO.output(pin2[i], True)
			
			if aux_value4[i]<time.time():
					GPIO.output(pin3[i], True)
						
			

						



		if stype[i]=='TI':
			if time.time()>aux_value[i]:
				aux_value[i]=aux_value4[i]+time.time()
				sensor = Adafruit_DHT.DHT22
				humidity, temperature = Adafruit_DHT.read(sensor, pin1[i])
				if humidity is None or temperature is None:
					humidity=100
					temperature=100
				value[i]=temperature
				value[aux_value3[i]]=humidity
				print('Temp and Hum:')
				print(temperature)
				print(humidity)


	#print('End: states.update')
	#print(value)

			
						
						





								
					
			








		











		
			






