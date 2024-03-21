class DeviceInfoDTO:
    def __init__(self, json_data):
        self.companyId = json_data["companyId"]
        self.deviceId = json_data["deviceId"]
        self.deviceMacAddress = json_data["deviceMacAddress"]
        self.deviceModel = json_data["deviceModel"]
        self.deviceName = json_data["deviceName"]
        self.deviceType = json_data["deviceType"]
        self.firmwareVersion = json_data["firmwareVersion"]
        self.label = json_data["label"]
        self.manufacturer = json_data["manufacturer"]
        self.rawDeviceId = json_data["rawDeviceId"]
        self.serviceUuid = json_data["serviceUuid"]
        self.vendorId = json_data["vendorId"]