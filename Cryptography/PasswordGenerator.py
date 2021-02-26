# Anuneet Anand
# FCS Assignment - 1 : [2a]
# Password Generator

from random import choice

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

PlainText = input()
PlainText = PlainText.upper()
CipherText = ""

# Generating password by randomly substituting each character with a similar looking character.
for character in PlainText:
	CipherText += choice(P[character])

print(CipherText)

# END OF CODE
# Glyph References : https://simple.wikipedia.org/wiki/Leet