# CSE 101 - IP HW2
# K-Map Minimization 
# Name: Anuneet Anand
# Roll Number: 2018022
# Section: A
# Group: 6
# Date: 17/10/18 

def DBC(d):
	''' Converts a Decimal number to its 4-Bit Binary equivalent'''
	s=''
	while d:
		r=d%2
		d=int(d/2)
		s=str(r)+s
	while len(s)!=4:
		s='0'+s	
	return s	

def hyp(a,b):
	''' Inserts hyphen in place of the bit which gets eliminated on combining the two arguments'''
	x=''
	for i in range(4):
		if (a[i]==b[i]):
			x=x+a[i]
		else:
			x=x+'-'	
	return x

def Chk(a,b):
	''' Checks if the two arguments can be combined to eliminate a bit'''
	c=0
	for i in range(4):
		if a[i]!=b[i]:
			c=c+1
	return c 

def XD(XDp,PI):
	''' Finds Prime Implicants and store them in PI'''
	XDn={}												#n=p*
	for i in XDp.keys():
		a=XDp[i]
		k=0
		for j in XDp.keys():
			b=XDp[j]
			if Chk(a,b)==1:
				t=str(i)+','+str(j)
				x=hyp(a,b)
				if x not in XDn.values():
					XDn[t]=x 							#2 Terms of XDp combine to become a term in XDn
				k=1
		if not k:
			PI[str(i)]=a 								#Collecting Terms of XDp which can't be combined
	return XDn,PI

def FEPI(T,MT):
	'''Finds Essential Prime Implicants From PI''' 
	X=[]
	K={i:i.split(',') for i in T}						#Set of PI Terms 
	for a in MT:										#Ignore Don't Cares
		c=0
		for b in K.keys():
			if str(a) in K[b]:
				c=c+1
				t=b
		if c==1 and t not in X: 						#If there exists a minterm uniquely covered by the PI 
			X.append(t)
	return X

def BS(RK,XEPI,NC,RPI):
	''' Finds combinations of RPI which completes cover'''
	i=[]													#List of combinations Of RPI which completes cover 
	NC=set(NC)
	for a in RK.keys():
		L=set(RK[a])
		if L>NC or L==NC:
			XEPI={}
			XEPI[a]=RPI[a]
			i.append(XEPI) 
		else:
			for b in RK.keys():
				L=set(RK[a]+RK[b])
				if L>NC or L==NC:
					XEPI={}
					XEPI[a]=RPI[a]
					XEPI[b]=RPI[b]
					i.append(XEPI)
				else:
					for c in RK.keys():
						L=set(RK[a]+RK[b]+RK[c])
						if L>NC or L==NC:
							XEPI={}
							XEPI[a]=RPI[a]
							XEPI[b]=RPI[b]
							XEPI[c]=RPI[c]
							i.append(XEPI) 
						else:
							for d in RK.keys():
								L=set(RK[a]+RK[b]+RK[c]+RK[d])
								if L>NC or L==NC:
									XEPI={}
									XEPI[a]=RPI[a]
									XEPI[b]=RPI[b]
									XEPI[c]=RPI[c]
									XEPI[d]=RPI[d]
									i.append(XEPI)
								else:
									for e in RK.keys():
										L=set(RK[a]+RK[b]+RK[c]+RK[d]+RK[e])
										if L>NC or L==NC:
											XEPI={}
											XEPI[a]=RPI[a]
											XEPI[b]=RPI[b]
											XEPI[c]=RPI[c]
											XEPI[d]=RPI[d]
											XEPI[e]=RPI[e]
											i.append(XEPI)
	return i									
	 
def FPI(RPI,EPI,MT):
	''' Collects Non-Essential Prime Implicants required to complete cover & include them alongwith with Essential Prime Implicants'''
	XEPI={}
	NC=[]
	EK={i:list(map(int,i.split(','))) for i in EPI.keys()}
	RK={i:list(map(int,i.split(','))) for i in RPI.keys()}

	for a in MT:
		c=0
		for b in EK.keys():
			if a in EK[b]:
				c=1
		if not(c):
			NC.append(a)								#Collecting Terms Not Covered by EPI
	NC.sort()

	H=[]												#List Of Best Solutions
	if len(NC)>0:
		i=BS(RK,XEPI,NC,RPI)
		if i:
			m=len(i[0])
			j={}
			G=[]
			for k in i:
				if len(k)<=m:
					m=len(k)
			for k in i:
				if len(k)==m:							#Choosing solutions with minimum number of terms
					j=k
					if j not in G:
						G.append(j)
	
			for j in G:
				NEPI={}
				NEPI=dict(EPI)
				for x in j.keys():
					NEPI[x]=RPI[x]
					if NEPI not in H:
						H.append(NEPI)
	else:
		NEPI=dict(EPI)
		H.append(NEPI)
	return H
	
def mexp(M):
	''' Converts the binary data to boolean expression'''
	k=''
	if M[0]=='1':
		k=k+'w'
	if M[0]=='0':
		k=k+'w’'
	if M[1]=='1':
		k=k+'x'
	if M[1]=='0':
		k=k+'x’'
	if M[2]=='1':
		k=k+'y'
	if M[2]=='0':
		k=k+'y’'
	if M[3]=='1':
		k=k+'z'
	if M[3]=='0':
		k=k+'z’'
	return k

def minFunc(numVar, stringIn):
	'''
	This python function takes function of maximum of 4 variables as input and gives the corresponding minimized 
	function(s) as the output (minimized using the K-Map methodology),considering the case of Don’t Care conditions.
	Input is a string of the format (a0,a1,a2, ...,an) d (d0,d1, ...,dm)
	Output is a string representing the simplified Boolean Expression in SOP form.
	No need for checking of invalid inputs.Do not include any print statements in the function.
	'''
	n=numVar
	S=stringIn
	MT,DC=S.split('d')
	MT=MT[1:-2]
	if len(MT):
		MT=list(map(int,MT.split(',')))		 			#Collecting Minterms From Input
	else:
		MT=[]
	MTb=[DBC(i) for i in MT]							#Minterms in Binary Format
	DC=DC[2:-1]
	if len(DC):
		DC=list(map(int,DC.split(',')))					#Collecting Don't Cares From Input
	else:
		DC=[]	
	DCb=[DBC(i) for i in DC]							#Don't Cares in Binary Format

	MD=MT+DC
	MDb=MTb+DCb

	PI={}												#Prime Implicants
	XD1={i:DBC(i) for i in MD}
	XD2,PI=XD(XD1,PI)										#Finding Pairs
	XD4,PI=XD(XD2,PI)										#Finding Quads
	XD8,PI=XD(XD4,PI)										#Finding Octs
	XD16,PI=XD(XD8,PI)

	T=list(PI.keys())
	X=FEPI(T,MT)			
	EPI={}												#Essential Prime Implicants
	RPI={}												#Remaining Prime Implicants	
	TEPI={}												

	for i in PI.keys():
		if i in X:
			EPI[i]=PI[i]
		else:
			RPI[i]=PI[i]
	
	H=FPI(RPI,EPI,MT)									#Final groups of Prime Implicants which cover all minterms
	SO=''
	for TEPI in H:
		SEL=''
		SE=[]					
		for i in TEPI.values():								#Converting To Boolean Terms
			if n==2:
				j=(str(i))[2:]+'-'+'-'
				SE.append(mexp(list(j)))					#Two Variable Terms(w,x) 
			if n==3:
				j=(str(i))[1:]+'-'
				SE.append(mexp(list(j)))					#Three Variable Terms(w,x,y)
			if n==4:
				SE.append(mexp(list(i)))					#Four Variable Terms(w,x,y,z)
	
		SE.sort()											#Sorting Lexicographically (Note: s comes before s’)
		for i in SE:
			SEL=SEL+'+'+i 									#Forming Boolean Expression
		SO=SO + SEL[1:] + ' OR '							#Solutions separated by OR
	
	stringOut=SO[:-4]
	if len(MD)==(2**n):                          
		stringOut='1'
	if len(MT)==0:
		stringOut='0'
	return stringOut

if __name__ == '__main__': 								#To execute as a script
	numVar=int(input("No. Of variables: "))
	stringIn=input("Function: ")
	f=minFunc(numVar,stringIn)
	print("Simplified expression: ",f)