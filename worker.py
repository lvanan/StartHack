from datetime import datetime

import requests
import json
import socket
import os
import sqlite3
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from device_location_update import DeviceLocationUpdate
from iot_telemetry import IoTTelemetry

con = sqlite3.connect("tutorial.db")

from collections import Counter
import math


def randomness_check(binary_string):
    # Runs randomnesschecks on string
    entropy_per_bit = calculate_binary_entropy(binary_string)
    print(f"Entropy per bit: {entropy_per_bit}")
    if entropy_per_bit > 0.997:
        return True
    return True  # False #xxxtodo


def calculate_binary_entropy(binary_string):
    # Calculates entropy per bit and returns it: 0 -> no entropy, 1 -> surrealisticly high entropy

    # Count occurrences of 0 and 1
    frequency = Counter(binary_string)
    total_bits = len(binary_string)

    # Calculate probabilities
    p0 = frequency['0'] / total_bits if '0' in frequency else 0
    p1 = frequency['1'] / total_bits if '1' in frequency else 0

    if (abs(1 - p0 - p1) > 0.01):
        raise ValueError("probability does not add up")

    # Avoid calculating log(0) if all bits are 0s or 1s
    entropy = 0
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    if p1 > 0:
        entropy -= p1 * math.log2(p1)

    return entropy


def random_int_from_xy(x, y, M=100):
    # Step 1: Convert x and y to string and concatenate
    input_str = extract_decimal_digits(x) + extract_decimal_digits(y)
    # print(extract_decimal_digits(x), extract_decimal_digits(y))
    # print(input_str)

    # Convert the digit string to a binary string
    binary_string = ''.join(format(int(d), 'b') for d in input_str)
    print(binary_string)
    r = randomness_check(binary_string)

    # Step 2: Hash the concatenated string using SHA-256
    hash_output = hashlib.sha256(input_str.encode()).hexdigest()

    # Step 3: Convert the hexadecimal hash to an integer
    hash_int = int(hash_output, 16)

    # Step 4: Scale the integer to the range 0 to M using modulo
    random_int = hash_int % M

    return random_int, r


def extract_decimal_digits(float_num):
    # Convert float number to string
    float_str = str(float_num)

    # Find the index of the decimal point
    decimal_index = float_str.find('.')

    # Extract the substring after the decimal point
    if decimal_index != -1:
        decimal_digits = float_str[decimal_index + 1:]
    else:
        # If there's no decimal point, return an empty string
        decimal_digits = ""

    return decimal_digits


def get_API_Key_and_auth():
    # Gets public key from spaces and places in correct format
    print("-- No API Key Found --")

    # Gets user to paste in generated token from app
    token = input('Enter provided API key here: ')

    # Writes activation key to file. This key can be used to open up Firehose connection
    f = open("API_KEY_LAB.txt", "a")
    f.write(token)
    f.close()
    return token


# work around to get IP address on hosts with non resolvable hostnames
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_ADRRESS = s.getsockname()[0]
s.close()
url = 'http://' + str(IP_ADRRESS) + '/update/'

# Tests to see if we already have an API Key
try:
    if os.stat("API_KEY_LAB.txt").st_size > 0:
        # If we do, lets use it
        f = open("API_KEY_LAB.txt")
        apiKey = f.read()
        f.close()
    else:
        # If not, lets get user to create one
        apiKey = get_API_Key_and_auth()
except:
    apiKey = get_API_Key_and_auth()


# overwrite previous log file
f = open("logs.json", 'r+')
device_update_output = open("device_update_output.txt", 'r+')
iot_telemetry_output = open("iot_telemetry_output.txt", 'r+')
json.dump({}, f)
json.dump({}, device_update_output)
json.dump({}, iot_telemetry_output)
f.truncate(0)

# Opens a new HTTP session that we can use to terminate firehose onto
s = requests.Session()
s.headers = {'X-API-Key': apiKey}
r = s.get(
    'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)  # Change this to .io if needed

# Jumps through every new event we have through firehose
print("Starting Stream")
event_types = set()

engine = create_engine('sqlite:///location.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

records_to_save = set()

for line in r.iter_lines():
    if line:
        # decodes payload into useable format
        decoded_line = line.decode('utf-8')
        event = json.loads(decoded_line)

        # writes every event to the logs.json in readible format
        f.write(str(json.dumps(json.loads(line), indent=4, sort_keys=True)))

        # gets the event type out the JSON event and prints to screen
        eventType = event['eventType']

        event_types.add(eventType)
        print(event_types)

        if eventType == 'DEVICE_LOCATION_UPDATE':
            try:
                telemetry_dto = DeviceLocationUpdate(event)
                # random_number, random_check = random_int_from_xy(telemetry_dto.latitude % 1,
                #                                                  telemetry_dto.longitude % 1)
                print(str(telemetry_dto.__dict__))
                device_update_output.write(str(telemetry_dto.__dict__))
                device_update_output.write('\n')

            except Exception as e:
                print(f"something is off: {e}")

        if eventType == 'IOT_TELEMETRY':
            try:
                iot_telemetry = IoTTelemetry(event, datetime.now().strftime('%Y%m%d%H%M%S'))
                if not records_to_save.__contains__(iot_telemetry):
                    records_to_save.add(iot_telemetry)

                if len(records_to_save) > 100:
                    session.add_all(records_to_save)
                    session.commit()
                    json_data = [obj.__json__() for obj in records_to_save]
                    iot_telemetry_output.write(json.dumps(json_data))
                    records_to_save.clear()

            except Exception as e:
                print(f"something is off: {e}")

session.close()
