file_path=r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LAB6"
array=["orange","banana","pineapple"]

with open(file_path,"w") as file:
    for item in array:
        file.write(item+" ")