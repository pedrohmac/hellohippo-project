import argparse
import os
import pandas as pd

from data_processing import process_claims

def load_data_from_directory(directory):
    all_data = pd.DataFrame()
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            data = pd.read_json(filepath)
            all_data = pd.concat([all_data, data], ignore_index=True)
        elif filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            data = pd.read_csv(filepath)
            all_data = pd.concat([all_data, data], ignore_index=True)
    return all_data


def main():
    parser = argparse.ArgumentParser(description='Process pharmacy data.')
    parser.add_argument('pharmacy_directory', type=str)
    parser.add_argument('claims_directory', type=str)
    parser.add_argument('reverts_directory', type=str)
    args = parser.parse_args()

    pharmacies = load_data_from_directory(args.pharmacy_directory)
    claims = load_data_from_directory(args.claims_directory)
    reverts = load_data_from_directory(args.reverts_directory)

    # Process data, calculate metrics and generate output files
    process_claims(pharmacies, claims, reverts)

if __name__ == '__main__':
    main()
