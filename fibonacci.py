# Fibonacci series using recursion
def fibonacci(n):
    if n == 0: 
        return 0
    elif n == 1:
        return 1 
    else:
        return fibonacci(n-1) + fibonacci(n-2)   
terms = int(input("Enter the number of terms you want to calculate fibonacci series of: "))
for i in range(terms):
    print(fibonacci(i), end=" ")
# iterative method
def fibonacci_iterative(n):
    a = 0
    b = 1
    for _ in range(n):
        print(a, end=" ")
        b = a + b
        a = b - a
terms = int(input("\nEnter the number of terms you want to calculate fibonacci series of (iterative): "))
fibonacci_iterative(terms)