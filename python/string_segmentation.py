
# Original problem: https://www.educative.io/m/string-segmentation 
# You are given a dictionary of words and a large input string. 
# You have to find out whether the input string can be completely segmented 
# into the words of a given dictionary. The following two examples elaborate on the problem further.

# This code doesn't work 
# def string_segmentation(s, dict):
#     start = 0
#     for i in range(len(s)):
#         temp=s[start:i+1]
#         if temp in dict:
#             start = i+1 
#             print(f'segment found:{temp}')
#     return True if temp in dict else False

# This code should work
# def can_segment_string(s, dictionary):
#   for i in range(len(s)):
#     if s in dictionary: return True
#     if s[:i] in dictionary and can_segment_string(s[i:], dictionary):
#       return True 
#   return False

def string_segmentation(s, dict):
    for i in range(len(s)):
        temp=s[0:i+1]
        if temp in dict:
            second = s[i+1:]
            print(f'Frist segment {temp}, second segment {second}')
            if not second or second in dict or string_segmentation(second, dict):
                return True
    return False

def main():
    res = string_segmentation(input, dict)
    print(res)

input = 'hellonow'
dict = ("hello","hell","on","now")

if __name__ == '__main__':
    main()