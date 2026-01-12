number = []
while True:
    num = int(input("Enter a number to add it in list: "))
    number.append(num)
    print("Do you want to add another number? (yes/no)")
    choice = input().lower()
    if choice != "yes":
        break
print("The final list is:", number)
def my_length(number):
    count = 0
    for _ in number:
        count += 1
    return count
print("The length of the list is:", my_length(number))