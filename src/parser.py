# read and parse the input file
def parse_input(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    # read the number of character-value pairs
    index = 0
    k = int(lines[index])
    index += 1

    # store character values in a dictionary
    values = {}
    for _ in range(k):
        # split the line into character and value, and store in the dictionary
        char, value = lines[index].split()
        values[char] = int(value)
        index += 1

    # read the two strings
    a = lines[index]
    index += 1
    b = lines[index]

    return values, a, b