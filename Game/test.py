s = open('language.txt', 'r')
temp = ''
results = []

for char in s:
    if char == '=':
        results.append(temp)
        temp = []
    else:
        temp += char

if len(temp) > 0:
    results.append(temp)
outFile = open('output.txt', 'w')
for line in results:
    print(line, file=outFile)