# CSE-112
# Project-2 : Booth's Algorithm
# Anuneet Anand (2018022)
# Pruthwiraj Nanda (2018075)

def Int(x):
	''' Finds Decimal Representation Of A Binary Number'''
	s = 1
	if x[0]=="1":
		x = TC(x)
		s = -1
	n = 0
	for i in range(len(x)-1,-1,-1):
		n = n + int(x[i])*(2**(len(x)-i-1))
	n = n * s
	return n

def Ext(B,n):
	''' Extends A Binary Number To Required Number Of Bits''' 
	S = B[0]
	while len(B)<n:
		B = S + B
	return B

def Bin(x):
	''' Converts A Decimal Number To It's Unsigned Binary Representation'''
	B = ""
	while x:
		B = str(x%2) + B
		x = x // 2
	return "0" + B

def TC(x):
	''' Returns Two's Complement Representation Of An Unsigned Binary Number'''
	s = ""
	j = x.rfind("1")
	L = list(x)
	for i in range(j):
		L[i] = int(L[i]) ^ 1
	for i in L:
		s += str(i)
	return s

def Num(x):
	''' Converts Decimal Number Into Its Appropiate Binary Representation'''
	if x>=0:
		return Bin(abs(x))
	else:
		return TC(Bin(abs(x)))

def Add(x,y):
	''' Adds Two Binary Numbers '''
	n = max (len(x),len(y))
	x=Ext(x,n)
	y=Ext(y,n)
	r = 0
	c = 0
	z = ""
	for i in range(n-1,-1,-1):
		r = int(x[i]) ^ int(y[i]) ^ c
		c = ( (int(x[i]) ^ int(y[i]) ) & c ) | ( int(x[i]) & int(y[i]) )
		z = str(r) + z
	return z

def Multiply(X,Y):
	''' Multiplication Algorithm '''

	x = Num(X)
	y = Num(Y)
	l = max(len(x),len(y))

	A = Ext(x,l) + "0" * (l+1)
	B = Ext(Num(-X),l) + "0" * (l+1)
	P = "0" * (l) + Ext(y,l) + "0"

	for i in range(l):
		if P[-1]=="1" and P[-2]=="0":			# Last Two Bits : "01"
			P = Add(P,A)
		elif P[-1]=="0" and P[-2]=="1":			# Last Two Bits : "10"
			P = Add(P,B)
		P = P[0]+P[:-1]							# Right Shift
	P = P[:-1]
	return Int(P),P

def Divide(X,Y):
	''' Division Algorithm '''

	x = Num(X)
	y = Num(Y)
	l = max(len(x),len(y))
	qs = int(x[0]) ^ int(y[0])					# Determining Sign Of Quotient
	rs = int(x[0])								# Determining Sign Of Remainder

	Q =  Ext(Num(abs(X)),l)
	R = "0" * (l+1)
	A =  Ext(Num(abs(Y)),l)
	B =  Ext(Num(-abs(Y)),l)

	for i in range(l):
		if R[0]=="1":							# R<0
			R = R[1:] + Q[0]					# R = R + A
			R = Add(R,A)
		else:									# R>=0
			R = R[1:] + Q[0]					# R = R - A
			R = Add(R,B)
		if R[0]=="1":
			Q = Q[1:] + "0"
		else:
			Q = Q[1:] + "1"
	if R[0]=="1":
		R = Add(R,A)

	if qs == 1:
		Q = TC(Q)
	if rs == 1:
		R = TC(R)

	return Int(Q),Int(R),Q,R

print("Enter First Number: ",end="")
X = int(input())
print("Enter Second Number: ",end="")
Y = int(input())
if (Y==0):
	print("Divsior Can't Be Zero")
else:
	P,Pb = Multiply(X,Y)
	Q,R,Qb,Rb = Divide(X,Y)

	with open('Output.txt','w') as Output_File:
		Output_File.write("Numbers: "+str(X)+", "+str(Y)+"\n")
		Output_File.write("Product: "+str(P)+"	"+str(Pb)+"\n")
		Output_File.write("Quotient: "+str(Q)+"	"+str(Qb)+"		"+"Remainder :"+str(R)+"	"+str(Rb)+"\n")
		Output_File.close()
# END OF CODE
