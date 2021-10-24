
mystr = "[ [ { { ( ( ) ) } } ] ][{]}"
my_list = []

def check_balance(mystr):
    for char in mystr:
        if char == " ":
            continue
        if char in "({[":
            my_list.append(char)
        else:
            if my_list == []:
                return False
            elif matches(my_list[-1],char):
                my_list.pop()
            else:
                return False

    if my_list == []:
        return True
    else:
        return False

def matches(open, close):
    openers = "({["
    closers = ")}]"

    print(open, close)

    return openers.index(open) == closers.index(close)

print(check_balance(mystr))