# Anuneet Anand
# FCS Assignment - 1 : [2b]
# Dictionary Attack

from itertools import product
# Change for large n
# import sys
# sys.setrecursionlimit(10**5)

# Similar looking characters for substitution
P = {
	"A":["4","@","A","a"],
	"B":["8","6","B","b"],
	"C":["<", "{", "[", "(","C","c"],
	"D":["D","d"],
	"E":["3","E","e"],
	"F":["F","f"],
	"G":["6","[","G","g"],
	"H":["4","#","H","h"],
	"I":["|","1","!","I","i"],
	"J":["J","j"],
	"K":["K","k"],
	"L":["1","|","L","l"],
	"M":["M","m"],
	"N":["N","n"],
	"O":["0","O","o"],
	"P":["P","p"],
	"Q":["9","0","Q","q"],
	"R":["R","r"],
	"S":["5","$","S","s"],
	"T":["7","+","T","t"],
	"U":["U","u"],
	"V":["V","v"],
	"W":["W","w"],
	"X":["%","X","x"],
	"Y":["Y","y"],
	"Z":["2","5","Z","z"],
	}

LIMIT = 15

Words = {}
Passwords = {}
for i in range(LIMIT+1):
	Words[i]=[]
	Passwords[i]=[]

# Generates all possible passwords recursively
def Gen(Words,Passwords,z):
	if z == 0:								# Zero length passwords not possible.
		return []

	elif z == 1:							# Trivial Case
		for i in Words[z]:
			Passwords[z]+=P[i]
		return Passwords[z]

	elif len(Passwords[z]):					# Memoization
		return Passwords[z]

	else:
		if len(Words[z]):					# Generate passwords using words of length z.
			for text in Words[z]:
				Temp = []
				for i in text:
					Temp.append("".join(s for s in P[i]))
				X = set([''.join(s) for s in list(product(*Temp))])
				Passwords[z] += list(X)

		else:								# Generate passwords using words of length z/2 and (z+1)/2 and concate them.
			R = set()

			if len(Passwords[z//2]):
				R1 = Passwords[z//2]
			else:
				R1 = Gen(Words,Passwords,z//2)

			if len(Passwords[(z+1)//2]):
				R2 = Passwords[(z+1)//2]
			else:
				R2 = Gen(Words,Passwords,(z+1)//2)

			for x in R1:					# Concatenating word = word1.word2
				for y in R2:
					R.add(x+y)
					R.add(y+x)

			Passwords[z] = list(R)

		return Passwords[z]

# Max Valid Value = 15
n = int(input())

# Reading dictionary file for words.
with open("dictionary.txt","r") as Input_File:
	List = Input_File.readlines()
	for word in List:
		text = word.strip()
		text = text.upper()
		if 0<len(text)<LIMIT+1:
			Words[len(text)].append(text)

# Generating Possible Passwords
PasswordsList = Gen(Words,Passwords,n)
PasswordsList = list(set(PasswordsList))
PasswordsList.sort()

# Storing in file
with open("passwords.txt","w") as Output_File:
	for x in PasswordsList:
		Output_File.write(x+"\n")

# END OF CODE
# Word Reference : https://github.com/dolph/dictionary