# https://leetcode.com/problems/valid-palindrome-ii/submissions/ 

class Solution:
    def isPalindrome(self, s:str):
        start, end = 0, len(s)-1
        print(s)
        while start <= end:
            if s[start] != s[end]:
                return False
            else:
                start += 1
                end -=1 
        return True
        
    def validPalindrome(self, s: str) -> bool:
        n = len(s)
        if n == 1: return True
        start, end = 0, n-1
        while start <= end:
            # if s[start] == s[end]:
            #     start += 1
            #     end -= 1
            # elif s[start] == s[end-1] and start <= end-1 and switch:
            #     end -= 1
            #     switch = False
            # elif s[start+1] == s[end] and start+1 <= end and switch:
            #     start += 1
            #     switch = False
            # else: return False
            
            if s[start] == s[end]:
                start += 1
                end -= 1
            else: break
        if self.isPalindrome(s[start:end]):
            return True
        elif self.isPalindrome(s[start+1:end+1]):
            return True
        else: return False