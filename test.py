from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import hashlib
import matplotlib.pyplot as plt

from iot_telemetry import IoTTelemetry
from random_pool import RandomPool


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

    device_update_output = open("coordinates.json", 'r+')

    for e in oldest_entries:
        device_update_output.write(str(e.__dict__))
        device_update_output.write('\n')

    return oldest_entries


query_coordinates()
