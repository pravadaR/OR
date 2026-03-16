import numpy as np   # Import numpy library for numerical calculations
# Function to print simplex tableau
def print_tableau(tableau):
    print("\nTableau:")
    for row in tableau:   # Loop through each row
        print(["{:.2f}".format(x) for x in row])   # Print values upto 2 decimals

# Input number of decision variables
n = int(input("Enter number of variables: "))
# Input number of constraints
m = int(input("Enter number of constraints: "))

# Input coefficients of original objective function
print("Enter objective coefficients:")
c = list(map(float, input().split()))   # Example: 3 5
A = []   # Matrix to store coefficients of variables in constraints
b = []   # RHS values
# Input constraints
print("Enter constraints (a b c):")
for i in range(m):
    row = list(map(float, input(f"Constraint {i+1}: ").split()))
    # Example input: 1 2 8
    A.append(row[:-1])   # Store coefficients of variables
    b.append(row[-1])    # Store RHS value

tableau = []   # Create empty simplex tableau
# Add artificial variables for Phase I
for i in range(m):
    row = A[i] + [0]*m + [b[i]]
    # Structure:
    # [decision variables | artificial variables | RHS]
    row[n+i] = 1   # Add artificial variable
    tableau.append(row)   # Add row to tableau
  
# Create Phase-I objective function
tableau.append([0]*n + [1]*m + [0])
# Minimise the sum of artificial variables
print("\nPhase I: Finding Feasible Solution")
# Phase-I Simplex iterations
while True:
    print_tableau(tableau)   # Print current tableau
    last = tableau[-1]   # Get objective function row

    pivot_col = last.index(max(last[:-1]))
    # Choose column with the largest positive value
    # If no positive value → optimal solution for Phase-I
    if last[pivot_col] <= 0:
        break
    ratios = []   # Store ratios for minimum ratio test

    for i in range(m):
        if tableau[i][pivot_col] > 0:
            ratios.append(tableau[i][-1] / tableau[i][pivot_col])
        else:
            ratios.append(float('inf'))   # Ignore invalid ratios
    pivot_row = ratios.index(min(ratios))   # Choose smallest ratio
    pivot = tableau[pivot_row][pivot_col]   # Pivot element

    # Normalise pivot row (make pivot element = 1)
    for j in range(len(tableau[0])):
        tableau[pivot_row][j] /= pivot
    # Make pivot column zero in other rows
    for i in range(len(tableau)):
        if i != pivot_row:
            factor = tableau[i][pivot_col]
            for j in range(len(tableau[0])):
                tableau[i][j] -= factor * tableau[pivot_row][j]

print("\nFeasible solution obtained (Artificial variables minimized)")
# Phase-II begins
print("\nPhase II: Optimize Original Objective Function")
# Replace Phase-I objective function with original objective function
tableau[-1] = [-x for x in c] + [0]*(m+1)
# Negative because simplex maximisation uses -Z
print_tableau(tableau)   # Print new tableau
# Final optimal value
print("\nOptimal Value =", tableau[-1][-1])
