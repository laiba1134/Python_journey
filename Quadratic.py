# Equation of form ax^2 + bx + c = 0

while True:
    a = float(input("Enter coefficient a: "))

    if a == 0:
        print("This is not a quadratic equation (a cannot be 0).")
        continue

    b = float(input("Enter coefficient b: "))
    c = float(input("Enter coefficient c: "))

    # Calculate discriminant
    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        root1 = (-b + discriminant**0.5) / (2*a)
        root2 = (-b - discriminant**0.5) / (2*a)
        print(f"Real and distinct roots: {root1} and {root2}")

    elif discriminant == 0:
        root = -b / (2*a)
        print(f"Real and equal roots: {root}")

    else:
        real_part = -b / (2*a)
        imag_part = (abs(discriminant)**0.5) / (2*a)
        print(f"Complex roots: {real_part} + {imag_part}i and {real_part} - {imag_part}i")

    choice = input("Do you want to solve another equation? (y/n): ")
    if choice.lower() != 'y':
        break
