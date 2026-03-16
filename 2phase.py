import numpy as np   # Import numpy library

# Function to print the tableau neatly
def print_tableau(tableau):
    print("\nTableau:")
    for row in tableau:
        print(["{:.2f}".format(x) for x in row])   # Print numbers up to 2 decimal places


# Input number of decision variables
n = int(input("Enter number of variables: "))

# Input number of constraints
m = int(input("Enter number of constraints: "))

# Input objective function coefficients
print("Enter objective coefficients:")
c = list(map(float, input().split()))

A = []   # Matrix to store constraint coefficients
b = []   # RHS values

# Input constraints
print("Enter constraints (a b c):")

for i in range(m):
    row = list(map(float, input(f"Constraint {i+1}: ").split()))
    A.append(row[:-1])   # coefficients of variables
    b.append(row[-1])    # RHS value


tableau = []   # Initialize simplex tableau


# -------- PHASE I --------
# Add artificial variables to find feasible solution

for i in range(m):

    row = A[i] + [0]*m + [b[i]]  
    # Structure:
    # [decision variables | artificial variables | RHS]

    row[n+i] = 1   # Add artificial variable

    tableau.append(row)   # Add row to tableau


# Phase-I objective function (minimize sum of artificial variables)
tableau.append([0]*n + [1]*m + [0])


print("\nPhase I: Finding Feasible Solution")

while True:

    print_tableau(tableau)

    last = tableau[-1]   # Last row = objective function

    pivot_col = last.index(max(last[:-1]))   # Choose largest positive value

    if last[pivot_col] <= 0:   # Stop if optimal
        break

    ratios = []

    for i in range(m):
        if tableau[i][pivot_col] > 0:
            ratios.append(tableau[i][-1] / tableau[i][pivot_col])
        else:
            ratios.append(float('inf'))

    pivot_row = ratios.index(min(ratios))   # Minimum ratio rule

    pivot = tableau[pivot_row][pivot_col]   # Pivot element

    # Normalize pivot row
    for j in range(len(tableau[0])):
        tableau[pivot_row][j] /= pivot

    # Make pivot column zero in other rows
    for i in range(len(tableau)):
        if i != pivot_row:
            factor = tableau[i][pivot_col]
            for j in range(len(tableau[0])):
                tableau[i][j] -= factor * tableau[pivot_row][j]


print("\nFeasible solution obtained (Artificial variables minimized)")


# -------- PHASE II --------
# Optimize original objective function

print("\nPhase II: Optimize Original Objective Function")

# Replace Phase-I objective with original objective function
tableau[-1] = [-x for x in c] + [0]*(m+1)

while True:

    print_tableau(tableau)

    last_row = tableau[-1]

    pivot_col = last_row.index(min(last_row[:-1]))   # Most negative value

    if last_row[pivot_col] >= 0:   # Stop if optimal
        break

    ratios = []

    for i in range(m):
        if tableau[i][pivot_col] > 0:
            ratios.append(tableau[i][-1] / tableau[i][pivot_col])
        else:
            ratios.append(float('inf'))

    pivot_row = ratios.index(min(ratios))

    pivot = tableau[pivot_row][pivot_col]

    # Normalize pivot row
    for j in range(len(tableau[0])):
        tableau[pivot_row][j] /= pivot

    # Make pivot column zero in other rows
    for i in range(m+1):
        if i != pivot_row:
            factor = tableau[i][pivot_col]
            for j in range(len(tableau[0])):
                tableau[i][j] -= factor * tableau[pivot_row][j]


# Final optimal value
print("\nOptimal Value =", tableau[-1][-1])
