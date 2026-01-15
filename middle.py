def insert():
    size = int(input("Enter the size of the list: "))
    n = []
    for i in range(size):
        val = int(input("Enter a number: "))
        n.append(val)
    return n
n = insert()

t = 0   # turtle (slow)
r = 0   # rabbit (fast)
end = len(n) - 1

while r < end and r + 1 <= end:
    t += 1
    r += 2

# Decision layer
if r == end:
    print(f"Middle element: {n[t]}")
else:
    print(f"Middle elements: {n[t-1]} and {n[t]}")
