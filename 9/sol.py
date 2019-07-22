with open('input.txt', 'r') as f:
    data = f.read()

players = 413
last_marble = 71082

marbles = [0]*71082

current_player = 0
player_marbles = [[] for __ in range(players)]

current_marble = 0

for i in range(last_marble ):
    next_marble = i + 1
    num_marbles = len(marbles)
    if next_marble % 23 == 0:
        player_marbles[current_player].append(next_marble)
        to_remove_index = (current_marble - 7) % num_marbles
        player_marbles[current_player].append(marbles[to_remove_index])
        marbles = marbles[:to_remove_index] + marbles[to_remove_index+1:]
        if to_remove_index == num_marbles -1:
            current_marble = 0
        else:
            current_marble = to_remove_index
    else:
        if current_marble == num_marbles - 1:
            marbles = marbles[:1] + [next_marble] + marbles[1:]
            current_marble = 1
        else:
            marbles = marbles[:current_marble+2] + [next_marble] + marbles[current_marble+2:]
            current_marble += 2

    current_player += 1
    current_player %= players

scores = []
for pi in player_marbles:
    scores.append(sum(pi))

max_score = 0
for i, ps in enumerate(scores):
    if ps >= max_score:
        max_score = ps
#        print("Player {} has {} points".format(i+1, max_score))
print(max(scores))
