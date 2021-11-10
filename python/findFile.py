import os, re

class findName():
    def __init__(self, path='.', name='.*', recursive=False) -> None:
        self.path = path
        self.name = name
        self.recursive = recursive
        self.data = self.init_data()
        # print(self.data)

    def init_data(self):
        res = list()
        if self.recursive:
            fullPath = os.walk(self.path)
            for root,dir,filename in fullPath:
                # print(root, dir, filename)
                for name in filename:
                    name = root + '/' + name
                    res.append(name)
        else:
            fullPath = os.listdir(self.path)
            for i in fullPath:
                res.append(i)
        return res       

    def byName(self, name):
        res = []
        for i in self.data:
            if re.search(name, i):
                res.append(i)
        return res
    def BiggerThanSize(self, size):
        res = dict()
        for i in self.data:
            if os.path.getsize(i) >= size:
                res[i] = os.path.getsize(i)
        return res

if __name__ == '__main__':
    mySearch = findName(recursive=True)
    res = mySearch.byName('wechat')
    print(res)
    res = mySearch.BiggerThanSize(5000)
    print(res)