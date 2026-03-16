import numpy as np
#matrix calculations and arrya handling
print("Maximize Z = a*x + b*y")
#this prints message for user.
a = float(input("Enter coefficient of x: "))
b = float(input("Enter coefficient of y: "))
#user enters objective functions
n = int(input("Enter number of constraints: "))
#user enters number of constraints.
A = []
B = []
#these are empty lists. A-coefficient and B-RhS values
for i in range(n):
#looop runs n times
    print("\nConstraint", i+1)
#constraint 1,2,3
    c = float(input("Enter coefficient of x: "))
    d = float(input("Enter coefficient of y: "))
    e = float(input("Enter RHS: "))
#user enters constraints
    A.append([c,d])
    B.append(e)
#stores values
A = np.array(A) #convert list to numpy array
B = np.array(B) #same conversion
table = []
#empty list to store simplex table
for i in range(n):
#loop for each constraint
    row = list(A[i])
#copies constraint row
    slack = [0]*n #creates slack variables
    slack[i] = 1 #makes identity matrix

    row += slack #adds slack to row
    row.append(B[i]) #adds RHS
    table.append(row) #adds row to simplex table

table = np.array(table, dtype=float) #convert table to numpy array

Cj = [a,b] + [0]*n #this creats Cj row.

CB = [0]*n #coefficient of basic variable. initially slack variables. profit=0

def print_table(): #defines function to print simplex table

    print("\nSimplex Table:\n")

    print("CB   Basis ", end="")  #prints heading

    for val in Cj: #prints Cj row
        print(f"{val:8}", end="")

    print("   RHS")

    for i in range(n): #print each row

        print(f"{CB[i]:2}    S{i+1}   ", end="")

        for val in table[i]:
            print(f"{val:8.2f}", end="")

        print()

    Zj = np.zeros(len(Cj)) #creates Zj row

    for i in range(n):
        Zj += CB[i]*table[i,:-1] #formula

    print("\nZj:       ", end="")

    for val in Zj:
        print(f"{val:8.2f}", end="")

    print("\nCj-Zj:    ", end="")

    for i in range(len(Cj)):
        print(f"{Cj[i]-Zj[i]:8.2f}", end="")

while True:

    print_table()

    Zj = np.zeros(len(Cj))

    for i in range(n):
        Zj += CB[i]*table[i,:-1]

    CJ_ZJ = np.array(Cj) - Zj

    if max(CJ_ZJ) <= 0:

        break

    pivot_col = np.argmax(CJ_ZJ)

    ratios = []

    for i in range(n):

        if table[i][pivot_col] > 0:

            ratios.append(table[i][-1]/table[i][pivot_col])

        else:

            ratios.append(9999)

    pivot_row = np.argmin(ratios)

    pivot = table[pivot_row][pivot_col]

    table[pivot_row] = table[pivot_row]/pivot

    for i in range(n):

        if i != pivot_row:

            table[i] -= table[i][pivot_col]*table[pivot_row]

    CB[pivot_row] = Cj[pivot_col]

print("\nOptimal Solution Found\n")

for i in range(n):

    print(f"Variable in basis row {i+1} value =",table[i][-1])

Z = sum(CB[i]*table[i][-1] for i in range(n))

print("Maximum Z =",Z)
