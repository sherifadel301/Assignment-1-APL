words = ["python","lambda","programming","map","function"]

result = list(map(lambda x: (x[0],x[-1]), words))

print(result)