item1=float(input("Enter price of food item 1:"))
item2=float(input("Enter price of food item 2:"))
item3=float(input("Enter price of food item 3:"))

subtotal=item1+item2+item3
service_charge=0.05*subtotal
total=subtotal+service_charge

print("Final bill is:",total)

