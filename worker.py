import requests
import json
import socket
import os
import sqlite3
import hashlib


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model.detected_position import DetectedPositionDTO
from model.telemetry_dto import TelemetryDTO

con = sqlite3.connect("tutorial.db")
Base = declarative_base()


def random_int_from_xy(x, y, M=100):
    # Step 1: Convert x and y to string and concatenate
    input_str = str(x) + str(y)

    # Step 2: Hash the concatenated string using SHA-256
    hash_output = hashlib.sha256(input_str.encode()).hexdigest()

    # Step 3: Convert the hexadecimal hash to an integer
    hash_int = int(hash_output, 16)

    # Step 4: Scale the integer to the range 0 to M using modulo
    random_int = hash_int % M

    return random_int


def save_to_db(decoded_line):
    engine = create_engine('sqlite:///example.db')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()

    session.add(decoded_line)

    session.commit()
    session.close()


def get_API_Key_and_auth():
    # Gets public key from spaces and places in correct format
    print("-- No API Key Found --")

    # Gets user to paste in generated token from app
    token = input('Enter provided API key here: ')

    # Writes activation key to file. This key can be used to open up Firehose connection
    f = open("API_KEY.txt", "a")
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
    if os.stat("API_KEY.txt").st_size > 0:
        # If we do, lets use it
        f = open("API_KEY.txt")
        apiKey = f.read()
        f.close()
    else:
        # If not, lets get user to create one
        apiKey = get_API_Key_and_auth()
except:
    apiKey = get_API_Key_and_auth()

# overwrite previous log file
f = open("logs.json", 'r+')
ran = open("random.txt", 'r+')
json.dump({}, f)
f.truncate(0)

# Opens a new HTTP session that we can use to terminate firehose onto
s = requests.Session()
s.headers = {'X-API-Key': apiKey}
r = s.get(
    'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)  # Change this to .io if needed

# Jumps through every new event we have through firehose
print("Starting Stream")
for line in r.iter_lines():
    if line:
        # decodes payload into useable format
        decoded_line = line.decode('utf-8')
        event = json.loads(decoded_line)

        # writes every event to the logs.json in readible format
        f.write(str(json.dumps(json.loads(line), indent=4, sort_keys=True)))

        # gets the event type out the JSON event and prints to screen
        eventType = event['eventType']

        print(eventType)
        if eventType == 'IOT_TELEMETRY':
            try:
                telemetry_dto = TelemetryDTO(event)
                random_number = random_int_from_xy(telemetry_dto.latitude % 1, telemetry_dto.longitude % 1)
                print(random_number)
                ran.write(str(random_number))
                ran.write('\n')
            except Exception as e:
                print(f"something is off: {e}")

