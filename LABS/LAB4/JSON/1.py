import json 
file_path=r"C:\Users\doras\OneDrive\Рабочий стол\PP2_LABARATORIKA\LABS\LAB4\JSON\sample-data.json"
with open(file_path, "r") as jfile:
    x = json.load(jfile)

print("Interface Status")
print("="*81)
print(f'{"DN":<50} {"Description":<15} {"Speed":<8} {"MTU":<6}')
print("-"*48+" "+"-"*15+" "+"-"*9+" "+"-"*6)

for i in x["imdata"]:
    attributes = i["l1PhysIf"]["attributes"]
    print(f'{attributes["dn"]:<50} {attributes["descr"]:<14} {attributes["speed"]:<9} {attributes["mtu"]}')