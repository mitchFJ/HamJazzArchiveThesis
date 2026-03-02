from flask import Flask, jsonify, request
from flask_cors import CORS
import csv

# To use:
# run python py_to_exe.py and leave active. This makes a server for this file.
# run python -m http.server 8000 and leave active. This makes a server for the website instead of running it from file.
# if errors arise, you may need to disable certain firewalls preventing two local servers from communicating.

app = Flask(__name__)
CORS(app)
CSV_PATH = '../extracted_text.csv'

def actual_worker():
    return("Yippee!")

@app.route('/test_returns', methods=['GET', 'POST'])
def test_returns():
    if request.method == 'POST':
        # Process data sent from JavaScript
        data = request.json.get("message")
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        else:
            print(data)
            places = []
            with open(CSV_PATH, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                # Convert each row to a dictionary and append to a list
                for row in csv_reader:
                    if (len(places)>5):
                        break
                    places.append(row)
            if len(places)>0:
                return jsonify({"answer": places[0]})
            else:
                return jsonify({"answer": "Failure to read csv"})
            result = actual_worker()
            return jsonify({"answer": result})
    else:
        # Handle GET request
        return jsonify({"message": "Hello from Python!"})
    return("Successful Interaction")
if __name__ == '__main__':
    # Run the server on http://127.0.0.1:5000
    app.run(debug=True, port=5000)