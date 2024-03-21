class DeviceLocationUpdate:
    def __init__(self, json_data):
        self.latitude = json_data["deviceLocationUpdate"]["latitude"]
        self.longitude = json_data["deviceLocationUpdate"]["longitude"]
        self.x_pos = json_data["deviceLocationUpdate"]["xPos"]
        self.y_pos = json_data["deviceLocationUpdate"]["yPos"]

    # def __init__(self, latitude, longitude):
    #     self.latitude = latitude
    #     self.longitude = longitude
