import numpy as np #import library

def print_tableau(tableau, n, m): #function to print simplex tableau
    print("\nSimplex Tableau:") #print title
    
    header = [] #create column header list
    for i in range(n):
        header.append(f"x{i+1}") #add decision variables
    for i in range(m):
        header.append(f"s{i+1}")  #add slack variables
    header.append("RHS") #add RHS column

    print(" | ".join(header)) #print header

    for row in tableau:
        print(" | ".join(f"{val:.2f}" for val in row)) #loops through each row og the tableau, val:.2f prints values up to 2 decimal places

n = int(input("Enter number of variables: "))
m = int(input("Enter number of constraints: "))

print("Enter coefficients of objective function:")
c = list(map(float, input().split()))

A = [] #stores coefficients of variables
b = [] #stores RHS values

print("Enter coefficients of constraints:")
for i in range(m): #runs for each constraint.
    row = list(map(float, input(f"Constraint {i+1}: ").split())) #input row
    A.append(row[:-1])  #store coefficients
    b.append(row[-1])    #store RHS
    
tableau = [] #create tableau, this matrix will store the simplex table

# Add constraints + slack variables
for i in range(m):
    row = A[i] + [0]*m + [b[i]] #create row
    row[n+i] = 1   # Slack variable
    tableau.append(row) #add row to tableau

# Add objective function row
tableau.append([-x for x in c] + [0]*(m+1))

iteration = 1

while True:

    print(f"\nIteration {iteration}")
    print_tableau(tableau, n, m) #print current tableau

    last_row = tableau[-1] #objective row
    pivot_col = last_row.index(min(last_row[:-1])) #select pivot column

    if last_row[pivot_col] >= 0: #optimality check
        break

    ratios = [] #compute ratios
    for i in range(m): #calculate ratio test
        if tableau[i][pivot_col] > 0: #avoid division by zero
            ratios.append(tableau[i][-1] / tableau[i][pivot_col]) #ratio formula
        else:
            ratios.append(float('inf')) #invalid ratios ignored

    pivot_row = ratios.index(min(ratios)) #find pivot row

    pivot_element = tableau[pivot_row][pivot_col] #pivot element

    # Normalise pivot row
    for j in range(len(tableau[0])):
        tableau[pivot_row][j] /= pivot_element #make pivot element equal to 1.
 
    # Make other elements zero
    for i in range(m+1):
        if i != pivot_row: #skip pivot row
            factor = tableau[i][pivot_col] #calculate factor
            for j in range(len(tableau[0])): 
                tableau[i][j] -= factor * tableau[pivot_row][j] #row operation

    iteration += 1 #increase iteration

print("\nFinal Optimal Table:")
print_tableau(tableau, n, m) # print final table
print("\nOptimal Value =", tableau[-1][-1]) #print optimal value
