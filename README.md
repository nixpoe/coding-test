## Financial Return Calculator Challenge 📈

### The Challenge
Our quantitative analysis team requires a command-line interface (CLI) tool for calculating forward-adjusted stock returns. This tool is a business-critical asset for our team, as its output will directly inform performance models used for key client reporting. Accuracy and methodological transparency are the top priorities.

While standard data libraries provide backward-adjusted prices, our models require a forward-adjusted calculation to accurately reflect the performance of a specific investment.

Your mission is to build this tool. It will read unadjusted stock price data (for tickers like AAPL or TSLA), perform a user-specified return calculation, and save the results to a file, supporting multiple output formats. Do the actual calculations yourself, do not use any libraries like pandas, ta-lib etc. You can use basic libraries to help with loading and storing the CSV, Parquet, and JSON file formats.

Try to build things step by step, be methodical!

### Core Requirements
##### 1) Extensible Data Loading
The tool must read historical stock data from a file provided via a command-line argument. The input format (Parquet, JSON, or CSV) should be determined automatically from the file's extension. The data will always contain the columns: unadjusted_close,	ticker_symbol,	datetime,	split, and	dividend. Your design must be extensible. You can expect that new input formats might be added in the future.

##### 2) Extensible Data Saving
The tool must save the processed data to a file specified by the user. The output format (Parquet, JSON, or CSV) should also be determined automatically from the output file's extension. Similar to data loading, the saving mechanism must be extensible. You can expect that new output formats might be added in the future.

##### 3) Flexible Calculation Logic
The tool must be controlled via command-line arguments. The calculations should always process the entire provided data file. A typical command would look like this:

python calculator.py --input data/aapl.parquet --output results/aapl_adj.json --mode backward

There are two calculation modes:

- mode backward: Implements the standard backward-adjusted price calculation. This method adjusts historical prices to reflect all splits and dividends that occur after that point in time, creating a consistent time series. The output should include a new column, e.g., backward_adj_close.

- mode forward: Implements a [forward-adjusted price](https://quantdare.com/approach-to-dividend-adjustment-factors-calculation/) calculation. This method should produce a price series that reflects the growth of an initial investment by reinvesting all dividends and accounting for splits. This is often used to calculate a total return index. The output should include a new column, e.g., forward_adj_close. 

##### 4) Verification & Quality
How can we be confident that your calculations are correct, especially for edge cases (e.g., a stock with no dividends, a split occurring on the start date)?

### Deliverables

- Git Repository: A link to a repository with the complete, runnable source code.
