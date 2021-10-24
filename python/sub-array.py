

nums = [4, 3, 2, 1]

def solution(nums):
    if sum(nums) % 2 == 1:
        return False
    if len(nums) == 0 or len(nums) == 1:
        return False

    target = sum(nums) / 2
    current = 0
    for k,v in enumerate(nums):
        current += v
        print(current, target)
        if current == target:
            return nums[0:k+1], nums[k+1:]
        if current > target:
            return False

print(solution(nums))