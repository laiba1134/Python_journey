#Program to verify the validity of a credit card number using the Luhn algorithm
def luhn_check(number):
    for ch in number:
        if not ch.isdigit() and ch != ' ':
            return False
    # Remove spaces
    number = number.replace(' ', '')
    # length check
    if len(number) != 16:
        return False
    total = 0
    reverse = number[::-1]
    for i in range(len(reverse)):
        digit = int(reverse[i])
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0
while True:
    card_no = input("Enter credit card number with spaces: ")
    if luhn_check(card_no):
        print("Valid credit card number ✅")
        choice = input("Do you want to check another number? (y/n): ")
        if choice.lower() == 'y':
            continue
        else:
            break
    else:
        print("Invalid credit card number ❌")