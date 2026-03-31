# read and parse the input file
def parse_input(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    # make sure the file has enough lines
    if len(lines) < 4:
        raise ValueError("input file is too short")

    # read the number of character-value pairs
    index = 0
    k = int(lines[index])
    index += 1

    # make sure k is valid
    if k < 1:
        raise ValueError("k must be at least 1")

    # make sure enough lines exist for the alphabet and strings
    if len(lines) < 1 + k + 2:
        raise ValueError("input file is incomplete")

    # store character values in a dictionary
    values = {}
    for _ in range(k):
        parts = lines[index].split()

        # each alphabet line should have exactly two parts
        if len(parts) != 2:
            raise ValueError("invalid character-value line")

        char, value = parts

        # each symbol should be a single character
        if len(char) != 1:
            raise ValueError("each alphabet symbol must be one character")

        # do not allow duplicate characters
        if char in values:
            raise ValueError("duplicate alphabet character found")

        values[char] = int(value)

        # values must be nonnegative
        if values[char] < 0:
            raise ValueError("character values must be nonnegative")

        index += 1

    # read the two strings
    a = lines[index]
    index += 1
    b = lines[index]

    # make sure both strings only use characters from the alphabet
    for char in a:
        if char not in values:
            raise ValueError("string A contains character not in alphabet")

    for char in b:
        if char not in values:
            raise ValueError("string B contains character not in alphabet")

    return values, a, b