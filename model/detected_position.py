class DetectedPositionDTO:
    def __init__(self, json_data):
        self.confidenceFactor = json_data["confidenceFactor"]
        self.lastLocatedTime = json_data["lastLocatedTime"]
        self.latitude = json_data["latitude"]
        self.locationId = json_data["locationId"]
        self.longitude = json_data["longitude"]
        self.mapId = json_data["mapId"]
        self.xPos = json_data["xPos"]
        self.yPos = json_data["yPos"]