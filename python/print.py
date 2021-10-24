
# X is a list
x = [ 1, 2, 3, 4, 5]

x[2] = 222
for i in x:
    print("i is {}".format(i))

print(type(x))

# Y is a tuple

y = (1, 2, 3, 4, 6)

for i in y:
    print("i is {}". format(i))

print(type(y))

for i in range(5):
    print("i is {}". format(i))
print(type(range(5)))

# z is a dic

z = { 'name': 'zhang', 'age': 41, 'career':'Engineer' }

for i,j in z.items():
    print('z is {}, {}'. format(i,j))
print(type(z))
print(id(z))

if isinstance(z, tuple):
    print("Yes")
else:
    print("No")

hungrey = False

x = "I am hungery" if hungrey else "I am not hungery"
print(x)

x = 0x0a

print("Hex is {}". format(x))

while x > 0:
    print(x)
    x -= 1

def main():
    '''
    f =  open("test.log")

    for line in f:
        line = line.rstrip()
        print(".", end='', flush=True)
        #print(line)
    '''
    count  = 1
    nums = [ 1, 0, 1]
    for i in nums:
        print(f"Count number is {count}")
        print(f"Value i is {i}")

        if len(nums) == 1:
            return i
        else:
            nums.remove(i)
            if i in nums:
                nums.remove(i)
                
        print(nums)
        count += 1

if __name__ == "__main__":
    print("*** This is Main ***")
    result = main()
    print(result)
