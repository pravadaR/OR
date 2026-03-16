import numpy as np

def print_tableau(tableau, n, m):
    print("\nSimplex Tableau:")
    
    header = []
    for i in range(n):
        header.append(f"x{i+1}")
    for i in range(m):
        header.append(f"s{i+1}")
    header.append("RHS")

    print(" | ".join(header))

    for row in tableau:
        print(" | ".join(f"{val:.2f}" for val in row))

n = int(input("Enter number of variables: "))
m = int(input("Enter number of constraints: "))

print("Enter coefficients of objective function:")
c = list(map(float, input().split()))

A = []
b = []

print("Enter coefficients of constraints:")
for i in range(m):
    row = list(map(float, input(f"Constraint {i+1}: ").split()))
    A.append(row[:-1])  
    b.append(row[-1])    


tableau = []

# Add constraints + slack variables
for i in range(m):
    row = A[i] + [0]*m + [b[i]]
    row[n+i] = 1   # Slack variable
    tableau.append(row)

# Add objective function row
tableau.append([-x for x in c] + [0]*(m+1))

iteration = 1

while True:

    print(f"\nIteration {iteration}")
    print_tableau(tableau, n, m)

    last_row = tableau[-1]
    pivot_col = last_row.index(min(last_row[:-1]))

    if last_row[pivot_col] >= 0:
        break

    ratios = []
    for i in range(m):
        if tableau[i][pivot_col] > 0:
            ratios.append(tableau[i][-1] / tableau[i][pivot_col])
        else:
            ratios.append(float('inf'))

    pivot_row = ratios.index(min(ratios))

    pivot_element = tableau[pivot_row][pivot_col]

    # Normalize pivot row
    for j in range(len(tableau[0])):
        tableau[pivot_row][j] /= pivot_element

    # Make other elements zero
    for i in range(m+1):
        if i != pivot_row:
            factor = tableau[i][pivot_col]
            for j in range(len(tableau[0])):
                tableau[i][j] -= factor * tableau[pivot_row][j]

    iteration += 1


print("\nFinal Optimal Table:")
print_tableau(tableau, n, m)
print("\nOptimal Value =", tableau[-1][-1])
