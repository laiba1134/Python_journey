#checking if a number is Armstrong number or not
def armstrong(number):
    num_str = str(number)
    power = len(num_str)
    total = 0
    for d in num_str:
        total += int(d) ** power
    return total == number
while True: 
    number = int(input("Enter a number: "))
    if armstrong(number):
        print("Armstrong number ")
        choice = input("Do you want to check another number? (y/n): ")
        if choice.lower() == 'y':
            continue
        else:
            break
    else:
        print("Not an Armstrong number ")
        break
