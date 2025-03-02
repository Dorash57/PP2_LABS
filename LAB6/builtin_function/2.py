a=input()
big=0
small=0
for i in range(len(a)):
    if (a[i].isupper()):
        big+=1
    else:
        small+=1
print("Big letters",big,"Small letters",small)