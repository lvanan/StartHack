class LocationDTO:
    def __init__(self, json_data):
        self.apCount = json_data["apCount"]
        self.inferredLocationTypes = json_data["inferredLocationTypes"]
        self.locationId = json_data["locationId"]
        self.name = json_data["name"]
        self.parent = json_data["parent"]
        self.sourceLocationId = json_data["sourceLocationId"]