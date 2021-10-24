import re

# re.search() searches a string, and return the start index and end index for the result
# return None if not find
# the r char means a raw string. not regex

# s = 'GeeksforGeeks: A computer science 123 portal for geeks 321'

# regex = '\d+.*?'
# match = re.findall(regex, s)   # return a LIST
# print(match)

# p = re.compile('[a-e]')
# m = p.findall('Aye, Said Mr. Gilbon Start') # return a list
# print(m)

# # re.split(regex, string, maxsplit=0, flag=0)

# s = 'ae92            up    up   from b1 to c1 2'
# match = re.split('\s+', s, maxsplit=3, flags=re.IGNORECASE) # return a list
# print(match)

# print(re.sub('\sAND\s', ' & ', 'Baked AND beans AND Spams',count=3)) # return a string

# t = re.subn(r'\sAND\s', ' && ', 'Beans AND bakers AND spames') # return a turple
# print(t)

regex = r'[a-zA-Z]+ \d+'
s = 'My Birthday is Sep 13'

Match = re.search(regex,s) # if there is a match, match.group() returns the matched string
print(Match.group())

print(Match.groups())

for i in Match.groups():  # match.groups() return a list
    print(i)


# re.match searchs from the beginning, but re.search searchs from anyplace. 

s = 'I love dogs'
print(re.match(r'. dogs', s))

print(re.search(r'. dogs', s))

