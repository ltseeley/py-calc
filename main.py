"""
The Flask app.
"""


from flask import abort, json, render_template, request
from flask import Flask, Response
from queue import Queue


# Path to the file that will persist the most recent calculations
CALC_FILE_PATH = "calculations.json"
# The number of most recent calculations to persist
CALC_LIMIT = 10
# The maximum size (in bytes) of incoming calculations that will be accepted
# (for security purposes)
CALC_MAX_SIZE = 1024;


# Initialization of the Flask app
app = Flask(__name__)
# Queues used to send new calculations to clients
queues = []


# Run the app
if __name__ == '__main__':
    app.run(threaded=True)


@app.route('/')
def index():
    """
    Get the calculator webpage.
    """
    try:
        calculations = json.load(open(CALC_FILE_PATH, 'r'))
    except FileNotFoundError:
        calculations = []

    return render_template('calculator.html', calculations=calculations)


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

    # Notify any active clients of the new calculation
    for q in queues:
        q.put(new_calculation)

    return 'Calculation added'


@app.route('/calculations/stream')
def calculations_stream():
    """
    Subscribe to a stream of server-sent events (SSE) that notify the client of
    new calculations.
    """
    # Create a new queue and add it to the list of queues to be notified of new
    # calculations
    q = Queue()
    global queues
    queues.append(q)

    return Response(event_stream(q), mimetype="text/event-stream")

def event_stream(q):
    """
    The event generator for the SSE endpoint
    """
    while True:
        yield 'data: {}\n\n'.format(q.get())
