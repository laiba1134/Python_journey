def modulus(x1,x2):
    return x1 % x2
def floor_division(x1,x2):
    return x1 // x2
def power(x1,x2):
    return x1 ** x2
def square_root(x):
    return x ** 0.5
def absolute_value(x):
    if x < 0:
        return x
    elif x > 0:
        return x
    elif x == 0:
        return 0
    else:
        return "Invalid Input"
def get_numbers(value, allow_zero = True):
    while True:
        try:
            num = float(input(value))
            if not allow_zero and num == 0:
                print("Error! Division by Zero. Enter valid number")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
def calculator():
    while True:
        print("Welcome to Advanced Calculator!")
        print("Select operation:")
        print("1. Modulus")
        print("2. Floor Division")
        print("3. Power")
        print("4. Square Root")
        print("5. Absolute Value")
        print("6. Exit")
        choice = input("Enter choice(1,2,3,4,5,6): ")
        if choice == '6':
            print("Exiting calculator. Goodbye!")
            break  # Exit immediately
        elif choice in ['1','2','3']:
            no_1 = get_numbers("Enter first number: \n")
            no_2 = get_numbers("Enter second number: \n")
            if choice == '1':
                print(f"{no_1} % {no_2} = {modulus(no_1,no_2)}")
            elif choice == '2':
                print(f"{no_1} // {no_2} = {floor_division(no_1,no_2)}")
            elif choice == '3':
                print(f"{no_1} ** {no_2} = {power(no_1,no_2)}")
        elif choice == '4':
            no = get_numbers("Enter number to find square root: \n", allow_zero=False)
            print(f"Square root of {no} = {square_root(no)}")
        elif choice == '5':
            no = get_numbers("Enter number to find absolute value: \n")
            print(f"Absolute value of {no} = {absolute_value(no)}")
        else:
            print("Invalid Input")
if __name__ == "__main__":
    calculator()