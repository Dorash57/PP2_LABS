import re 

# 1 
def match_string(s):
    pattern = r'^as*b$'
    if re.match(pattern ,s):
        return True
    return False

strings = ["ab" , "asb" , "assb" , "asssb" , "acb" , "abbb"]

for x in strings:
    if match_string(x):
        print(f"followed '{x}' ")
    else :
        print(f"does not followed '{x}' ")

# 2 
def my_fucntion (s):
    y = r'^ab{2,3}$'
    if re.match(y , s):
        return True
    return False

strings = ["abb" , "abbb"  , "aabb" , "a" , "abbbb" , "ab"]

for x in strings:
    if my_fucntion(x):
        print(f"Followed , '{x}' ")
    else :
        print(f"Does not Followed , '{x}' ")

# 3 
def my_func(s):
    res = r'^[a-z]+_[a-z]+$'
    if re.match(res , s):
        return True 
    return False

strings = [ "Hello" , "1213asd" , "as_df" , "as-df"]

for x in strings:
    if my_func(x):
        print(f"Followed '{x}'")
    else:
        print(f"Does not Followed '{x}' ")


# 4

def example_4(s):
    sequences=r'^[A-Z]{1}[a-z]+$'

    if re.match(sequences , s):
        return True 
    return False

strings = [ "Hello" , "1213asd" , "As_df" , "Dima" , "python" ,"HEllo"]

for x in strings:
    if example_4(x):
        print(f"Followed '{x}'")
    else:
        print(f"Does not Followed '{x}' ")

# 5
def example_5(s):
    matematika = r'^a.*ab$'
    if re.match(matematika , s):
        return True 
    return False

strings = [ "aab" , "ab" , "asdfggab" , "a22341ab" , "ab" ,"abfd"]

for x in strings:
    if example_5(x):
        print(f"Followed '{x}'")
    else:
        print(f"Does not Followed '{x}' ")

# 6

txt = "Almaty and Astana , Atyrau they are big city.Also they are very beautifully"
x = re.sub("[ ,.]" , ":" , txt )
print(x)

# 7 

dxt = input()

words = dxt.split("_")
camel_case = words[0] + "".join(word.capitalize() for word in words[1:])

print(camel_case)

# 8 

axt = input()

x = re.split(r'(?=[A-Z])', axt)

x = list(filter(None, x))
print(x)

# 9 

dvd = input()

x = re.sub(r'(?<!^)([A-Z])', r' \1', dvd)
print(x)


#10 

keys = input()

x = re.sub(r'(?<!^)([A-Z])', r'_\1',keys ).lower()
print(x)
