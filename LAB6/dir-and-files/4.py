file_path=r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LAB6"
with open(file_path,"r") as a:
    line_counter=len(a.readlines())
print(line_counter)