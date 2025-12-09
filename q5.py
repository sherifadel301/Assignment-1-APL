marks = [[45,80,70],[90,60,100],[88,76,92]]

result = list(map(lambda x: list(map(lambda y:round(y*1.05),x)),marks))

print(result)