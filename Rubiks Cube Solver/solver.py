# Anuneet Anand (2018022)
# Rhythm Patel (2018083)
# ADA Programming Assingment : 2
# Use Python 2

import rubik
import time
from collections import deque

# To convert name of move to it's tuple
X = {"F": rubik.F, "Fi": rubik.Fi, "L": rubik.L,
     "Li": rubik.Li, "U": rubik.U, "Ui": rubik.Ui}

'''
For Question 1, using BFS, find the shortest path from
start_position to end_position. Returns a list of moves.
You can use the rubik.quarter_twists move set. 
Each move can be applied using rubik.perm_apply() 
'''


def shortest_path(start, end):
    M = []													# Moves
    P = {start: "START"}									# Parent
    Q = deque()												# Queue
    F = False												# Flag

    if start == end:
        return M

    Q.append(start)
    while len(Q) > 0 and F == False:						# BFS
        x = Q.popleft()

        for i in range(6):
            p = rubik.quarter_twists[i]
            y = rubik.perm_apply(p, x)

            if y not in P:
                Q.append(y)
                P[y] = i

            if y == end:
                F = True
                break

    if F == False:											# Back-Tracking to generate solution
        M = None
    else:
        z = end
        while P[z] != "START":
            c = rubik.quarter_twists[P[z]]

            if P[z] % 2 == 0:								# F, L, U
                n = rubik.quarter_twists[P[z]+1]
            else:											# Fi, Li, Ui
                n = rubik.quarter_twists[P[z]-1]

            M.append(rubik.quarter_twists_names[c])
            z = rubik.perm_apply(n, z)

    if (M != None):
        M = M[::-1]

    return M


'''
For Question 2, using 2-way BFS, 
find the shortest path from start_position to end_position. 
Returns a list of moves.
You can use the rubik.quarter_twists move set. 
Each move can be applied using rubik.perm_apply
'''


def shortest_path_optmized(start, end):
    M = []													# Moves
    P_start = {start: "START"}								# Parent for BFS from start
    P_end = {end: "END"}									# Parent for BFS from end
    Q_start = deque()										# Queue for BFS from start
    Q_end = deque()											# Queue for BFS from end
    middle = 0												# Intersection Point

    if start == end:
        return M

    Q_start.append(start)
    Q_end.append(end)

    while len(Q_start) > 0 and len(Q_end) > 0 and middle == 0:
        x_start = Q_start.popleft()
        x_end = Q_end.popleft()

        for i in range(6):									# BFS from start
            p = rubik.quarter_twists[i]
            y_start = rubik.perm_apply(p, x_start)

            if y_start not in P_start:
                Q_start.append(y_start)
                P_start[y_start] = i

            if y_start in P_end:
                middle = y_start
                break

        for i in range(6):									# BFS from end
            p = rubik.quarter_twists[i]
            y_end = rubik.perm_apply(p, x_end)

            if y_end not in P_end:
                Q_end.append(y_end)
                P_end[y_end] = i

            if y_end in P_start:
                middle = y_end
                break

    if middle == 0:											# Back-Tracking to generate solution
        return None
    else:

        z = middle
        while P_start[z] != "START" and P_start[z] != "END":
            c = rubik.quarter_twists[P_start[z]]

            if P_start[z] % 2 == 0:							# F, L, U
                n = rubik.quarter_twists[P_start[z]+1]
            else:											# Fi, Li, Ui
                n = rubik.quarter_twists[P_start[z]-1]

            M.append(rubik.quarter_twists_names[c])
            z = rubik.perm_apply(n, z)

        M = M[::-1]

        z = middle
        while P_end[z] != "END" and P_end[z] != "START":

            if P_end[z] % 2 == 0:							# F, L, U
                n = rubik.quarter_twists[P_end[z]+1]
            else:											# Fi, Li, Ui
                n = rubik.quarter_twists[P_end[z]-1]
            c = n

            M.append(rubik.quarter_twists_names[c])
            z = rubik.perm_apply(n, z)

    return M


'''To verify the solution generated.'''


def verify(start, end, solution):
    if solution is None:
        return
    for i in solution:
        start = rubik.perm_apply(X[i], start)
    if start == end:
        print("Verification: Correct Solution")
    else:
        print("Verification: Incorrect Solution")


'''To Test on some predefined test cases'''


def test():
    print "Running Tests..."
    print ""
    start_points = [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),(6, 7, 8, 0, 1, 2, 9, 10, 11, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),(6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23),(7, 8, 6, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23),(6, 7, 8, 0, 1, 2, 9, 10, 11, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),(7, 8, 6, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)]
    end_points = [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23),(10, 11, 9, 16, 17, 15, 7, 8, 6, 20, 18, 19, 3, 4, 5, 14, 12, 13, 2, 0, 1, 21, 22, 23),(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)]
    
    for i in range(len(start_points)):
        start = start_points[i]
        end = end_points[i]
        print "-----------------------------------------------------------------------------------------------"
        print "Test :" , i+1
        print "Start: ", start
        print "End: ", end
        print "-----------------------------------------------------------------------------------------------"
        solve(start, end)


''' To Solve using both functions and report times'''


def solve(start, end):
    print ""
    print "----------------------- Shortest Path Optimized -----------------------------------------------"
    print ""
    a = time.time()
    moves_optimised = shortest_path_optmized(start, end)
    b = time.time()
    verify(start, end, moves_optimised)
    print moves_optimised
    print "Execution Time Of shortest_path_optmized() :", b-a, "sec"
    print ""

    print "----------------------- Shortest Path ---------------------------------------------------------"
    print ""
    a = time.time()
    moves = shortest_path(start, end)
    b = time.time()
    verify(start, end, moves)
    print moves
    print "Execution Time Of shortest_path():", b-a, "sec"
    print ""
    print "-----------------------------------------------------------------------------------------------"


#test()
start = input()
end = input()
solve(start, end)
