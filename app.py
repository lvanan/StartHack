from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import hashlib
import matplotlib.pyplot as plt

from iot_telemetry import IoTTelemetry
from random_pool import RandomPool

n = 5

def to_binary(value):
    """Convert a float32 value to its binary representation and remove the 'b' from '.'."""
    return format(np.float32(value).view(np.int32), '032b')


def apply_mask(value, mask):
    """Apply a mask to a binary string."""
    masked = ''.join(str(int(a) ^ int(b)) for a, b in zip(value, mask))
    return masked


def shuffle_string(s, seed):
    """Shuffle a string based on a given seed."""
    np.random.seed(seed)
    lst = list(s)
    np.random.shuffle(lst)
    return ''.join(lst)


def process_row(row):
    # Convert all values to binary and process them accordingly
    x_pos_bin = to_binary(row.x_pos)
    y_pos_bin = to_binary(row.y_pos)
    latitude_bin = to_binary(row.latitude)
    longitude_bin = to_binary(row.longitude)

    # Concatenate x_pos and y_pos binaries
    concat_bin = x_pos_bin + y_pos_bin

    # Use the last 4 digits of the latitude's binary as a mask
    mask = latitude_bin[-4:] * (len(concat_bin) // 4) + latitude_bin[-(len(concat_bin) % 4):]
    masked_value = apply_mask(concat_bin, mask)

    # Hash the masked value
    hashed_value = hashlib.sha256(masked_value.encode()).hexdigest()

    # Shuffle the hash based on the last 4 digits of the longitude's binary representation
    seed = int(longitude_bin[-4:], 2)
    shuffled_hash = shuffle_string(hashed_value, seed)

    return shuffled_hash


def query_coordinates():
    engine = create_engine('sqlite:///location.db')

    # Create a sessionmaker bound to the engine to create sessions
    Session = sessionmaker(bind=engine)

    # Create a session
    session = Session()

    # Query the database to fetch an entry from the "iot_telemetry" table based on some criteria
    oldest_entries = session.query(IoTTelemetry).order_by(IoTTelemetry.timestamp).limit(
        1000).all()

    # if oldest_entries:
    #     for entry in oldest_entries:
    #         session.delete(entry)
    #
    #     session.commit()

    # Close the session
    session.close()
    return oldest_entries


def init_pool():
    oldest_coordinates = query_coordinates()
    random_hashes = [process_row(row) for row in oldest_coordinates]

    pool = RandomPool()
    for hash_val in random_hashes:
        pool.add_to_pool(hash_val)

    return pool


app = Flask(__name__)

pool = init_pool()


# Define a route to render the start_page.html template
@app.route('/')
def index():
    return render_template('start_page.html')


# Define a route to handle form submissions
@app.route('/submit', methods=['POST'])
def submit():
    # print("Pool entropy:", pool.pool_entropy())
    # print("Randomness assessment (True means uniform):", pool.assess_randomness())

    # Generate a sample and remove it from the pool
    samples = set()
    for i in range(0, n):
        sample = pool.generate_sample_and_remove()
        samples.add(sample)

    # print("Sample:", sample)
    #
    # iot_telemetry_output = open("random.json", 'r+')
    # for i in range(999):
    #     sample_to_write = pool.generate_sample_and_remove()
    #     iot_telemetry_output.write(json.dumps(sample_to_write))
    #     iot_telemetry_output.write('\n')
    #
    # # name = request.form['name']
    # return str(sample)

    plt.hist(samples, bins=10, color='skyblue', edgecolor='black')
    return render_template('generator_page.html', value=str(samples))


if __name__ == '__main__':
    app.run(debug=True)
