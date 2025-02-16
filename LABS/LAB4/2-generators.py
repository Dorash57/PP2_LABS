#1 
def kvadrat_generator(san):
    for x in range(1 , san+1):
        yield x ** 2
        
n = int(input())
for answer in kvadrat_generator(n):
    print(answer , end=" ")

#2 
def even_numbers(san):
    for x in range (0 , san+1):
        if x%2==0:
            yield x

n = int(input())
print(", ".join(map(str, even_numbers(n))))

#3 
def divisible_3_and_4(san):
    for x in range(0 , san+1):
        if x % 12 ==0:
            yield x
n = int(input())
print(" ".join(map(str ,divisible_3_and_4(n))))

#4
def square_numbers_a_b(a , b):
    for x in range (a , b+1):
        yield x ** 2 
a2 , b2 =map(int , input().split())
print(" ".join(map(str ,square_numbers_a_b(a2,b2))))

#5 

def returns_all_numbers(san):
    for x in range(san , -1 , -1):
        yield x
n = int(input())
print(" ".join(map(str ,returns_all_numbers(n))))
