password = input("Please set your password: ")

max_attempts = 3

for attempt in range(max_attempts):
    confirm = input("Please enter your password: ")

    if confirm == password:
        print("Password confirmed!")
        break
    else:
        remaining = max_attempts - attempt - 1
        if remaining > 0:
            print(f"Incorrect password! You have {remaining} attempts left.")
else:
    print("Too many incorrect attempts. Access denied.")
