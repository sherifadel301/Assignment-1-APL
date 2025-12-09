products = ["LAPTOP","Phone","Tablet","CAMERA"]

result = list(map(lambda x: x.strip().title(), products))

print(result)