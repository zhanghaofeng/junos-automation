
class returnMax():
    def __init__(self, input) -> None:
        self.myList = input

    def returnMax(self):
        return max(self.myList)

if __name__ == '__main__':
    input = [1,3,2,3,4,10]
    mymax = returnMax(input)
    print(mymax.returnMax())
