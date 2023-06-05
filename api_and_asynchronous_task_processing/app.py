import os
import threading
from flask import Flask, request, jsonify, send_file
from datetime import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .csv_proc import ProcessingCsv

app = Flask(__name__)
app.app_context().push()
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 1 GB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Global constants
COMPLETE = "completed"
PROCESS = "process"
ERROR = "error"


class FileProcessingStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(255), unique=True)
    file_name = db.Column(db.String(255))
    status = db.Column(db.String(50))

    def __init__(self, task_id, file_name, status):
        self.task_id = task_id
        self.file_name = file_name
        self.status = status

db.create_all()


@app.route('/schedule', methods=['POST'])
def schedule_processing() -> jsonify:
    """Schedules the processing of a file uploaded by the user.

    Returns:
        A JSON response containing the task ID.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Save the uploaded file with task ID
    utility_files = UtilityFiles()
    task_id = utility_files.generate_task_id()
    file_path = utility_files.save_file(file, task_id)

    # Save the processing status of the file
    status = FileProcessingStatus(task_id=task_id, file_name=file.filename, status=PROCESS)
    db.session.add(status)
    db.session.commit()

    thread = threading.Thread(target=process_data, args=(file_path, task_id))
    thread.start()

    return jsonify({'task_id': task_id})


@app.route('/result/<task_id>', methods=['GET'])
def download_result(task_id) -> jsonify:
    """Downloads the processed result file based on the task ID.

    Args:
        task_id (str): The task ID.

    Returns:
        A JSON response with the result file for download.
    """
    status = FileProcessingStatus.query.filter_by(task_id=task_id).first()
    if status is None:
        return jsonify({'error': 'Task ID not found'}), 404

    if status.status != COMPLETE:
        if status.status is PROCESS:
            return jsonify({'error': 'The file is still being processed'}), 404
        elif status.status is ERROR:
            return jsonify({'error': 'The file has an error'}), 404

    utility_files = UtilityFiles()
    result_file_path = utility_files.get_result_file_path(task_id)

    if result_file_path is None:
        return jsonify({'error': 'Result file not available yet'}), 404

    return send_file(result_file_path, as_attachment=True)


def process_data(file_path: str, task_id: str) -> str:
    """Processes  CSV file.

    Args:
        file_path (str): The path to the CSV file.
        task_id (str): The task ID.

    Returns:
        str: The path to the generated result file.
    """
    with app.app_context():

        utility_csv = ProcessingCsv()
        result_chunks = utility_csv.process_data(file_path)

        utility_files = UtilityFiles()
        result_file_path = utility_files.generate_result_file_path(task_id)

        status = FileProcessingStatus.query.filter_by(task_id=task_id).first()

        try:
            utility_csv.generate_output_csv(result_file_path, result_chunks)
            if status:
                status.status = COMPLETE
                db.session.commit()
        except:
            if status:
                status.status = ERROR
                db.session.commit()

        return result_file_path


class UtilityFiles:
    """Utility functions for file handling."""

    def save_file(self, file, task_id: str) -> str:
        """Saves the uploaded file with the specified task ID.

        Args:
            file: The uploaded file object.
            task_id (str): The task ID.

        Returns:
            str: The saved file path.
        """
        file_path = os.path.join('uploads', f'{task_id}_{file.filename}')
        file.save(file_path)
        return file_path

    def generate_task_id(self) -> str:
        """Generates a task ID based on the current timestamp.

        Returns:
            str: The generated task ID.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'task_{timestamp}'

    def generate_result_file_path(self, task_id: str) -> str:
        """Generates the result file path based on the task ID.

        Args:
            task_id (str): The task ID.

        Returns:
            str: The generated result file path.
        """
        return f'results/result_{task_id}.csv'

    def get_result_file_path(self, task_id: str) -> str:
        """Gets the result file path based on the task ID.

        Args:
            task_id (str): The task ID.

        Returns:
            str: The result file path if available, None otherwise.
        """
        result_file_path = self.generate_result_file_path(task_id)
        if os.path.isfile(result_file_path):
            return result_file_path
        return None


if __name__ == '__main__':
    app.run(debug=True)
