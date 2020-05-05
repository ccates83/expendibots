def parse_line(line):
    """
    Takes in a line and parses each line (game) into actions by whites and black
    """
    white_locs = []
    black_locs = []

    current = "white"

    for i in range(0, len(line)):
        # End states
        if line[i:i+4] == "draw":
            return [white_locs, black_locs, "draw"]
        if line[i:i+5] == "black":
            return [white_locs, black_locs, "black"]
        if line[i:i+5] == "white":
            return [white_locs, black_locs, "white"]

        # print(line[i:i+4])
        if line[i:i+4] == 'MOVE':
            # print("MOVE DETECTED")
            if current == "white":
                white_locs.append(line[i+18:i+24])
                current = "black"
            else:
                black_locs.append(line[i+18:i+24])
                current = "white"

def print_2d_arr(arr):
    for elem in arr:
        row = "["
        for item in elem:
            row += " {} ".format(item)
        row += "]"
        print(row)

white_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
black_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
def create_books(game):
    """
    Create an 8x8 grid of the expendibots board that will fill with values for
    each location for black and white
    """
    print("winner:", game[2])
    if game[2] == "white":
        w_multiplier = 1
        b_multiplier = -1
    else:
        w_multiplier = -1
        b_multiplier = 1

    if game[2] == "draw": return
    if game[2] == "white":
        w = 1
        b = -1
    else:
        w = -1
        b = 1

    turn = 1
    for elem in game[0]:
        loc = (int(elem[1]), int(elem[4]))
        white_grid[loc[1]][loc[0]] += w*turn
        turn += 1

    turn = 1
    for elem in game[1]:
        loc = (int(elem[1]), int(elem[4]))
        black_grid[loc[1]][loc[0]] += b*turn
        turn += 1



    return (white_grid, black_grid)



games = []
filepath = "records.txt"
with open(filepath) as fp:
    line = fp.readline()
    n = 1
    while line:
        if line != "\n":
            print("ACTIONS IN GAME", n)
            # print(line)
            data = parse_line(line)
            games.append(data)
            n += 1
        line = fp.readline()


for game in games:
    print("updating for game winner:", game[2])
    create_books(game)

print("WHITE GRID")
print_2d_arr(white_grid)
print()
print("BLACK GRID")
print_2d_arr(black_grid)
