while True:
    value = input("Enter the string you want to verify if its palindrom or not: ")
    reverse = value[::-1]
    print(reverse)
    if reverse == value:
        print("The string is palindrom!")
    else:
        print("The string is not palindrom!")
        choice = input("Do you want to verify another string? ")
        if choice == "No" or choice == "no":
            print("Exiting the string ")
            break
        continue
        
    
        
        


