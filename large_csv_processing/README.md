# Large CSV Processing

This repository contains an example code snippet for processing CSV files using the pandas library in Python.
 The code demonstrates how to efficiently handle large CSV files,
  perform data manipulation tasks, and manage memory constraints.

## Features

1. **Efficiency**: The code leverages pandas, which is built on top of the efficient NumPy library.
 This ensures fast processing and manipulation of tabular data.

2. **Convenience**: pandas provides a high-level API that simplifies data manipulation tasks.
The code showcases how to use pandas' functionalities for filtering, grouping,
 and aggregating data in a concise and readable manner.

3. **Memory Management and Chunking**: The code takes advantage of pandas'
 ability to read and process data in smaller chunks using the `chunksize` parameter in `read_csv()`.
  This ensures efficient memory utilization when working with CSV files larger than the available memory.

4. **Computational Complexity**: The code has a computational complexity of O(N),
 where N is the number of rows in the CSV file. This is because the code iterates over the CSV file in chunks,
  performing aggregations and concatenations on each chunk.
  The overall time complexity depends on the number of chunks required to process the entire file.

## Getting Started

To use the code in your project, follow these steps:

1. Create a virtual environment:

   ```
   python -m venv env
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Activate the virtual environment:

   - For Windows:
     ```
     env\Scripts\activate
     ```

   - For macOS/Linux:
     ```
     source env/bin/activate
     ```

3. Install the required dependencies:

   ```
   pip install pandas
   ```

4. Modify the input and output file paths in the main script `process_csv_file.py`:

   ```python
   input_file_path = 'path/to/input_file.csv'
   output_file_path = 'path/to/output_file.csv'
   ```

5. Run the script:

   ```
   python process_csv_file.py
   ```

