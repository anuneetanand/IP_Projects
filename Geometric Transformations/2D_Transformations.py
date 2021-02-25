# Anuneet Anand
# 2018022
# Section-A
# Group-6
# HW4 - Transformations of 2D Geometric Objects

import matplotlib.pyplot as plt
import math as m
plt.ion()

def GN(l,u,n):
	''' To generate a continuous list of numbers for plotting.'''
	X=[]
	s=float(abs(u-l)/n)
	for i in range(n+1):
		y=l+s*i
		X.append(y)
	return X

def Graph():
	''' To design the axes and assign scale'''
	plt.xticks(GN(-25,25,50))
	plt.yticks(GN(-25,25,50))
	plt.xlim(-25,25)
	plt.ylim(-25,25)

def MM(A,B):
	''' Multiplies two matrices and returns the product matrix.'''
	C=[[0 for x in range(len(B[0]))] for y in range(len(A))]
	for i in range(len(A)):
		for j in range(len(B[0])):
			for k in range(len(B)):
				C[i][j]=C[i][j]+A[i][k]*B[k][j]
	return C

class Shape():
	'''Base Class'''
	def Draw(self):
		''' Draws the required shape.'''
		plt.clf()							# To remove previous figure
		Graph()								# To draw the axes
		plt.grid()
		plt.plot(self.X+[self.X[0]],self.Y+[self.Y[0]])

	def Transform(self,T):
		''' To transform all points of the shape.'''
		for i in range(len(self.X)):
			V=[[self.X[i]],[self.Y[i]],[1]]
			V1=MM(T,V)								
			self.X[i],self.Y[i]=round(V1[0][0],2),round(V1[1][0],2)	#Assigning New Coordinates.
		if(type(self) is Polygon):
			print("New X Coordinates: ",self.X)
			print("New Y Coordinates: ",self.Y)		
		if(type(self) is Disc):
			z=[]
			V1=MM(T,[[self.a],[self.b],[1]])
			self.a,self.b=V1[0][0],V1[1][0]							#New Center
			for i in range(len(self.X)):
				z.append((( (self.X[i]-self.a)**2 + (self.Y[i]-self.b)**2 )**0.5))
			print("New Centre: (%2.2f,%2.2f)" %(self.a,self.b))
			print("r1: %2.2f"%(max(z)))			
			print("r2: %2.2f"%(min(z)))

	def Rotate(self,o):
		''' Rotates the shape by an angle o about the origin in counter-clockwise direction.'''
		ot=(o*m.pi)/180
		T =[[m.cos(ot),-m.sin(ot),0],[m.sin(ot), m.cos(ot),0],[0,0,1]]
		self.Transform(T)
		self.Draw()

	def Scale(self,x,y):
		'''Scales the Shape:-
			- By factor x along x-axis
			- By factor y along y-axis'''
		T=[[x,0,0],[0,y,0],[0,0,1]]
		self.Transform(T)
		self.Draw()

	def Translate(self,dx,dy):
		'''Translates the Shape:-
			- By amount dx along x-axis
			- By amount dy along y-axis'''
		T=[[1,0,dx],[0,1,dy],[0,0,1]]
		self.Transform(T)
		self.Draw()

class Polygon(Shape):
	def __init__(self,X,Y):
		''' Initialises the vertices of polygon.'''
		self.X=X
		self.Y=Y

class Disc(Shape):
	def __init__(self,a,b,r):
		''' Initialises the parameters of Disc.'''
		n=GN(0,m.pi*2,360)
		if r<0:
			raise Exception("Radius can't be negative!")
		self.a=a
		self.b=b
		self.X=[a+r*m.cos(i) for i in n]
		self.Y=[b+r*m.sin(i) for i in n]

if __name__ == '__main__':
	GS=input("Choose A Shape (Disc/Polygon)\n")
	f=1
	if GS=='Disc':
		a,b,r=map(float,input("Enter Coordinates Of Centre & Radius:-\n").split())
		S=Disc(a,b,r)
		plt.figure(figsize=(15,15), dpi=50)
		S.Draw()
	elif GS=='Polygon':
		X=list(map(float,input("Enter X Coordinates: ").split()))
		Y=list(map(float,input("Enter Y Coordinates: ").split()))
		S=Polygon(X,Y)
		plt.figure(figsize=(15,15), dpi=50)		
		S.Draw()		
	else:
		print("Invalid Choice!")
		f=0

	while f:
		Q=input().split()
		if Q[0]=='quit':
			break
		elif Q[0]=='R':
			o=float(Q[1])
			S.Rotate(o)
		elif Q[0]=='S':
			x,y=float(Q[1]),float(Q[2])
			S.Scale(x,y)
		elif Q[0]=='T':
			dx,dy=float(Q[1]),float(Q[2])
			S.Translate(dx,dy)
		else:
			print("Invalid Query")
			continue
