# https://leetcode.com/problems/license-key-formatting/
# list.insert() is expensive. Try to use append and reverse the string in the end. 

class Solution:
    def licenseKeyFormatting(self, s: str, k: int) -> str:
        res = []
        s = s.replace('-', '')
        for index,value in enumerate(s[::-1]):
            if (index+1) % k == 0 and index != len(s)-1:
                res.append(value.upper())
                res.append('-')
            else:
                res.append(value.upper())
        
        return ''.join(res)[::-1]