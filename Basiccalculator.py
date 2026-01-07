def subtract(no_1,no_2):
    return no_1 - no_2
def addition(no_1,no_2):
    return no_1 + no_2
def multiplication(no_1,no_2):
    return no_1 * no_2
def division(no_1,no_2):
    return no_1/no_2
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
        print("Welcome to Basic Calculator!")
        print("Select operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")
        choice = input("Enter choice(1/2/3/4/5): ")
        if choice == '5':
            print("Exiting calculator. Goodbye!")
            break  # Exit immediately
        elif choice in ['1','2','3','4']:
            no_1 = get_numbers("Enter first number: \n")
            if choice == '4':
                no_2 = get_numbers("Enter second number: \n", allow_zero=False)
            else:
                no_2 = get_numbers("Enter second number: \n")
            if choice == '1':
                print(f"{no_1} + {no_2} = {addition(no_1,no_2)}")
            elif choice == '2':
                print(f"{no_1} - {no_2} = {subtract(no_1,no_2)}")
            elif choice == '3':
                print(f"{no_1} * {no_2} = {multiplication(no_1,no_2)}")
            elif choice == '4':
                print(f"{no_1} / {no_2} = {division(no_1,no_2)}")
        else:
            print("Invalid Input")
if __name__ == "__main__":
    calculator()