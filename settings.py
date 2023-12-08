from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/settings', methods=['POST'])
def settings():
    try:
        # Assuming you want to handle file uploads in this route
        if 'dataFile' not in request.files or 'refFile' not in request.files:
            return "No file part in the request", 400

        data_file = request.files['dataFile']
        ref_file = request.files['refFile']

        # Continue with your file processing logic
        # ...

        return "Files uploaded successfully"

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
