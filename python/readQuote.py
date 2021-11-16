import os, random

def genSeed(filename):
    fSize = os.path.getsize(filename)
    return random.randrange(fSize)

def getQuote(filename, seed):
    f = open(filename)
    f.seek(seed)
    line = f.readline().strip()

    while line and line != '%':
        line = f.readline().strip()
    
    line = f.readline()
    res = ''
    while line and line.strip() != '%':
        res += line
        line = f.readline()

    if line.strip() == '%':
        return res
    else:
        return None

def main():
    filename= 'quote.txt'
    seed = genSeed(filename)
    res = getQuote(filename, seed)
    while not res:
        seed = genSeed(filename)
        res = getQuote(filename, seed)
    print(res)

if __name__ == '__main__':
    main()