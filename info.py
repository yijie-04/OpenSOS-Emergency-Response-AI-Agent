#data structure
from datetime import datetime

class Caller:
    def __init__(self, caller_name = "XXX", symptoms = "XXX",
                 incident_type = "XXX", incident_location = "XXX", timestamp=None, priority=None,
                 call_id = '123', caller_phone = '555-1234',
                 severity = None):
        self.call_id = call_id
        self.caller_phone = caller_phone
        self.incident_location = incident_location
        self.symptoms = symptoms
        self.incident_type = incident_type
        self.caller_name = caller_name
        self.priority = priority
        self.timestamp = timestamp if timestamp is not None else datetime.now()
        self.severity = severity
    
    def print_info(self):
        for attribute, value in self.__dict__.items():
            print(f"{attribute}: {value}")