# Backend Engineer - Assignment

This assignment is designed to be completed within a few hours or up to a day. Remember, the simpler the solution, the better.

The assignment consists of two logical parts:

1. **CSV Processing Module**
Create a module or function that takes an input CSV file, processes it, and generates an output CSV file. The input CSV file will have the following format: "Song", "Date", "Number of Plays". Each song can have multiple records for each day, and the input is not sorted. The output CSV file should have the following format: "Song", "Date", "Total Number of Plays for Date".

Important notes:
- Both the input and output CSV files can be larger than available memory.
- You are allowed to use Python built-ins or any available third-party libraries/frameworks/software.
- If you choose to use a third-party library, please explain how it works internally and why it is suitable for this task. Also, provide a brief explanation of the computational complexity of the algorithms used in the library.

Example:
Input CSV file:
```
Song,Date,Number of Plays
Umbrella,2020-01-02,200
Umbrella,2020-01-01,100
In The End,2020-01-01,500
Umbrella,2020-01-01,50
In The End,2020-01-01,1000
Umbrella,2020-01-02,50
In The End,2020-01-02,500
```

Output CSV file:
```
Song,Date,Total Number of Plays for Date
Umbrella,2020-01-01,150
Umbrella,2020-01-02,250
In The End,2020-01-01,1500
In The End,2020-01-02,500
```

2. **API and Asynchronous Task Processing**
This part involves creating two API endpoints to schedule file processing and download the result.

API Endpoint 1: Schedule file for processing
- Input: Upload a CSV file (remember, the file can be larger than memory)
- Output: ID of the processing task
- Action:
  - Process the uploaded large CSV file in the background using the CSV processing module implemented in the first part.
  - Return the ID of the processing task to retrieve the results later.

API Endpoint 2: Download the result
- Input: ID of the processing task
- Output: The resulting CSV file if the processing is done

Important notes:
- Both the input and output files can be larger than memory, and the processing can take a significant amount of time. Implement the system in a way that the API server can receive further requests while the previous file is still being processed.
- You are free to choose any Python API and task execution frameworks you prefer or not use them at all.
- This system does not need to be production-ready. It is a test to demonstrate your understanding of API and asynchronous task processing concepts.
- Please provide all the necessary configurations and instructions for someone who has not seen the project previously. Also, include examples on how to upload a file and download the results.

Thank you for your time!