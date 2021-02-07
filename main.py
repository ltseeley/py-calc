"""
The Flask app.
"""


from flask import abort, json, request
from flask import Flask


# Path to the file that will persist the most recent calculations
CALC_FILE_PATH = "calculations.json"
# The number of most recent calculations to persist
CALC_LIMIT = 10
# The maximum size (in bytes) of incoming calculations that will be accepted
# (for security purposes)
CALC_MAX_SIZE = 1024;


# Initialization of the Flask app
app = Flask(__name__)


# Run the app
if __name__ == '__main__':
    app.run(threaded=True)


@app.route('/calculations', methods=['POST'])
def calculations():
    """
    Accept calculations from the web app and save them to the filesystem.
    """
    # Validate and get the incoming calculation
    if request.content_length > CALC_MAX_SIZE:
        # Max size exceeded
        abort(400);
    new_calculation = request.get_data(as_text=True)
    if not new_calculation:
        # The calculation is empty
        abort(400)

    # Save the new calculation
    try:
        with open(CALC_FILE_PATH, 'r+') as calc_file:
            # Load one less than the limit since we'll be replacing the oldest
            # calculation
            calculations = json.load(calc_file)[:CALC_LIMIT-1]
            calculations.insert(0, new_calculation)
            # Clear the file before writing the calculations
            calc_file.seek(0)
            calc_file.truncate()
            # Write the calculations
            json.dump(calculations, calc_file)
    except FileNotFoundError:
        # If the file didn't already exist, initialize it with this calculation
        with open(CALC_FILE_PATH, 'w') as calc_file:
            json.dump([new_calculation], calc_file)

    return 'Calculation added'
