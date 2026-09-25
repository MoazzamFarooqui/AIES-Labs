product1_name=input("Enter product 1 name:")
product1_qty=int(input("Enter product 1 quantity:"))
product1_price=int(input("Enter price of product 1:"))

product2_name=input("Enter product 2 name:")
product2_qty=int(input("Enter product 2 quantity:"))
product2_price=int(input("Enter price of product 2:"))

product3_name=input("Enter product 3 name:")
product3_qty=int(input("Enter product 3 quantity:"))
product3_price=int(input("Enter price of product 3:"))

totalbill=(product1_qty*product1_price)+(product2_qty*product2_price)+(product3_qty*product3_price)
print("Total bill=",totalbill)

