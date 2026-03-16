import numpy as np #used for mathematical operations and arrays
import matplotlib.pyplot as plt #used for drawing graphs
 
print("Objective Function: Z = c1*x + c2*y") #displays obj dunction format to the user.
 
c1 = int(input("Enter c1: ")) 
c2 = int(input("Enter c2: ")) #user inputs the coefficients.
constraints = []  #(a,b,sign,c)
n = int(input("\nEnter number of constraints: ")) #user enters number of constraints.
for i in range(n): #loop n times to take each constraint
  print("\nConstraint", i+1) 
  a = int(input("Enter a: ")) 
  b = int(input("Enter b: ")) 
  sign = input("Enter sign (<= or >=): ") #ineuality sign
  c = int(input("Enter c: ")) 
  constraints.append((a, b, sign, c)) #store constraint
x = np.linspace(0, 50, 400)  #create X values for graph creates 400 values of x b/w 0 and 50.
lines = []  # stores equations for later intersection calculations.
plt.figure() #starts a new plot figure
for a, b, sign, c in constraints: #loop through each constraint
  if b != 0: #avoid division by zero
    y = (c - a*x)/b #convert eq to y form
    plt.plot(x, y) #draws the constraint line on graph
  lines.append((a, b, c)) #stores eq for intersection calculations.
 
lower = np.zeros(len(x)) 
upper = np.ones(len(x)) * 50 #used for shading feasible region.
 
for a, b, sign, c in constraints: 
   if b != 0: 
       y = (c - a*x)/b 
       if sign == "<=": 
           upper = np.minimum(upper, y) #feasible region lies below line.
       else: 
           lower = np.maximum(lower, y) #feasible region lines above line.
 
plt.fill_between(x, lower, upper, where=(upper >= lower), alpha=0.3) #shades feasible area.
 
def feasible(xp, yp): #checks whether a point satisfies all constraints.
   for a, b, sign, c in constraints: 
       val = a*xp + b*yp #substitute point into equation
       if sign == "<=" and val > c: 
           return False #if violated->not feasible
       if sign == ">=" and val < c: 
           return False #point is feasible
 
   return True #point is feasible
 
corner = [] #stores all feasible intersection points
 
for i in range(len(lines)): #loop through first line.
   a1, b1, c1_ = lines[i] 
   for j in range(i+1, len(lines)): #find inersections between lines
       a2, b2, c2_ = lines[j] 
       det = a1*b2 - a2*b1 
       if det != 0:   # not parallel 
           x_int = (c1_*b2 - c2_*b1) / det 
           y_int = (a1*c2_ - a2*c1_) / det 
           if x_int >= 0 and y_int >= 0: #check first quadrant
               if feasible(x_int, y_int): #only keep valid points
                   corner.append((x_int, y_int)) #store corner point
 
for a, b, c in lines: 
   if a != 0: 
       x_int = c/a #check axis 
       if x_int >= 0 and feasible(x_int, 0): 
 
           corner.append((x_int, 0)) 
   if b != 0: 
       y_int = c/b 
       if y_int >= 0 and feasible(0, y_int): 
           corner.append((0, y_int)) 
 
if len(corner) == 0: #if no feasible region
   print("\nNo feasible solution") 
   plt.show() 
   exit() 
 
Zmax = None # initialise max Z
best_points = [] #stores optimal value and points
 
print("\n") 
 
for xp, yp in corner: #loop through corner points
   Z = c1*xp + c2*yp #objective func
   print("(" + str(round(xp,2)) + "," + str(round(yp,2)) + ") ->", round(Z,2)) #print result
 
   plt.scatter(xp, yp, color="red") #plot corner point
 
   plt.text(xp+0.2, yp+0.2, "(" + str(round(xp,1)) + "," + str(round(yp,1)) + ")")  #label point
 
   if Zmax is None or Z > Zmax: #update max
       Zmax = Z 
       best_points = [(xp, yp)] 
   elif Z == Zmax: 
       best_points.append((xp, yp)) #multiple optimal sol
 
if len(best_points) == 1: 
   print("\nUnique Optimal Solution") #unique sol
   print("Point:", (round(best_points[0][0],2), round(best_points[0][1],2))) #print iptimal point
   print("Maximum Z =", round(Zmax,2)) #print max z value
else: 
   print("\nMultiple Optimal Solutions")  #multiple optimal soln
   print("Maximum Z =", round(Zmax,2))  #print max value
   print("Corner Points:") #print heading
   for p in best_points: #loop through all optimal points
       print((round(p[0],2), round(p[1],2))) #print each optimal point
 
plt.xlim(0, 20) 
plt.ylim(0, 15) 
plt.xlabel("x") 
plt.ylabel("y") 
plt.grid() 
plt.show()
