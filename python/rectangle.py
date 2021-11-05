# https://leetcode.com/problems/construct-the-rectangle/

def solution(area):
    l, w = area, 1
    diff = area - 1
    res = [l, w]

    while l >= w:
        print(l, w)
        if area % w == 0:
            l = area // w
            if l - w < diff:
                print(f'Change, {l}, {w}')
                diff = l - w
                res = [l ,w]
        w += 1
        l = area // w
    
    return res

def solution2(area):
    mid = int(area ** 0.5)

    for i in range(mid)[::-1]:
        if area % i == 0:
            return [area // i, i]

if __name__ == '__main__':
    print(solution2(122122))
