# Ex 1
def read_int():
    return int(input())

grams = read_int()
ounces = 28.3495231 * grams 
print(ounces)

# Ex 2

def temp(fahren):
    cels=(5/9)*(fahren-32)
    print(cels)
temp(13)

#Ex 3
def farm():
    a = int(input())
    b = int(input())
    return a , b 
heads , legs = farm()
rab=(legs-2*heads)//2
chick=heads-rab
print("chicken =", chick, "rabbits =", rab)

# Ex 4 
def filter_prime(numbers):
    return [x for x in numbers if all(x % i != 0 for i in range(2, int(x**0.5) + 1)) and x > 1]

numbers = list(map(int, input().split()))
print(filter_prime(numbers))

#x 5
from itertools import permutations
st = input()
list1= list(permutations(st))
for x in list1:
    print(x)

#x 6 
def reversed(s):
    return ' '.join(s.split()[::-1])

s = input()
print(reversed(s))

#x 7
def has_33(nums):
    
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i+1] == 3:
            return True
    return False

print(has_33([1, 3, 3]))  # True
print(has_33([1, 3, 1, 3]))  # False
print(has_33([3, 1, 3]))  # False


#Ex 8
a = list(map(int, input().split()))

def func(a):
    l = len(a)
    for i in range(l):
        if a[i]==0:
            for j in range(i+1, l):
                if a[j]==0:
                    for x in range(j+1, l):
                         match(a[x]):
                               case 0: return False
                               case 7: return True
    return False
print(func(a))

#Ex 9

def volume(rad):
    print(4/3 * 3.14 * rad**3)
rad = int(input())
volume(rad)

#Ex 10
def unique(m):
    ans = []
    for i in m:
        if ans.count(i) == 0: 
            ans.append(i)
    return ans

a = list(map(int , input().split())) 
print(unique(a))

#Ex 11

def ispalindrom(word):
    copy = word[::-1]
    if copy == word:
        return True
    return False
word = input()
print(ispalindrom(word))
print(ispalindrom("abbad")) # false
print(ispalindrom("abba")) #true

#Ex 12
def histogram(arr):
    for i in arr:
        
        print('*' * i)
brr = list(map(int,input().split()))
(histogram(brr))


#Ex 13 
import random
def guess():
    number= random.randint(1, 21)
    name = input("Hello! What is your name?\n")
    print(f"Well, {name}, I am thinking of a number between 1 and 20.\n")
    count = 0
    for i in range(20):
        count +=1
        x = int(input("Take a guess.\n"))
        if x < number:
            print("Your guess is too low.\n")
        elif x > number:
            print("Your guess is too high.")
        elif x == number:
            print(f"Good job, {name}, You guessed my number in {count} guesses!")
            break
    
guess()