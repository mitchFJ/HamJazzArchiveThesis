from flask import Flask, jsonify, request
from flask_cors import CORS

# To use:
# run python py_to_exe.py and leave active. This makes a server for this file.
# run python -m http.server 8000 and leave active. This makes a server for the website instead of running it from file.
# if errors arise, you may need to disable certain firewalls preventing two local servers from communicating.

app = Flask(__name__)
CORS(app)

def actual_worker():
    return("Yippee!")

@app.route('/test_returns', methods=['GET', 'POST'])
def test_returns():
    if request.method == 'POST':
        # Process data sent from JavaScript
        data = request.json.get("value")
        print(f"Received data from JS: {data['message']}")
        # Return a response
        result = actual_worker()
        return jsonify(result)
    else:
        # Handle GET request
        return jsonify({"message": "Hello from Python!"})
    return("Successful Interaction")
if __name__ == '__main__':
    # Run the server on http://127.0.0.1:5000
    app.run(debug=True, port=5000)