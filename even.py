# Finding if a number is even or odd using basic logic
while True:
    n = int(input("Enter a positive number: "))

    if n < 0:
        print("Please enter a positive number.")
        continue
    temp = n

    while temp > 1:
        temp -= 2
    if temp == 0:
        print(f"{n} is an even number")
    else:
        print(f"{n} is an odd number")
    break
# using mode operator
while True:
    num = int(input("Enter a number: "))
    if num < 0:
        print("Please enter a non-negative number.")
        continue
    if num % 2 == 0:
        print(f"{num} is an even number")
        break
    else:
        print(f"{num} is an odd number")
        break
# using bitwise operator
while True:
    num = int(input("Enter a number: "))
    if num < 0:
        print("Please enter a non-negative number.")
        continue
    if num & 1 == 0:
        print(f"{num} is an even number")
        break
    else:
        print(f"{num} is an odd number")
        break
    
