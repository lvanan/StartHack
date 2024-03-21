from model.detected_position import DetectedPositionDTO
from model.device_info import DeviceInfoDTO
from model.location import LocationDTO
from sqlalchemy import Column, Integer, String


class TelemetryDTO():
    def __init__(self, json_data):
        self.latitude = json_data["iotTelemetry"]["detectedPosition"]["latitude"]
        self.longitude = json_data["iotTelemetry"]["detectedPosition"]["longitude"]

    # def __init__(self, latitude, longitude):
    #     self.latitude = latitude
    #     self.longitude = longitude
