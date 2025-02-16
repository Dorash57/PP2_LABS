#1 
import math 

a = float(input("Input degree: "))
print(f"Output radian: {math.radians(a)}")

#2 

height = float(input("Height: "))
fv = float(input("Base, first value: "))
sv = float(input("Base, second value: "))
print("Expected Output:",height * ((fv+sv)/2))

#3 
import math 

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
tan_value = math.tan(math.pi/n)

area = (n * s **2  ) / (4 * tan_value) 
print (f"The area of the polygon is: {area:.6f} ")

#4 
a = float(input("Length of base: "))
b = float(input("Height of parallelogram: "))
print("Expected Output:" , a*b)