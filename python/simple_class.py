
class returnMax():
    def __init__(self) -> None:
        self.myList = []
    def pushValue(self, input):
        self.myList.append(input)
    def printList(self):
        print(self.myList)
    def returnMaxValue(self):
        return max(self.myList)

if __name__ == '__main__':
    mymax = returnMax()
    mymax.pushValue(0)
    mymax.pushValue(3)
    mymax.pushValue(10)
    mymax.pushValue(20)
    mymax.printList()
    print(mymax.returnMaxValue())

