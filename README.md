# Stock Data CLI Tool

A command-line tool for calculating forward and backward adjusted stock prices, supporting multiple file formats (CSV, JSON, Parquet).

## Features

- **Forward Adjustment**: Shows total return including reinvested dividends and stock splits
- **Backward Adjustment**: Makes all historical prices comparable to the most recent price
- **Multiple Formats**: Supports CSV, JSON, and Parquet input/output files
- **Extensible**: Easy to add new file formats and calculation methods

## Usage

### Basic Command Structure

```bash
python calculator.py --input <input_file> [options]
```

### Required Arguments

- `--input`: Path to input data file (CSV, JSON, or Parquet)

### Optional Arguments

- `--output`: Output file path to save results (format determined by extension)
- `--mode`: Calculation mode (`forward` or `backward`, default: `forward`)


## Examples

### 1. Basic Forward Adjustment
```bash
python calculator.py --input data/data.parquet --mode forward
```

### 2. Backward Adjustment with CSV Output
```bash
python calculator.py --input data/data.parquet --output results/data_backward_adj.csv --mode backward
```

### 3. Forward Adjustment with JSON Output
```bash
python calculator.py --input data/data.csv --output results/data_forward_adj.json --mode forward
```


### 4. Display Results Without Saving
```bash
python calculator.py --input data/data.json --mode backward
```

## Input Data Format

Your input file must contain the following required columns:

- `unadjusted_close`: Original closing price
- `ticker_symbol`: Stock ticker symbol (e.g., AAPL, TSLA)
- `datetime`: Date in YYYY-MM-DD format
- `split`: Split ratio (1.0 for no split, 2.0 for 2:1 split)
- `dividend`: Dividend amount (0.0 for no dividend)

### Example Input (CSV):
```csv
unadjusted_close,ticker_symbol,datetime,split,dividend
172.28,AAPL,2018-01-02,1.0,0.0
172.24,AAPL,2018-01-03,1.0,0.0
156.4,AAPL,2018-02-09,1.0,0.63
```

## Output Formats

The tool automatically detects output format based on file extension:

- `.csv` → CSV format
- `.json` → JSON format  
- `.parquet` → Parquet format

## Adjustment Types

### Forward Adjustment (`--mode forward`)
- **Purpose**: Shows total return of an investment including reinvested dividends
- **Reference**: First price remains unchanged
- **Use Case**: Performance analysis, "what if I invested $X in 2018?"

**Example Output:**
```
unadjusted_close    ticker_symbol   datetime      split     dividend    forward_adj_close
172.28              AAPL            2018-01-02    1.0       0.0         172.28
172.24              AAPL            2018-01-03    1.0       0.0         172.24
173.04              AAPL            2018-01-04    1.0       0.0         173.04
175.00              AAPL            2018-01-05    1.0       0.0         175.00
...                 ...             ...           ...       ...         ...
146.92              AAPL            2021-09-24    1.0       0.0         613.59
145.37              AAPL            2021-09-27    1.0       0.0         607.12
141.91              AAPL            2021-09-28    1.0       0.0         592.67
142.83              AAPL            2021-09-29    1.0       0.0         596.51
...                 ...             ...           ...       ...         ...
200.30              AAPL            2025-06-24    1.0       0.0         853.43
201.56              AAPL            2025-06-25    1.0       0.0         858.80
201.00              AAPL            2025-06-26    1.0       0.0         856.41
201.08              AAPL            2025-06-27    1.0       0.0         856.76
320.55              TSLA            2018-01-02    1.0       0.0         320.55
317.25              TSLA            2018-01-03    1.0       0.0         317.25
314.55              TSLA            2018-01-04    1.0       0.0         314.55
316.65              TSLA            2018-01-05    1.0       0.0         316.65
...                 ...             ...           ...       ...         ...
774.39              TSLA            2021-09-24    1.0       0.0         3871.95
791.37              TSLA            2021-09-27    1.0       0.0         3956.85
777.57              TSLA            2021-09-28    1.0       0.0         3887.85
781.32              TSLA            2021-09-29    1.0       0.0         3906.60
...                 ...             ...           ...       ...         ...
340.47              TSLA            2025-06-24    1.0       0.0         5107.05
327.55              TSLA            2025-06-25    1.0       0.0         4913.25
325.78              TSLA            2025-06-26    1.0       0.0         4886.70
323.63              TSLA            2025-06-27    1.0       0.0         4854.45

```

### Backward Adjustment (`--mode backward`)
- **Purpose**: Makes all historical prices comparable to current prices
- **Reference**: Most recent price remains unchanged
- **Use Case**: Technical analysis, price charting

**Example Output:**
```
unadjusted_close    ticker_symbol   datetime      split     dividend    backward_adj_close
172.28              AAPL            2018-01-02    1.0       0.0         40.43
172.24              AAPL            2018-01-03    1.0       0.0         40.42
173.04              AAPL            2018-01-04    1.0       0.0         40.61
175.00              AAPL            2018-01-05    1.0       0.0         41.07
...                 ...             ...           ...       ...         ...
146.92              AAPL            2021-09-24    1.0       0.0         144.01
145.37              AAPL            2021-09-27    1.0       0.0         142.49
141.91              AAPL            2021-09-28    1.0       0.0         139.10
142.83              AAPL            2021-09-29    1.0       0.0         140.00
...                 ...             ...           ...       ...         ...
200.30              AAPL            2025-06-24    1.0       0.0         200.30
201.56              AAPL            2025-06-25    1.0       0.0         201.56
201.00              AAPL            2025-06-26    1.0       0.0         201.00
201.08              AAPL            2025-06-27    1.0       0.0         201.08
320.55              TSLA            2018-01-02    1.0       0.0         21.37
317.25              TSLA            2018-01-03    1.0       0.0         21.15
314.55              TSLA            2018-01-04    1.0       0.0         20.97
316.65              TSLA            2018-01-05    1.0       0.0         21.11
...                 ...             ...           ...       ...         ...
774.39              TSLA            2021-09-24    1.0       0.0         258.13
791.37              TSLA            2021-09-27    1.0       0.0         263.79
777.57              TSLA            2021-09-28    1.0       0.0         259.19
781.32              TSLA            2021-09-29    1.0       0.0         260.44
...                 ...             ...           ...       ...         ...
340.47              TSLA            2025-06-24    1.0       0.0         340.47
327.55              TSLA            2025-06-25    1.0       0.0         327.55
325.78              TSLA            2025-06-26    1.0       0.0         325.78
323.63              TSLA            2025-06-27    1.0       0.0         323.63
```

## Error Handling

The tool handles various error conditions:

- **File not found**: Displays error message and exits
- **Unsupported format**: Shows supported formats (CSV, JSON, Parquet)
- **Invalid prices**: Skips rows with zero/negative prices with warnings

## File Structure

```
CLI_calculator/
├── .gitignore                       # Git ignore rules
|── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
├── calculator.py                    # Main CLI script
├── stock_data_cli/
│   └── src/
│       ├── loader/                  # Data loading modules
│       │   ├── csv_loader.py
│       │   ├── json_loader.py
│       │   ├── parquet_loader.py
│       │   ├── csv_saver.py
│       │   ├── json_saver.py
│       │   └── parquet_saver.py
│       └── returns/                 # Calculation modules
│           ├── forward_adjusted.py
│           └── backward_adjusted.py
├── data/                            # Input data (optional)
│   └── data.parquet
└── results/                         # Output directory (empty)
```


## Dependencies

- `pandas`: Data manipulation and analysis
- `pyarrow`: Parquet file support

