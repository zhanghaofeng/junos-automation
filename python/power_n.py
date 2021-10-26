
# Runtime Complexity: O(n)

def power(x, n):
    if n == 0: return 1
    res = 1
    for i in range(n):
        res = res * x
    return res

def power2(x, n):
    if n == 0: return 1
    else:
        return x * power(x, n-1)

def power3(x, n):
    
    res = 1 if n % 2 == 0 else x
    while n >= 2:
        print(res)
        res = res * x * x
        n = n // 2
    return res

if __name__ == '__main__':
    # print(power(2,5))
    # print(power2(2,5))
    print(power3(1.5, 3))