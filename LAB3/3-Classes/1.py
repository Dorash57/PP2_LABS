#1
class Person:
    def __init__(self, n):
        self.name = n

    def inp(self):
        self.n = input()

    def __str__(self):
        print(self.n.upper())
noname = Person("Me")
noname.inp()
noname.__str__()

#2
class Shape:
    def area(self, a=0):
        print(a)

class Square(Shape):
    def __init__(self, length):
        self.l=length
s = Square(5465)
s.area()

#3
class Rectangle(Shape):
    def __init__(self, length, width):
        self.l=length
        self.w=width
    def area(self):
        return self.l*self.w
    
r=Rectangle(12 ,5)
print(r.area())

#4
class Point:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    
    def show(self):
        print(self.x, self.y)
    
    def move(self):
        x1=int(input("Move x by units: "))
        y1=int(input("Move y by units: "))
        self.x+=x1
        self.y+=y1
        print(f"New coordinates ({self.x}, {self.y})")

    def dist (self, point_2):
        x2 = point_2.x
        y2 = point_2.y
        return ((self.x-x2)**2 + (self.y-y2)**2)**0.5
p1 = Point(1, 1)
p1.show()
p1.move()
p2 = Point(1,1)
p2.show()
print(p1.dist(p2))

#5
class Account:
    def __init__(self, owner, balance):
        self.o = owner
        self.b = balance
    
    def deposit(self):
        self.b=self.b+(self.b*(5/100))
        print(self.b)

    def withdraw(self):
        w=int(input())
        if w<=self.b:
            self.b=self.b-w
            print(self.b)
        else:
            print("Not enough money")

o1=Account("me", 50000)
o1.deposit()
o1.withdraw()

#6
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]
prime_numbers = list(filter(lambda x : is_prime(x), numbers))
print(*prime_numbers)