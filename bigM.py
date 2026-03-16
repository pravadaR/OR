import numpy as np   # Import numpy library for numerical operations

M = 1000   # Large penalty value used in Big-M method for artificial variables
# Function to print the simplex tableau neatly
def print_tableau(tableau):
    print("\nSimplex Tableau:")  # Print heading

    for row in tableau:  # Loop through each row of tableau
        print(["{:.2f}".format(x) for x in row])  # Print each value upto 2 decimal places
# Input number of decision variables
n = int(input("Enter number of variables: "))

# Input number of constraints
m = int(input("Enter number of constraints: "))
# Input coefficients of the objective function
print("Enter coefficients of objective function:")
c = list(map(float, input().split()))   # Example input: 3 5

A = []   # Matrix to store coefficients of variables in constraints
b = []   # List to store RHS values
signs = []  # List to store inequality signs (<=, >=, =)

# Input constraints from the user
print("Enter constraints (a b sign c)")
for i in range(m):
    data = input(f"Constraint {i+1}: ").split()   # Example input: 1 2 <= 8
    row = list(map(float, data[:-2]))  # Extract coefficients of variables
    sign = data[-2]  # Extract inequality sign
    rhs = float(data[-1])  # Extract RHS value
    A.append(row)   # Store variable coefficients
    b.append(rhs)   # Store RHS
    signs.append(sign)  # Store constraint type

tableau = []   # Create empty simplex tableau
# Add slack, surplus and artificial variables
for i in range(m):
    row = A[i] + [0]*m + [0]*m + [b[i]]
    # Structure:
    # [decision variables | slack variables | artificial variables | RHS]
    if signs[i] == "<=":  # For ≤ constraint
        row[n+i] = 1  # Add slack variable

    elif signs[i] == ">=":  # For ≥ constraint
        row[n+i] = -1  # Add surplus variable
        row[n+m+i] = 1  # Add artificial variable

    elif signs[i] == "=":  # For equality constraint
        row[n+m+i] = 1  # Add artificial variable

    tableau.append(row)  # Add row to tableau
# Create objective function row
obj = [-x for x in c] + [0]*(2*m+1)
# Negative because simplex maximisation uses -Z
# Add penalty for artificial variables
for i in range(m):
    if signs[i] != "<=":   # If artificial variable exists
        obj[n+m+i] = -M   # Add large penalty (-M)
tableau.append(obj)  # Add objective row to tableau

# Start Simplex iterations
while True:
    print_tableau(tableau)  # Display current tableau
    last_row = tableau[-1]  # Get objective function row
    pivot_col = last_row.index(min(last_row[:-1]))
    # Choose the column with the most negative value
    # If no negative value → optimal solution found
    if last_row[pivot_col] >= 0:
        break
    ratios = []  # Store ratios for minimum ratio test
  
    for i in range(m):
        if tableau[i][pivot_col] > 0:  # Only positive pivot column values allowed
            ratios.append(tableau[i][-1] / tableau[i][pivot_col])  # RHS / pivot column
        else:
            ratios.append(float('inf'))  # Ignore invalid ratios
    pivot_row = ratios.index(min(ratios))  # Choose smallest ratio
    pivot = tableau[pivot_row][pivot_col]  # Pivot element
    # Normalise pivot row (make pivot element = 1)
    for j in range(len(tableau[0])):
        tableau[pivot_row][j] /= pivot

    # Make pivot column values zero in other rows
    for i in range(len(tableau)):
        if i != pivot_row:  # Skip pivot row
            factor = tableau[i][pivot_col]
            for j in range(len(tableau[0])):
                tableau[i][j] -= factor * tableau[pivot_row][j]

# Print optimal value of the objective function
print("\nOptimal Value =", tableau[-1][-1])
