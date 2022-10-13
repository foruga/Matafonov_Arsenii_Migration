i = input()
i = i.split(' ')
for el in range(len(i)):
    i[el] = i[el].capitalize()
result = ' '.join(i)
print(result)