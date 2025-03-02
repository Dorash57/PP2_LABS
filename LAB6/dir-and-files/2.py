import os
path=r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LAB6"
allDirs = os.listdir(path)
for item in allDirs:
    if  os.path.isfile(os.path.join(path,item)):
        print(f"only file= {item}")