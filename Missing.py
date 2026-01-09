size = int(input("Enter the size of array: "))
arr = []

for i in range(size):
    arr.append(int(input(f"Enter element {i + 1}: ")))

arr.sort()

missing = []

for i in range(len(arr) - 1):
    if arr[i + 1] - arr[i] > 1:
        for num in range(arr[i] + 1, arr[i + 1]):
            missing.append(num)

if not missing:
    print("No number is missing inside the given list.")
else:
    print("Missing number(s):", missing)
# This code takes an array of integers as input, sorts it, and finds any missing integers in the sequence.