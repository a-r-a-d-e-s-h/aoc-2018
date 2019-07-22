with open('xiuxing.txt', 'r') as f:
    data = f.read()

def checks(line):
    letters = [0]*26
    for char in line:
        index = ord(char) - ord('a')
        letters[index] += 1
    return (int(2 in letters), int(3 in letters))

lines = data.split('\n')
lines = [l for l in lines if l]

results = [checks(line) for line in lines]
totals = [0,0]
for item in results:
    totals[0] += item[0]
    totals[1] += item[1]
print(totals)
print(totals[0]*totals[1])

def differ_more_than_1(line1, line2):
    if line1 == line2:
        print("{} = {}".format(line1, line2))
        return False
    if len(line1) != len(line2):
        print("{} and {} are of different lengths!".format(line1, line2))
        return False
    differences = 0
    for i in range(len(line1)):
        x = line1[i]
        y = line2[i]
        if x != y:
            differences += 1
        if differences > 1:
            return False
    return True

for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        line1 = lines[i]
        line2 = lines[j]
        if differ_more_than_1(line1, line2):
            print("Found correct boxes!")
            print(line1, line2)
            for k in range(len(line1)):
                if line1[k] != line2[k]:
                    print("Answer is:")
                    print(line1[:k] + line1[k+1:])
