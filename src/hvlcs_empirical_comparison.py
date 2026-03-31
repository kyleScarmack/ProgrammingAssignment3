import random
import time
import csv
from pathlib import Path
import matplotlib.pyplot as plt

from hvlcs import hvlcs
from parser import parse_input


def create_random_input_file(path, alphabet, lengths):
    # Seeded randomness for reproducibility
    rng = random.Random(4533 + sum(lengths))

    # Assign values to characters
    values = {ch: rng.randint(1, 10) for ch in alphabet}

    # Generate strings A and B
    lenA, lenB = lengths
    A = "".join(rng.choice(alphabet) for _ in range(lenA))
    B = "".join(rng.choice(alphabet) for _ in range(lenB))

    # Write input file
    with open(path, "w") as file:
        file.write(f"{len(alphabet)}\n")
        for ch in alphabet:
            file.write(f"{ch} {values[ch]}\n")
        file.write(A + "\n")
        file.write(B + "\n")


def write_output_file(path, maxValue, subsequence):
    # Write result to file
    with open(path, "w") as file:
        file.write(f"{maxValue}\n")
        file.write(subsequence + "\n")


def time_hvlcs(inputFile, repeats=3):
    # Measure best runtime over multiple runs
    best = float("inf")
    bestResult = None

    # Parse input once
    values, A, B = parse_input(str(inputFile))

    for _ in range(repeats):
        t0 = time.perf_counter()
        result = hvlcs(values, A, B)
        t1 = time.perf_counter()

        dt = (t1 - t0) * 1000  # ms
        if dt < best:
            best = dt
            bestResult = result

    return best, bestResult


def run_empirical_comparison():
    # Input sizes to test
    testSizes = [
        (25, 25), (50, 50), (100, 100), (150, 150), (200, 200),
        (300, 300), (400, 400), (500, 500), (600, 600), (750, 750),
    ]

    runtimes = []
    labels = []

    # Set up directories
    scriptDir = Path(__file__).resolve().parent
    projectRoot = scriptDir.parent if scriptDir.name.lower() == "src" else scriptDir

    dataInputs = projectRoot / "data" / "inputs"
    dataOutputs = projectRoot / "data" / "outputs"
    resultsDirectory = projectRoot / "results"

    dataInputs.mkdir(parents=True, exist_ok=True)
    dataOutputs.mkdir(parents=True, exist_ok=True)
    resultsDirectory.mkdir(parents=True, exist_ok=True)

    alphabet = ["a", "b", "c", "d", "e", "f"]

    # Run tests
    for i, lengths in enumerate(testSizes, start=1):
        inputFile = dataInputs / f"hvlcs{i}.in"
        outputFile = dataOutputs / f"hvlcs{i}.out"

        create_random_input_file(inputFile, alphabet, lengths)

        runtime, result = time_hvlcs(inputFile, repeats=3)

        if result is None:
            continue

        runtimes.append(runtime)
        labels.append(f"{lengths[0]}x{lengths[1]}")

        maxValue, subsequence = result
        write_output_file(outputFile, maxValue, subsequence)

    # Save CSV
    csvPath = resultsDirectory / "runtime_data.csv"
    with open(csvPath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "string_lengths", "runtime_ms"])
        for i, (label, runtime) in enumerate(zip(labels, runtimes), start=1):
            writer.writerow([f"hvlcs{i}.in", label, runtime])

    # Plot results
    plt.figure()
    plt.plot(labels, runtimes, marker="o")
    plt.xlabel("Input file (|A| x |B|)")
    plt.ylabel("Runtime (ms)")
    plt.title("HVLCS Runtime vs. Input Size")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plotPath = resultsDirectory / "hvlcs_runtime_vs_input.png"
    plt.savefig(plotPath, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Runtime data saved to {csvPath}")
    print(f"Graph saved to {plotPath}")


if __name__ == "__main__":
    run_empirical_comparison()