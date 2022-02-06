# Python Projects

Python based projects done as part of core courses at `IIITD`

## Folder Structure  

```
├── Assembler
│   ├── Assembler.py
│   ├── AssemblyCode.txt
│   ├── Documentation - Assembler.pdf
│   └── MachineCode.txt
├── BetweennessCentrality
│   └── Betweenness_Centrality.py
├── BoothsAlgorithm
│   ├── BA.py
│   ├── Documentation.pdf
│   └── Output.txt
├── Cryptography
│   ├── DictionaryAttack.py
│   ├── PasswordGenerator.py
│   └── dictionary.txt
├── GeometricTransformations
│   └── 2D_Transformations.py
├── ImageProcessing
│   ├── Filtering
│   │   ├── AnuneetAnand_2018022_cameraman.jpg
│   │   ├── AnuneetAnand_2018022_code.py
│   │   ├── AnuneetAnand_2018022_denoiseIm.jpg
│   │   └── AnuneetAnand_2018022_noiseIm.jpg
│   ├── HistogramEqualisation
│   │   ├── AnuneetAnand_2018022_Image.jpg
│   │   └── AnuneetAnand_2018022_code.py
│   ├── Interpolation
│   │   ├── AnuneetAnand_2018022_Image_512x512.bmp
│   │   ├── AnuneetAnand_2018022_Image_64x64.jpg
│   │   └── AnuneetAnand_2018022_code.py
│   └── RGB
│       ├── AnuneetAnand_2018022_Image.jpg
│       ├── AnuneetAnand_2018022_code.py
│       ├── AnuneetAnand_2018022_noiseIm.jpg
│       └── AnuneetAnand_2018022_rgbIm.tif
├── K-MapSolver
│   └── K-Map_Solver.py
├── README.md
├── RubiksCubeSolver
│   ├── rubik.py
│   └── solver.py
└── Weather
    └── Weather.py
```

## Assembler :gear:

A Two Pass Assembler that converts assembly language code into 12-bit machine code. The first 4 bits are reserved for Opcode and remaining 8 bits reserved for Memory. Empty lines are ignored while reading the file and Comments are parsed and collected separately. Memory is first allocated to instructions and then to variables.

```
Number Of Opcodes : 12 
Memory Limit : 256
```

### Syntax Rules

- Empty lines & whitespaces are allowed in code and Tokens should be separated by spaces.
- It is mandatory for a label to start with an alphabet and end with “:”.
- Variable should start with an alphabet.
- Use `//` to write a comment. Note that `//` can’t appear in comment body or in code.

### Errors   

- **Memory Limit Exceeded:** The number of instructions and variables exceed 255.
- **Unable To Resolve Stop:** The assembly code should have exactly one stop and should appear at the end of the code. Any other occurrence of STP is treated as an error.
- **Invalid Comment Declaration:** The comments are not declared as per syntax given.
- **Invalid Opcode/Label:** The assembler detected an invalid Opcode or Label.
- **Invalid Label/Variable Declaration:** The variable or label was not declared as per the syntax provided.
- **Can't Resolve Label L:** A branch instruction with L appeared in the code but no such Label was declared as a marker.

**Collaborator:** [Pankil Kalra](https://github.com/pankilkalra)

## Betweenness Centrality :part_alternation_mark:
Betweenness Centrality is a measure of centrality in a graph based on shortest paths. For every pair of vertices in a connected graph, there exists a shortest path such that either the number of edges that the path passes through or the sum of the weights of the edges is minimized. The betweenness centrality for each vertex is the number of these shortest paths that pass through the vertex. The python code calculates the Standardised Betweenness Centrality and prints top K nodes ordered by Standardised Betweenness Centrality.

## Booths Algorithm :memo:

**Booth’s Multiplication Algorithm:** It multiplies two signed binary numbers in two's complement notation.   
**Non-Restoring Division Algorithm:** It divides two signed binary numbers and produce quotient & remainder.

**Collaborator:** [Pruthwiraj Nanda](https://github.com/pruthwi07) 


## Cryptography :lock:

**`PasswordGenerator.py`** : Generates efficient passwords based from user input passwords.   
**`DictionaryAttack.py`** : Dictionary Attack on passwords.

## Geometric Transformations :o:

Supports Rotate, Scale and Translate operations on Disc and Polygon.

## Image Processing 🖼️

Implementation of Image processing algorithms like Bilinear Interpolation, Histogram Equalisation, Fltering, RGB-HSV Conversion and Denoising

## K-Map Solver :pencil2:

The Karnaugh Map or K-Map is a method of simplifying Boolean algebra expressions.The cells in the K-Map are ordered using the Gray Code. K-Map can be created using either SOP (sum of products) or POS (product of sums).

Implemented Quine-McCluskey and Petrick methods to solve a `4 x 4` K-Map.

**Sample Input**
```
No. of variables: 4
Function: (1,3,7,11,15) d (0,2,5) 
```
**Sample Output**
```
Simplified expression: yz+w’x’ OR yz+w’z
```

## Rubiks Cube Solver :wrench:

Solving 2x2x2 Rubik's cube using BFS

**Sample Input**
```
(6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)
```
**Sample Output**
```
----------------------- Shortest Path Optimized -----------------------------------------------

Verification: Correct Solution
['F', 'F', 'Ui', 'L', 'Ui', 'F', 'Li', 'U', 'Li', 'Fi', 'Li', 'U', 'Li', 'Fi']
Execution Time Of shortest_path_optmized() : 0.121093034744 sec

----------------------- Shortest Path ---------------------------------------------------------

Verification: Correct Solution
['F', 'F', 'Ui', 'L', 'Ui', 'F', 'Li', 'U', 'Li', 'Fi', 'Li', 'U', 'Li', 'Fi']
Execution Time Of shortest_path(): 60.2349081039 sec

-----------------------------------------------------------------------------------------------
```
**Collaborator** [Rhythm Patel](https://github.com/rhythm-patel)

## Weather :sun_behind_small_cloud:
The module takes the location , n (For nth day from today) and time as input from the user and displays
appropiate weather information extracted from a JSON response given by a weather data website.
The concept of string slicing is used to extract required data.
