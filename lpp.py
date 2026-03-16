import numpy as np 
import matplotlib.pyplot as plt 
 
 
print("Objective Function: Z = c1*x + c2*y") 
 
c1 = int(input("Enter c1: ")) 
c2 = int(input("Enter c2: ")) 
constraints = [] 
n = int(input("\nEnter number of constraints: ")) 
for i in range(n): 
  print("\nConstraint", i+1) 
  a = int(input("Enter a: ")) 
  b = int(input("Enter b: ")) 
  sign = input("Enter sign (<= or >=): ") 
  c = int(input("Enter c: ")) 
  constraints.append((a, b, sign, c)) 
x = np.linspace(0, 50, 400) 
lines = [] 
plt.figure() 
for a, b, sign, c in constraints: 
  if b != 0: 
    y = (c - a*x)/b 
    plt.plot(x, y) 
  lines.append((a, b, c)) 
 
 
lower = np.zeros(len(x)) 
upper = np.ones(len(x)) * 50 
 
for a, b, sign, c in constraints: 
   if b != 0: 
       y = (c - a*x)/b 
       if sign == "<=": 
           upper = np.minimum(upper, y) 
       else: 
           lower = np.maximum(lower, y) 
 
plt.fill_between(x, lower, upper, where=(upper >= lower), alpha=0.3) 
 
 
def feasible(xp, yp): 
   for a, b, sign, c in constraints: 
       val = a*xp + b*yp 
       if sign == "<=" and val > c: 
           return False 
       if sign == ">=" and val < c: 
           return False 
 
   return True 
 
 
corner = [] 
 
 
for i in range(len(lines)): 
   a1, b1, c1_ = lines[i] 
   for j in range(i+1, len(lines)): 
       a2, b2, c2_ = lines[j] 
       det = a1*b2 - a2*b1 
       if det != 0:   # not parallel 
           x_int = (c1_*b2 - c2_*b1) / det 
           y_int = (a1*c2_ - a2*c1_) / det 
           if x_int >= 0 and y_int >= 0: 
               if feasible(x_int, y_int): 
                   corner.append((x_int, y_int)) 
 
 
for a, b, c in lines: 
   if a != 0: 
       x_int = c/a 
       if x_int >= 0 and feasible(x_int, 0): 
 
           corner.append((x_int, 0)) 
   if b != 0: 
       y_int = c/b 
       if y_int >= 0 and feasible(0, y_int): 
           corner.append((0, y_int)) 
 
 
if len(corner) == 0: 
   print("\nNo feasible solution") 
   plt.show() 
   exit() 
 
 
Zmax = None 
best_points = [] 
 
print("\n") 
 
for xp, yp in corner: 
   Z = c1*xp + c2*yp 
   print("(" + str(round(xp,2)) + "," + str(round(yp,2)) + ") ->", round(Z,2)) 
 
   plt.scatter(xp, yp, color="red") 
 
   plt.text(xp+0.2, yp+0.2, "(" + str(round(xp,1)) + "," + str(round(yp,1)) + 
")") 
 
   if Zmax is None or Z > Zmax: 
       Zmax = Z 
       best_points = [(xp, yp)] 
   elif Z == Zmax: 
       best_points.append((xp, yp)) 
 
 
if len(best_points) == 1: 
   print("\nUnique Optimal Solution") 
   print("Point:", (round(best_points[0][0],2), round(best_points[0][1],2))) 
   print("Maximum Z =", round(Zmax,2)) 
else: 
   print("\nMultiple Optimal Solutions") 
   print("Maximum Z =", round(Zmax,2)) 
   print("Corner Points:") 
   for p in best_points: 
       print((round(p[0],2), round(p[1],2))) 
 
 
plt.xlim(0, 20) 
 
plt.ylim(0, 15) 
plt.xlabel("x") 
plt.ylabel("y") 
plt.grid() 
plt.show()
