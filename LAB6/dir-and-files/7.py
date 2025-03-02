file_path=r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LAB6"
file_copy=r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LAB6\dir-and-files\7.py"
with open(file_path,"r") as file:
    content=file.read()
    with open(file_copy,"w") as copy:
        copy.write(content)