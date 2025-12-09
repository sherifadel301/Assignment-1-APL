words = ["python is cool","programming is fun","coding is art","learning is life"]

result = list(map(lambda x:list(map(lambda y:len(y),x.strip().split())),words))

print(result)