data = 290431

def digits(n):
    return [int(x) for x in str(n)]

def p2(val):
    recipes = [3, 7]
    elves = [0, 1]
    val_digits = [int(x) for x in val]
    while 1:
        current = [recipes[j] for j in elves]
        new_recipes = digits(sum(current))
        recipes.extend(new_recipes)
        elves = [(j + k+1)%len(recipes) for j,k in zip(elves, current)]
        for i in range(len(new_recipes)):
            if recipes[-i - len(val_digits):len(recipes)-i] == val_digits:
                return len(recipes) - i - len(val_digits)

print(p2("51589"))
print(p2("01245"))
print(p2("92510"))
print(p2("59414"))
import time
start = time.time()
print(p2("290431"))
elapsed = time.time() - start
print("{:.2f}s".format(elapsed))
