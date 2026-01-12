# forward right  triangle
x = "*"
for i in range(1, 5):
    print(x*i)

# backward right triangle
print("\n")
x = "*"
n = 4
for i in range(n, 0 ,-1):
    print(x*i)

# equilateral triangle
print("\n")
x = "*"
n = 4
for i in range(1, n + 1):
    print(" " * (n - i) + x * (2 * i - 1))
    
