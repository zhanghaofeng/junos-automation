
def moveZerotoLeft(input):
    total =  input.count(0)

    for i in range(total):
        temp = input[i:]
        index = temp.index(0)
        input.pop(index+i)
        input.insert(0, 0)
    #[0, 1, 10, 20, 59, 63, 0, 88, 0]
    #[0, 0, 1, 10, 20, 59, 63, 88, 0]

if __name__ == '__main__':
    input = [1, 10, 20, 0, 59, 63, 0, 88, 0]
    moveZerotoLeft(input)
    print(input)