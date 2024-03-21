import hashlib
from flask import Flask, render_template, request

from model.telemetry_dto import TelemetryDTO


def random_int_from_xy(x, y, M=100):
    # Step 1: Convert x and y to string and concatenate
    input_str = str(x) + str(y)

    # Step 2: Hash the concatenated string using SHA-256
    hash_output = hashlib.sha256(input_str.encode()).hexdigest()

    # Step 3: Convert the hexadecimal hash to an integer
    hash_int = int(hash_output, 16)

    # Step 4: Scale the integer to the range 0 to M using modulo
    random_int = hash_int % M

    return str(random_int)


def query_coordinates():
    return TelemetryDTO(1, 3)


app = Flask(__name__)


# Define a route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')


# Define a route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    telemetry = query_coordinates()
    random_number = random_int_from_xy(telemetry.longitude, telemetry.latitude)
    # name = request.form['name']
    return random_number


if __name__ == '__main__':
    app.run(debug=True)
