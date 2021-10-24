
# This code doesn't work 
# def string_segmentation(s, dict):
#     start = 0
#     for i in range(len(s)):
#         temp=s[start:i+1]
#         if temp in dict:
#             start = i+1 
#             print(f'segment found:{temp}')
#     return True if temp in dict else False

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