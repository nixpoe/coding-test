import sys
import os
import argparse

from stock_data_cli.src.loader.parquet_loader import ParquetLoader
from stock_data_cli.src.loader.json_loader import JsonLoader
from stock_data_cli.src.loader.csv_loader import CsvLoader
from stock_data_cli.src.loader.csv_saver import CsvSaver
from stock_data_cli.src.loader.json_saver import JsonSaver
from stock_data_cli.src.loader.parquet_saver import ParquetSaver
from stock_data_cli.src.returns.forward_adjusted import ForwardAdjusted
from stock_data_cli.src.returns.backward_adjusted import BackwardAdjusted

def main():
    parser = argparse.ArgumentParser(description='Stock return calculator (script version)')
    parser.add_argument('--input', type=str, required=True, help='Input data file (Parquet, JSON, or CSV)')
    parser.add_argument('--output', type=str, help='Output file path to save the results (Parquet, JSON, or CSV)')
    parser.add_argument('--mode', type=str, choices=['forward', 'backward'], default='forward', help='Calculation mode: forward or backward')

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: The file {args.input} does not exist.")
        sys.exit(1)

    file_extension = os.path.splitext(args.input)[1].lower()

    if file_extension == '.parquet':
        loader = ParquetLoader(args.input)
    elif file_extension == '.json':
        loader = JsonLoader(args.input)
    elif file_extension == '.csv':
        loader = CsvLoader(args.input)
    else:
        print("Error: Unsupported file format. Please provide a CSV, JSON, or Parquet file.")
        sys.exit(1)

    data = loader.load_data()

    # print("Loaded Data:")
    # print(data)
    # print()

    if args.mode == 'forward':
        adj = ForwardAdjusted(data)
        result = adj.forward_adj()
    else:
        adj = BackwardAdjusted(data)
        result = adj.backward_adj()

    if args.output:
        output_extension = os.path.splitext(args.output)[1].lower()
        if output_extension == '.csv':
            saver = CsvSaver(args.output)
        elif output_extension == '.json':
            saver = JsonSaver(args.output)
        elif output_extension == '.parquet':
            saver = ParquetSaver(args.output)
        else:
            print("Error: Unsupported output file format. Please use CSV, JSON, or Parquet.")
            sys.exit(1)
        saver.save(result)
        print(f"Results saved to {args.output}\n\n_____\n")
        print("Results:")
        print(result)
    else:
        print("No output file specified. Displaying results:\n")
        print(result)

if __name__ == "__main__":
    main()