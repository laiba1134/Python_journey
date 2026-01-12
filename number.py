numbers = []
limit = int(input("Enter the lenght of the list! "))
for i in range(limit):
    value = input(f"Enter the {i + 1 } element of list: ")
    numbers.append(value)
print(numbers)
def highest(nums):
    maximum = nums[0]
    for num in nums:
        if num > maximum:
            maximum = num 
    return maximum
def smallest(nums):
    minimum = nums[0]
    for num in nums:
        if num < minimum:
            minimum = num 
    return minimum
print("Highest number in list is: ", highest(numbers))
print("Smallest number in list is: ", smallest(numbers))