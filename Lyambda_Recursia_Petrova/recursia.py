# №1
def f1(n):
    if n == 1:
        return 1
    return n * f1(n-1)
print(f1(6))

# №2
def f2(n):
    x = 1
    for i in range(2,n+1):
        x *= i
    return x
print(f2(6))

# №3
def f3(l: list) -> list:
    for i in range(len(l)):
        l[i] = l[i]**2
    return l
print(f3([2,3,4,5,6,7,8,9]))
