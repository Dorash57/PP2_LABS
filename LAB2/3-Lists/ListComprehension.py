fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

newlist = [x for x in fruits if "a" in x]

print(newlist)

# The Syntax
# newlist = [expression for item in iterable if condition == True]

# You can use the range() function to create an iterable:
newlist = [x for x in range(10)]

# Set all values in the new list to 'hello':
newlist = ['hello' for x in fruits]

# Accept only numbers lower than 5:
newlist = [x for x in range(10) if x < 5]