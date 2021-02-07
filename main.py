"""
The Flask app.
"""


import sqlite3

from datetime import datetime
from flask import abort, render_template, request
from flask import Flask, Response
from queue import Queue


# The number of most recent calculations to load
CALC_LIMIT = 10
# The maximum size (in bytes) of incoming calculations that will be accepted
# (for security purposes)
CALC_MAX_SIZE = 1024;
# The SQLite database file used to persist calculations
DB_FILE = 'calculations.db'


# Initialization of the Flask app
app = Flask(__name__)
# Queues used to send new calculations to clients
queues = []


# Create the calculations table if it doesn't already exist
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS calculations (
    calculation text,
    timestamp text
);''')
conn.commit()
conn.close()


# Run the app
if __name__ == '__main__':
    app.run(threaded=True)


@app.route('/')
def index():
    """
    Get the calculator webpage.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT calculation FROM calculations ORDER BY timestamp DESC LIMIT ?',
        (CALC_LIMIT,))
    calculations = [row[0] for row in cursor.fetchall()]
    conn.close()

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
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO calculations VALUES (?, ?)',
        (new_calculation, datetime.now()))
    conn.commit()
    conn.close()

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

    response = Response(event_stream(q), mimetype="text/event-stream")
    # This head allows SSE to work with Google Cloud Run
    response.headers['X-Accel-Buffering'] = 'no'

    return response

def event_stream(q):
    """
    The event generator for the SSE endpoint
    """
    while True:
        yield 'data: {}\n\n'.format(q.get())
