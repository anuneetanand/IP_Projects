#Anuneet Anand
#2018022
#Section-A
#Group-6
#HomeWork Assignment 1

''' 
The module takes the location , n (For nth day from today) and time as input from the user and displays
appropiate weather information extracted from a JSON response given by a weather data website.
The concept of string slicing is used to extract required data.
DateTime Format: yyyy-mm-dd HH:MM:SS
In case no values for n and t are entered , respective default values are used: 0 , '03:00:00'
Valid values for City Name, n , t should be entered.
'''

import datetime
import urllib.request
date=datetime.date.today()
API_key='a22de6c28a1cec3173d177f111ebb5ac'

# Function to get weather response
def weather_response(location,API_key):
	''' It opens the website and stores it contents in a variable.The variable is returned as JSON response'''
	w=urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s'%(location,API_key),
		cafile=None, capath=None, cadefault=False, context=None)
	i=w.read()
	return i

# function to check for valid response 
def has_error(location,json):
	''' Returns True if the city name given by the user doesn't match the one given in JSON response'''
	text=str(json).lower()
	k=True
	if text.find(location.lower(),text.index('name')+7,len(location)):
		k=False
	return k

# functions to get attributes on nth day at time t

def get_temperature (json,n=0,t="03:00:00"):
	text=str(json)
	d=str(date+datetime.timedelta(days=n))                #Calculating Date
	dt=d+' '+t
	dtp=text.find(dt)                                     #Searching For Date-Time Of Required Data
	lm=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
	lm=str(lm+datetime.timedelta(hours=-3))
	lmp=text.find(lm)                                     #Searching For Date-Time Of Preceding Data 
	if dtp!=-1:
		if lmp!=-1:
			a=text.find('temp',lmp,dtp)+6
			b=text.find(',',a)
			T=text[a:b]
		else:
			a=text.find('temp')+6                      	   #In Case There Is No Preceding Data
			b=text.find(',',a)
			T=text[a:b] 
	else:
		E="Not_Available"         						   #In Case There Is No Required Data
		return E
	return float(T)
	
def get_humidity(json,n=0,t="03:00:00"):
	text=str(json)
	d=str(date+datetime.timedelta(days=n))                #Calculating Date
	dt=d+' '+t
	dtp=text.find(dt)                                     #Searching For Date-Time Of Required Data
	lm=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
	lm=str(lm+datetime.timedelta(hours=-3))
	lmp=text.find(lm)                                     #Searching For Date-Time Of Preceding Data
	if dtp!=-1:
		if lmp!=-1:
			a=text.find('humidity',lmp,dtp)+10
			b=text.find(',',a)
			H=text[a:b]
		else:
			a=text.find('humidity')+10                    #In Case There Is No Preceding Data
			b=text.find(',',a)
			H=text[a:b] 
	else:
		E="Not_Available"								  #In Case There Is No Required Data
		return E
	return int(H)
	
def get_pressure(json,n=0,t="03:00:00"):
	text=str(json)
	d=str(date+datetime.timedelta(days=n))                #Calculating Date
	dt=d+' '+t
	dtp=text.find(dt)                                     #Searching For Date-Time Of Required Data
	lm=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
	lm=str(lm+datetime.timedelta(hours=-3))
	lmp=text.find(lm)                                     #Searching For Date-Time Of Preceding Data
	if dtp!=-1:
		if lmp!=-1:
			a=text.find('pressure',lmp,dtp)+10
			b=text.find(',',a)
			P=text[a:b]
		else:
			a=text.find('pressure')+10                    #In Case There Is No Preceding Data
			b=text.find(',',a)
			P=text[a:b] 
	else:
		E="Not_Available"								  #In Case There Is No Required Data
		return E
	return float(P)

def get_wind(json,n=0,t="03:00:00"):
	text=str(json)
	d=str(date+datetime.timedelta(days=n))                #Calculating Date
	dt=d+' '+t
	dtp=text.find(dt)                                     #Searching For Date-Time Of Required Data
	lm=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
	lm=str(lm+datetime.timedelta(hours=-3))
	lmp=text.find(lm)                                     #Searching For Date-Time Of Preceding Data
	if dtp!=-1:
		if lmp!=-1:
			a=text.find('wind',lmp,dtp)+16
			b=text.find(',',a)
			W=text[a:b]
		else:
			a=text.find('wind')+16                        #In Case There Is No Preceding Data
			b=text.find(',',a)
			W=text[a:b] 
	else:
		E="Not_Available"                    			  #In Case There Is No Required Data
		return E
	return float(W)

def get_sealevel(json,n=0,t="03:00:00"):
	text=str(json)
	d=str(date+datetime.timedelta(days=n))                #Calculating Date
	dt=d+' '+t
	dtp=text.find(dt)                                     #Searching For Date-Time Of Required Data
	lm=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
	lm=str(lm+datetime.timedelta(hours=-3))
	lmp=text.find(lm)                                     #Searching For Date-Time Of Preceding Data
	if dtp!=-1:
		if lmp!=-1:
			a=text.find('sea_level',lmp,dtp)+11
			b=text.find(',',a)
			S=text[a:b]
		else:
			a=text.find('sea_level')+11                   #In Case There Is No Preceding Data
			b=text.find(',',a)
			S=text[a:b] 
	else:
		E="Not_Available"  								  #In Case There Is No Required Data
		return E
	return float(S)

if __name__ == '__main__':                                #To Run As A Script
	
	location=input("Enter Name Of City: ")
	info=weather_response(location,API_key)
	e=has_error(location,info)
	if e:
		print("Invalid Query")
	else:

		n=int(input("Enter Value For n To See Results Of nth Day From Today:\nValid=(0,4)\n"))
		t=str(input("Enter Time :\nValid=(03:00:00/06:00:00/09:00:00/12:00:00/15:00:00/18:00:00/21:00:00)\n"))
		if (n<0 or n>=4):
			print("Invalid Value For n")
		elif (not(t=='03:00:00' or t=='06:00:00' or t=='09:00:00' or t=='12:00:00' or t=='15:00:00' or t=='18:00:00' or t=='21:00:00')):
			print("Invalid Value For t")
		else:
			print("Temperature:",get_temperature(info,n,t))
			print("Humidity:",get_humidity(info,n,t))
			print("Pressure:",get_pressure(info,n,t))
			print("Wind:",get_wind(info,n,t))
			print("Sea Level:",get_sealevel(info,n,t))


