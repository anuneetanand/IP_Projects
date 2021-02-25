# CSE112: Computer Organisation
# ASSEMBLER PROJECT
# Anuneet Anand (2018022)
# Pankil Kalra (2018061)

def Bin(x):
	''' Converts A Decimal Number To It's 8-Bit Binary Representation'''
	B = ""
	while x:
		B = str(x%2) + B
		x = x // 2
	while len(B)<8:
		B = "0" + B
	return B

def Check_Int(x):
	''' Checks Whether The Data Is An Integer'''
	try:
		int(x)
		return True
	except ValueError:
		return False

OPCODE = {"CLA": "0000", "LAC": "0001", "SAC": "0010", "ADD": "0011", "SUB": "0100", "BRZ": "0101", "BRN": "0110", "BRP": "0111", "INP": "1000", "DSP": "1001", "MUL": "1010", "DIV": "1011", "STP": "1100"}
ASSEMBLY_CODE = []
MACHINE_CODE = []
JUNK = []
COMMENTS = []
MEMORY = {}
ERROR_LOG = [[] for i in range(10000)]
ERROR_FLAG = False
MEMORY_LIMIT_FLAG = False
STP_FLAG = False
Stp_List = []

'''
 Reading Assembly Code From Text File
 Assumptions :-
 - File name is "AssemblyCode.txt" and exists in current directory.
 - Code & Comments are separated using "//". Only single line comments allowed and "//" can't appear in comment body.
 - Code consist of single-space separated Opcodes,Symbols & Addresses.
'''
with open('AssemblyCode.txt','r') as Input_File:
	Data = Input_File.readlines()
	Location_Counter = 0
	Data = [Line for Line in Data if Line.strip()]				# Ignoring empty lines
	for Line in Data:										
		if Line.count("//")==0 :
			Code, Comment = Line,""
		elif Line.count("//")==1 :                     
			x = Line.find("//")
			Code, Comment = Line[:x],Line[x+2:]
			Code = Code.lstrip()
		else:
			Code , Comment = "" , ""
			ERROR_FLAG = True
			ERROR_LOG[Location_Counter].append("Invalid Comment Declaration")
		if Code!="":
			Raw_Code = Code.split()					
			Formatted_Code = ["","",""]
			Junk_Code = []
			for i in range(min(3,len(Raw_Code))):		# Collecting parts of code
				Formatted_Code[i]=Raw_Code[i]
			for i in range(3,len(Raw_Code)):			# Separating undefined part of code
				Junk_Code.append(Raw_Code[i])
			ASSEMBLY_CODE.append(Formatted_Code)
			JUNK.append(Junk_Code)
			Location_Counter += 1						# Updating Location Counter
		COMMENTS.append(Comment)
Input_File.close()

# Checking For Junk & Undefined Input
for i in range(Location_Counter):
	if JUNK[i]!=[]:
		ERROR_FLAG = True
		ERROR_LOG[i].append("Invalid Symbols Detected/Received More Operands Than Expected")

# Initialising Tables
OpCode_Table = [[] for i in range(Location_Counter)]
Symbol_Table = {"LABEL":["" for i in range(Location_Counter)] , "VARIABLE":["" for i in range(Location_Counter)]}
Label_Table = ["" for i in range(Location_Counter)]
Memory_Used = [0 for i in range(256)]						# 8-Bit Memory Addresses

'''
FIRST PASS :-
 - Assembly Code is processed line by line.
 - Opcodes, Symbols, Variables, Literals & Addresses are extracted and stored in respective tables.
 - Appropiate errors are displayed when less/more operands are supplied or opcodes are invalid.
''' 

# Checking For Memory Given To Instructions
if Location_Counter>255:
	MEMORY_LIMIT_FLAG = True
else:
	for i in range(Location_Counter):
		Memory_Used[i]=1
	for i in range(Location_Counter):
		S = ASSEMBLY_CODE[i]
		j = 0
		if S[0] in OPCODE.keys() and S[2]=="":																			# First Token is Opcode
			j=1
		elif ":" in S[0]:																					# First Token is Label
			Label_Table[i]=S[0][:-1]
			j=2
		else:
			ERROR_FLAG = True
			ERROR_LOG[i].append("Invalid Opcode/Label")
		if (j==1 or j==2):
			if S[j-1] in OPCODE.keys():
				OpCode_Table[i].append(S[j-1])																# Opcode
				if S[j-1] == "STP":
					Stp_List.append(i)
				if S[j]!="":
					if S[j] in OPCODE.keys():
						ERROR_FLAG = True
						ERROR_LOG[i].append("Multiple Opcodes Detected In One Instruction")
					elif S[j-1] in ["CLA","STP"]:
						ERROR_FLAG = True
						ERROR_LOG[i].append("Invalid Symbols Detected/Received More Operands Than Expected")
					elif (ord(str(S[j][0]))>=65 and ord(str(S[j][0]))<=90) or (ord(str(S[j][0]))>=97 and ord(str(S[j][0]))<=122):
						if S[j-1] in ["BRN","BRZ","BRP"]:													# Branch Labels
							Symbol_Table["LABEL"][i]=S[j]
						else:
							Symbol_Table["VARIABLE"][i]=S[j]												# Variables
							OpCode_Table[i].append(S[j])
					else:
						ERROR_FLAG = True
						ERROR_LOG[i].append("Invalid Label/Variable Declaration")
				else:
					if S[j-1] not in ["CLA","STP"]:
						ERROR_FLAG = True
						ERROR_LOG[i].append("Missing Symbols/Received Less Operands Than Expected")
			else:
				ERROR_FLAG = True
				ERROR_LOG[i].append("Invalid Opcode")

	# Assigning Memory To Variables
	for i in range(Location_Counter):
		Variable = Symbol_Table["VARIABLE"][i]
		if Variable!="":
			if 0 in Memory_Used:
				x = Memory_Used.index(0)
				Memory_Used[x] = 1
				MEMORY[Variable] = x
			else:
				MEMORY_LIMIT_FLAG = True

	# Resolving Labels
	for i in range(Location_Counter):
		Label = Symbol_Table["LABEL"][i]
		if Label!="":
			if Label in Label_Table:
				MEMORY[Label] = Label_Table.index(Label)
			else:
				ERROR_FLAG = True
				ERROR_LOG[i].append("Can't Resolve Label "+Label)

for i in range(Location_Counter):
	if Symbol_Table["VARIABLE"][i]!="" and Symbol_Table["VARIABLE"][i] in Label_Table:
		ERROR_FLAG = True
		ERROR_LOG[i].append("Invalid Variable. Clashes with a Label")

if len(Stp_List)!=1:
	STP_FLAG= True
else:
	i = Stp_List[-1]
	for j in range(i+1,Location_Counter):
		if OpCode_Table[j]!=[]:
			STP_FLAG = True
ERROR_FLAG = ERROR_FLAG or STP_FLAG or MEMORY_LIMIT_FLAG
'''
SECOND PASS :-
 - If no errors are detected, the assembly instructions are translated to machine code.
 - The tables populated during the first pass are used.
 - Appropriate substitution for labels & variables is made.
 - Machine code is written into the the file "MachineCode.txt" (new line character is used to enhance readability)
 - The various tables generated during first pass and memory mapping is displayed as output on the terminal.
'''
if ERROR_FLAG == False:
	for i in range(Location_Counter):
		M = OPCODE[OpCode_Table[i][0]]
		Label = Symbol_Table["LABEL"][i]
		Variable = Symbol_Table["VARIABLE"][i]
		if Label!="":
			M = M + Bin(int(MEMORY[Label]))
		elif Variable!="":
			M = M + Bin(int(MEMORY[Variable]))
		else:
			M = M + Bin(0)
		MACHINE_CODE.append(M)

	# Writing Machine Code To Text File
	with open('MachineCode.txt','w') as Output_File:
		for i in range(Location_Counter):
			Output_File.write(MACHINE_CODE[i]+"\n")
	Output_File.close()

	# Generated Tables & Memory Allocation
	print("\n"+"	>>> OPCODE TABLE <<<"+"\n")
	print("Line	OpCode 	Operand")
	for i in range(Location_Counter):
		s = ""
		for j in OpCode_Table[i]:
			s = s + j +"	"
		print(i,"	",s,end="	")
		print()

	print("\n"+"	>>> SYMBOL TABLE <<<" +"\n")
	print("Line	Label 	Variable")
	for i in range(Location_Counter):
		print(i,"	",Symbol_Table["LABEL"][i],"	",Symbol_Table["VARIABLE"][i])

	print("\n"+"	>>> COMMENTS <<<" +"\n")
	print("Line		Comment")
	for i in range(Location_Counter):
		print(i,"		",COMMENTS[i])

	print("\n"+" >>> MEMORY MAPPING <<<" +"\n")
	for i in range(Location_Counter):
		print(" ",Bin(i),OpCode_Table[i][0])
	for i in MEMORY:
		if i in Symbol_Table["VARIABLE"]:
			print(" ",Bin(MEMORY[i]),i)
else:
	# Displaying Errors Linewise
	print("ERROR REPORT!")
	for i in range(Location_Counter):
		if len(ERROR_LOG[i]):				
			print("Line",i+1,":",end="")
			for j in ERROR_LOG[i]:
				print(j)
	if(STP_FLAG):
		print("Not Able To Resolve STP")
	if(MEMORY_LIMIT_FLAG):
		print("Memory Limit Exceeded")

# END OF CODE
