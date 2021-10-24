k = 10
num = 20

for i in range(2 ** k):
    num_str = "{i:0{num}b}".format(i=i, num=num)
    print(num_str)

'''
class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        for i in range(2 ** k):
            num_str = "{i:0{num}b}".format(i=i, num=k)
            if num_str not in s:
                return False
        else:
            return True

class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        need = 1 << k
        got = set()

        for i in range(k, len(s)+1):
            tmp = s[i-k:i]
            if tmp not in got:
                got.add(tmp)
                need -= 1
                # return True when found all occurrences
                if need == 0:
                    return True
        return False
'''