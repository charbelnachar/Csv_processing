import os
import pandas as pd

class ProcessingCsv:
    def generate_unique_file_path(self, file_path: str) -> str:
        """
        Generate a unique file path based on an existing file path.

        If the file path already exists, a copy count is appended to the file name
        until a unique file path is found.

        Args:
            file_path (str): Existing file path.

        Returns:
            str: Unique file path.

        Example:
            generate_unique_file_path('output.csv')
            'output_1.csv'
        """
        if not os.path.exists(file_path):
            return file_path

        base_name, extension = os.path.splitext(file_path)
        copy_count = 1
        while os.path.exists(f"{base_name}({copy_count}){extension}"):
            copy_count += 1

        unique_file_path = f"{base_name}({copy_count}){extension}"
        return unique_file_path

    def process_data(self, csv_file_path: str, rows_per_chunk: int = 100000) -> pd.DataFrame:
        """
        Process a CSV file in chunks and calculate the total number of plays for each song and date.

        Args:
            csv_file_path (str): Path to the CSV file.
            rows_per_chunk (int): Number of rows to load per chunk. Default is 100000.

        Returns:
            pd.DataFrame: Processed data containing the song, date, and total number of plays for each date.

        Raises:
            ValueError: If the data chunk is empty.
        """
        result_df = pd.DataFrame(columns=['Song', 'Date', 'Total Number of Plays for Date'])

        for chunk in pd.read_csv(csv_file_path, chunksize=rows_per_chunk):
            if not chunk.empty:
                grouped_chunk = chunk.groupby(['Song', 'Date'])['Number of Plays'].sum().reset_index()
                grouped_chunk.rename(columns={'Number of Plays': 'Total Number of Plays for Date'}, inplace=True)
                result_df = pd.concat([result_df, grouped_chunk], ignore_index=True)


        return result_df

    def generate_output_csv(self, csv_file_path: str, data: pd.DataFrame, chunksize: int = 1000) -> None:
        """
        Generate the output CSV file.

        Args:
            csv_file_path (str): Path to the output CSV file.
            data (pd.DataFrame): Result chunks.
            chunksize (int): Number of rows to write per chunk. Default is 1000.

        Raises:
            ValueError: If no result chunks are provided.
        """

        with open(csv_file_path, 'a') as f:

            data.head(0).to_csv(f, index=False)

            for i in range(0, len(data), chunksize):
                chunk = data[i:i + chunksize]
                chunk.to_csv(f, mode='a', header=False, index=False)

    def process_csv_file(self, input_file_path: str, output_file_path: str, rows_per_chunk: int = 100000) -> None:
        """
        Process a CSV file in chunks and generate the output CSV file.

        Args:
            input_file_path (str): Path to the input CSV file.
            output_file_path (str): Path to the output CSV file.
            rows_per_chunk (int): Number of rows to load per chunk. Default is 100000.

        Raises:
            Exception: If there is an error processing the CSV file.
        """
        try:
            result_chunks = self.process_data(input_file_path, rows_per_chunk)
            csv_file_path = self.generate_unique_file_path(output_file_path)
            self.generate_output_csv(csv_file_path, result_chunks)
        except Exception as e:
            raise Exception("Error processing the CSV file:", str(e))


