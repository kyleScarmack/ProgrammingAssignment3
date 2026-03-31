import sys
from pathlib import Path

from parser import parse_input
from hvlcs import hvlcs


def run_solver(input_path):
    values, a, b = parse_input(str(input_path))
    return hvlcs(values, a, b)


def get_project_root():
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent if script_dir.name.lower() == "src" else script_dir


def discover_cases():
    root = get_project_root()
    input_dir = root / "data" / "inputs"
    output_dir = root / "data" / "outputs"

    input_files = {path.stem: path for path in input_dir.glob("*.in")}
    output_files = {path.stem: path for path in output_dir.glob("*.out")}

    matched_case_names = sorted(set(input_files) & set(output_files))

    return [
        {
            "name": case_name,
            "input_path": input_files[case_name],
            "output_path": output_files[case_name],
        }
        for case_name in matched_case_names
    ]


def read_expected(output_path):
    with open(output_path, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    if not lines:
        raise ValueError("output file is empty")

    expected_value = int(lines[0].strip())
    expected_subsequence = lines[1] if len(lines) > 1 else ""

    return expected_value, expected_subsequence


def evaluate_case(case):
    result = {
        "name": case["name"],
        "input_path": case["input_path"],
        "output_path": case["output_path"],
        "error": None,
    }

    try:
        expected_value, expected_subsequence = read_expected(case["output_path"])
        actual_value, actual_subsequence = run_solver(case["input_path"])
    except (FileNotFoundError, ValueError, IndexError) as error:
        result["error"] = str(error)
        return result

    result.update(
        {
            "expected_value": expected_value,
            "expected_subsequence": expected_subsequence,
            "actual_value": actual_value,
            "actual_subsequence": actual_subsequence,
            "value_match": actual_value == expected_value,
            "subsequence_match": actual_subsequence == expected_subsequence,
        }
    )

    return result


def print_case_result(result):
    print()
    print(f"Case: {result['name']}")
    print(f"Input: {result['input_path']}")
    print(f"Expected output: {result['output_path']}")

    if result["error"] is not None:
        print("Value match (pass/fail): FAIL")
        print("Subsequence exact match (info): N/A")
        print(f"Error: {result['error']}")
        return

    value_status = "PASS" if result["value_match"] else "FAIL"
    subsequence_status = "MATCH" if result["subsequence_match"] else "DIFFERENT"

    print(f"Expected value: {result['expected_value']}")
    print(f"Actual value:   {result['actual_value']}")
    print(f"Expected subsequence: {result['expected_subsequence']!r}")
    print(f"Actual subsequence:   {result['actual_subsequence']!r}")
    print(f"Value match (pass/fail): {value_status}")
    print(f"Subsequence exact match (info): {subsequence_status}")


def run_single_case(cases):
    while True:
        print()
        print("Available cases:")
        for index, case in enumerate(cases, start=1):
            print(f"{index}) {case['name']}")

        selection = input("Select a case number (or 'b' to go back): ").strip()

        if selection.lower() == "b":
            return

        if not selection.isdigit():
            print("Invalid selection. Enter a valid number.")
            continue

        case_index = int(selection)
        if not 1 <= case_index <= len(cases):
            print("Invalid selection. Number is out of range.")
            continue

        print_case_result(evaluate_case(cases[case_index - 1]))
        return


def print_summary(results):
    total = len(results)
    value_pass = sum(1 for result in results if result.get("value_match") is True)
    value_fail = total - value_pass
    subsequence_exact = sum(
        1 for result in results if result.get("subsequence_match") is True
    )
    subsequence_different = sum(
        1
        for result in results
        if result.get("error") is None and result.get("subsequence_match") is False
    )
    evaluation_errors = sum(1 for result in results if result.get("error") is not None)

    print()
    print("Summary")
    print(f"Total: {total}")
    print(f"Value-pass: {value_pass}")
    print(f"Value-fail: {value_fail}")
    print(f"Subsequence-exact: {subsequence_exact}")
    print(f"Subsequence-different: {subsequence_different}")
    if evaluation_errors:
        print(f"Evaluation errors: {evaluation_errors}")


def run_all_cases(cases):
    results = []

    for case in cases:
        result = evaluate_case(case)
        print_case_result(result)
        results.append(result)

    print_summary(results)


def menu_loop():
    cases = discover_cases()

    if not cases:
        print("No matched .in/.out case pairs were found in data/inputs and data/outputs.")
        return

    while True:
        print()
        print("Case Runner Menu")
        print("1) Run single case")
        print("2) Run all cases")
        print("3) Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_single_case(cases)
        elif choice == "2":
            run_all_cases(cases)
        elif choice == "3":
            print("Exiting case runner.")
            return
        else:
            print("Invalid option. Enter 1, 2, or 3.")


def run_cli(file_path):
    try:
        max_value, subsequence = run_solver(file_path)

        print(max_value)
        print(subsequence)

    except FileNotFoundError:
        print("error: input file not found")
    except ValueError:
        print("error: invalid input format")
    except IndexError:
        print("error: incomplete input file")


def main():
    if len(sys.argv) == 1:
        menu_loop()
    elif len(sys.argv) == 2:
        run_cli(sys.argv[1])
    else:
        print("usage: python src/main.py data/inputs/example.in")
        print("or run without arguments to open the interactive case menu")


if __name__ == "__main__":
    main()
