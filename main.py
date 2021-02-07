"""
The Flask app.
"""


from flask import Flask


# Initialization of the Flask app
app = Flask(__name__)


# Run the app
if __name__ == '__main__':
    app.run(threaded=True)
