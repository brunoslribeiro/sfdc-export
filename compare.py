import argparse
import csv
import json
from typing import List, Set


def _read_column_values(path: str, column: str) -> List[str]:
    """Return list of values for given column from CSV or JSONL file."""
    values: List[str] = []
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if column in row:
                    values.append(row[column])
    elif path.lower().endswith(".jsonl"):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    if column in obj:
                        values.append(obj[column])
    else:
        raise ValueError("Unsupported file format. Use .csv or .jsonl")
    return values


def compare_files(file1: str, file2: str, column: str, output: str | None = None) -> str:
    """Compare column values between two files and write results with status.

    Args:
        file1: Primary file path.
        file2: Secondary file path.
        column: Column/field name to compare.
        output: Optional output file path. Defaults to comparison.<ext>.

    Returns:
        Path to output file.
    """
    values2: Set[str] = set(_read_column_values(file2, column))

    if file1.lower().endswith(".csv"):
        with open(file1, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames + ["status"] if reader.fieldnames else ["status"]
            rows = []
            for row in reader:
                val = row.get(column)
                row["status"] = "FOUND" if val in values2 else "NOT FOUND"
                rows.append(row)
        out_path = output or "comparison.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as out_f:
            writer = csv.DictWriter(out_f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    elif file1.lower().endswith(".jsonl"):
        results = []
        with open(file1, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    val = obj.get(column)
                    obj["status"] = "FOUND" if val in values2 else "NOT FOUND"
                    results.append(obj)
        out_path = output or "comparison.jsonl"
        with open(out_path, "w", encoding="utf-8") as out_f:
            for obj in results:
                out_f.write(json.dumps(obj) + "\n")
    else:
        raise ValueError("Unsupported file format. Use .csv or .jsonl")

    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two data files on a column")
    parser.add_argument("file1", help="Primary file (csv or jsonl)")
    parser.add_argument("file2", help="Secondary file (csv or jsonl)")
    parser.add_argument("--column", required=True, help="Column/field to compare")
    parser.add_argument("--output", help="Output file path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out = compare_files(args.file1, args.file2, args.column, args.output)
    print(f"Comparison written to {out}")


if __name__ == "__main__":
    main()
