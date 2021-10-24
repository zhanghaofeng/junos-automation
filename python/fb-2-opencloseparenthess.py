
def printBalancedParenthess(string):
    open, close = 0, 0
    result = ''

    for char in string:
        result += char
        if char == '(':
            open += 1
        if char == ')':
            close += 1
        
        if close > open:
            result = '(' + result
            open += 1
    while open > close:
        result += ')'
        close += 1
    
    return result
if __name__ == '__main__':

    testString = '()('

    res = printBalancedParenthess(testString)
    print(res)
