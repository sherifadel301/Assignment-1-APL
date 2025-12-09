nums = [40,60,10,90,75,100]

max = max(nums)
min = min(nums)

result = list(map(lambda x: round((x-min)/(max-min),1),nums))

print(result)