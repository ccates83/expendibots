white = 0
black = 0
draw = 0

filepath = "records.txt"
with open(filepath) as fp:
    line = fp.readline()
    n = 1
    while line:
        if line != "\n":
            if line[-6:] == 'white\n': white += 1
            elif line[-6:] == 'black\n': black += 1
            else: draw += 1
            n += 1
        line = fp.readline()

print("White: {} wins".format(white))
print("Black: {} wins".format(black))
print("Draws:", draw)
