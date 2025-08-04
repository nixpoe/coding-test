import sys
import os
import argparse

from stock_data_cli.src.loader.base_loader import BaseLoader
from stock_data_cli.src.loader.base_saver import BaseSaver
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

    # Use Strategy pattern with factory method to get appropriate loader
    try:
        loader = BaseLoader.get_loader_for_file(args.input)
    except ValueError as e:
        print(f"Error: {e}")
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
        # Use Strategy pattern with factory method to get appropriate saver
        try:
            saver = BaseSaver.get_saver_for_file(args.output)
        except ValueError as e:
            print(f"Error: {e}")
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