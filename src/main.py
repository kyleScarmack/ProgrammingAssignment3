import sys
from parser import parse_input
from hvlcs import hvlcs


# handle command line input and program output
def main():
    if len(sys.argv) != 2:
        print("usage: python src/main.py data/inputs/example.in")
        return

    file_path = sys.argv[1]

    # parse input and run the solver
    try:
        values, a, b = parse_input(file_path)
        max_value, subsequence = hvlcs(values, a, b)

        print(max_value)
        print(subsequence)

    # handle common file and input errors
    except FileNotFoundError:
        print("error: input file not found")
    except ValueError:
        print("error: invalid input format")
    except IndexError:
        print("error: incomplete input file")


# run the program
if __name__ == "__main__":
    main()