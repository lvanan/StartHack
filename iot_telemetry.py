from sqlalchemy import Column, Integer, Float, String
from base import Base


class IoTTelemetry(Base):
    __tablename__ = 'iot_telemetry'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    x_pos = Column(Float)
    y_pos = Column(Float)
    timestamp = Column(String)

    def __init__(self, json_data, timestamp):
        self.latitude = json_data["iotTelemetry"]["detectedPosition"]["latitude"]
        self.longitude = json_data["iotTelemetry"]["detectedPosition"]["longitude"]
        self.x_pos = json_data["iotTelemetry"]["detectedPosition"]["xPos"]
        self.y_pos = json_data["iotTelemetry"]["detectedPosition"]["yPos"]
        self.timestamp = timestamp

    def __json__(self): return {"latitude": self.latitude, "longitude": self.longitude, "x_pos": self.x_pos,
                                "y_pos": self.y_pos, "timestamp": self.timestamp}
