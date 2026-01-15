nums = [1, 2, 3, 1, 2, 4]

nums.sort()  # in-place

i = 0
while i < len(nums):
    if i == len(nums) - 1 or nums[i] != nums[i + 1]:
        print(nums[i], "does not repeat")
        i += 1
    else:
        i += 2
