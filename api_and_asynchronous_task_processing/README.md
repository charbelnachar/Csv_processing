# Large CSV Processing with Flask

This repository contains a Flask application for processing large CSV files. The application allows users to upload CSV files, schedule their processing, and download the processed result. It utilizes the `ProcessingCsv` class from the `large_csv_processing` module to handle the processing of CSV files in chunks.

## Requirements

- Python 3.6 or higher
- Flask
- Flask-Migrate
- Flask-SQLAlchemy
- Panda


## Getting Started

To set up and run the Flask application, follow these steps:

1. Create a virtual environment:

   ```
   python -m venv env
   ```

2. Activate the virtual environment:

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
   pip install -r requirements.txt
   ```


4. Initialize the database:

   ```
   flask db init
   ```

5. Apply database migrations:

   ```
   flask db migrate
   flask db upgrade
   ```


6. Start the Flask development server:
   (run the command while in the folder where app.py is located:)
   ```
   flask run
   ```



## Usage

1. Upload a CSV file by sending a POST request to `/schedule` with the `file` parameter containing the file data.

   Example using cURL:

   ```
   curl -X POST -F "file=@/path/to/file.csv" http://localhost:5000/schedule
   ```

   The response will contain a `task_id` that can be used to track the processing status and download the result.

2. Check the processing status and download the result by sending a GET request to `/result/<task_id>`.

   Example using cURL:

   ```
   curl http://localhost:5000/result/task_20220101_123456
   ```

   If the processing is complete, the response will include the processed result file as an attachment.

