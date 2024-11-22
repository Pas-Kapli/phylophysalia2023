#!/usr/bin/env python3

import argparse
import os

def parse_fasta(file_path):
    """Parse a FASTA file and return taxon names and sequences."""
    headers, sequences = [], []
    with open(file_path, "r") as f:
        temp_seq = ""
        for line in f:
            if line.startswith(">"):
                headers.append(line.strip())
                if temp_seq:
                    sequences.append(temp_seq)
                    temp_seq = ""
            else:
                temp_seq += line.strip()
        if temp_seq:
            sequences.append(temp_seq)
    return headers, sequences


def write_fasta(headers, sequences, output_file):
    """Write sequences to a FASTA file."""
    with open(output_file, "w") as f:
        for header, seq in zip(headers, sequences):
            f.write(f"{header}\n{seq}\n")


def average_differences(sequences):
    """Calculate the average percentage differences for each sequence."""
    seq_count = len(sequences)
    seq_length = len(sequences[0])
    avg_diffs = []

    for i in range(seq_count):
        diffs = []
        for j in range(seq_count):
            if i != j:
                pair_diff = sum(
                    sequences[i][k] != sequences[j][k]
                    and sequences[i][k] not in "-N"
                    and sequences[j][k] not in "-N"
                    for k in range(seq_length)
                )
                valid_bases = sum(
                    sequences[i][k] not in "-N" and sequences[j][k] not in "-N"
                    for k in range(seq_length)
                )
                diffs.append(pair_diff / valid_bases if valid_bases > 0 else 0)
        avg_diffs.append(sum(diffs) / len(diffs) if diffs else 0)
    return avg_diffs


def filter_by_average_differences(headers, sequences, threshold):
    """Remove sequences exceeding average percentage differences."""
    avg_diffs = average_differences(sequences)
    filtered_headers = [
        header for header, diff in zip(headers, avg_diffs) if diff < threshold
    ]
    filtered_seqs = [
        seq for seq, diff in zip(sequences, avg_diffs) if diff < threshold
    ]
    return filtered_headers, filtered_seqs


def filter_by_missing_data(headers, sequences, threshold):
    """Remove sequences exceeding a threshold percentage of missing data."""
    filtered_headers = []
    filtered_seqs = []

    for header, seq in zip(headers, sequences):
        missing = seq.count("-") + seq.count("N")
        if missing / len(seq) < threshold:
            filtered_headers.append(header)
            filtered_seqs.append(seq)

    return filtered_headers, filtered_seqs


def remove_columns_with_missing_data(sequences):
    """Remove columns with all missing data."""
    seq_length = len(sequences[0])
    valid_columns = [
        i
        for i in range(seq_length)
        if any(seq[i] not in "-N" for seq in sequences)
    ]
    filtered_seqs = ["".join(seq[i] for i in valid_columns) for seq in sequences]
    return filtered_seqs


def check_alignment_quality(sequences, threshold):
    """Check if alignment exceeds a threshold of missing data columns."""
    seq_length = len(sequences[0])
    missing_columns = sum(
        any(seq[i] in "-N" for seq in sequences) for i in range(seq_length)
    ) 
    return missing_columns / seq_length <= threshold

def check_and_remove_existing_file(file_path):
    """Check if the output file exists, and delete it if it does."""
    if os.path.exists(file_path):
        print(f"Output file '{file_path}' already exists. Deleting it.")
        os.remove(file_path)

def main():
    parser = argparse.ArgumentParser(description="Filter alignment sequences.")
    parser.add_argument("input_file", help="Input FASTA file")
    parser.add_argument("output_file", help="Output file")
    parser.add_argument("--format", choices=["fasta", "phylip"], default="fasta", help="Output format")
    parser.add_argument("--diff_threshold", type=float, required=True, help="Threshold for average differences")
    parser.add_argument("--missing_threshold", type=float, required=True, help="Threshold for missing data")
    parser.add_argument("--alignment_missing_threshold", type=float, required=True, help="Threshold for alignment removal")
    args = parser.parse_args()

    # Check and remove existing output file
    check_and_remove_existing_file(args.output_file)

    # Parse input FASTA
    headers, sequences = parse_fasta(args.input_file)
    #print(1, headers, sequences)
    # Step 1: Filter by average differences
    headers, sequences = filter_by_average_differences(headers, sequences, args.diff_threshold)
    #print(2, headers, sequences)
    # Step 2: Filter by missing data
    headers, sequences = filter_by_missing_data(headers, sequences, args.missing_threshold)

    # Step 3: Remove columns with all missing data
    sequences = remove_columns_with_missing_data(sequences)

    # Step 4: Check alignment quality
    if not check_alignment_quality(sequences, args.alignment_missing_threshold):
        print("Alignment exceeds the threshold for missing data columns and will not be saved.")
        return

    # Write output
    if args.format == "fasta":
        write_fasta(headers, sequences, args.output_file)
    elif args.format == "phylip":
        with open(args.output_file, "w") as f:
            f.write(f"{len(headers)} {len(sequences[0])}\n")
            for header, seq in zip(headers, sequences):
                f.write(f"{header[1:]:<10}{seq}\n")

    print(f"Filtered alignment saved to {args.output_file}.")


if __name__ == "__main__":
    main()
