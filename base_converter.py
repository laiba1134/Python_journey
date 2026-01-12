number = input("Enter the number you want to convert: ")
base = int(input("Enter the current base of the number: "))
other_base = int(input("Enter the base you want to convert the number into: "))

# Step 1: Convert the input number to decimal
decimal = 0
power = 0

# Start from the rightmost digit
i = len(number) - 1
while i >= 0:
    digit = number[i]
    
    # Find the numeric value of this digit
    if digit == '0':
        digit_value = 0
    elif digit == '1':
        digit_value = 1
    elif digit == '2':
        digit_value = 2
    elif digit == '3':
        digit_value = 3
    elif digit == '4':
        digit_value = 4
    elif digit == '5':
        digit_value = 5
    elif digit == '6':
        digit_value = 6
    elif digit == '7':
        digit_value = 7
    elif digit == '8':
        digit_value = 8
    elif digit == '9':
        digit_value = 9
    else:
        # For letters A-F (hexadecimal and higher bases)
        if digit == 'A' or digit == 'a':
            digit_value = 10
        elif digit == 'B' or digit == 'b':
            digit_value = 11
        elif digit == 'C' or digit == 'c':
            digit_value = 12
        elif digit == 'D' or digit == 'd':
            digit_value = 13
        elif digit == 'E' or digit == 'e':
            digit_value = 14
        elif digit == 'F' or digit == 'f':
            digit_value = 15
    
    # Calculate the value of this digit in decimal
    # For example: in binary 101, rightmost 1 is 1*(2^0), next 0 is 0*(2^1), leftmost 1 is 1*(2^2)
    position_value = 1
    count = 0
    while count < power:
        position_value = position_value * base
        count = count + 1
    
    decimal = decimal + (digit_value * position_value)
    
    power = power + 1
    i = i - 1

print("Decimal value:", decimal)

# Step 2: Convert decimal to the target base
result = ""
temp = decimal

if temp == 0:
    result = "0"
else:
    while temp > 0:
        remainder = temp % other_base
        
        # Convert remainder to appropriate character
        if remainder == 0:
            digit_char = '0'
        elif remainder == 1:
            digit_char = '1'
        elif remainder == 2:
            digit_char = '2'
        elif remainder == 3:
            digit_char = '3'
        elif remainder == 4:
            digit_char = '4'
        elif remainder == 5:
            digit_char = '5'
        elif remainder == 6:
            digit_char = '6'
        elif remainder == 7:
            digit_char = '7'
        elif remainder == 8:
            digit_char = '8'
        elif remainder == 9:
            digit_char = '9'
        elif remainder == 10:
            digit_char = 'A'
        elif remainder == 11:
            digit_char = 'B'
        elif remainder == 12:
            digit_char = 'C'
        elif remainder == 13:
            digit_char = 'D'
        elif remainder == 14:
            digit_char = 'E'
        elif remainder == 15:
            digit_char = 'F'
        
        # Add this digit to the front of our result
        result = digit_char + result
        
        # Divide by the base for next iteration
        temp = temp // other_base

print("Result:", number, "(base", base, ") =", result, "(base", other_base, ")")