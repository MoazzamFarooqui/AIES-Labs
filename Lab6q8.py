number1=int(input("Enter number 1:"))
number2=int(input("Enter number 2:"))

def swap(number1,number2):
    return number2,number1

number1,number2=swap(number1,number2)

print("After swapping:")
print("Number 1:",number1)
print("Number 2:",number2)

