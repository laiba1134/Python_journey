PI = 3.141592653589793
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def to_radians(degrees):
    return degrees * (PI / 180)

def sine(degrees, terms=10):
    x = to_radians(degrees)
    sin_x = 0
    for i in range(terms):
        sign = (-1) ** i
        sin_x += sign * (x ** (2*i + 1)) / factorial(2*i + 1)
    return sin_x

def cosine(degrees, terms=10):
    x = to_radians(degrees)
    cos_x = 0
    for i in range(terms):
        sign = (-1) ** i
        cos_x += sign * (x ** (2*i)) / factorial(2*i)
    return cos_x

def tangent(degrees):
    cos_val = cosine(degrees)
    if abs(cos_val) < 0.00001:
        return "Error: Tangent undefined"
    return sine(degrees) / cos_val
while True:
    print("\n--- Custom Trigonometry Calculator ---")
    print("1. sin")
    print("2. cos")
    print("3. tan")
    print("4. exit")

    choice = input("Select option: ")

    if choice == '4':
        break

    angle = float(input("Enter angle in degrees: "))

    if choice == '1':
        print("sin(", angle, ") =", sine(angle))
    elif choice == '2':
        print("cos(", angle, ") =", cosine(angle))
    elif choice == '3':
        print("tan(", angle, ") =", tangent(angle))
    else:
        print("Invalid option")

