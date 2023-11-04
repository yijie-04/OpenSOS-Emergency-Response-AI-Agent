#data structure
class caller:
    def __init__(self, call_id, caller_phone, caller_name, symptoms = None,
                 incident_type = None, incident_location = None, timestamp = None, priority=None):
        self.call_id = call_id
        self.caller_phone = caller_phone
        self.incident_location = incident_location
        self.incident_type = incident_type
        self.caller_name = caller_name
        self.priority = priority
        self.timestamp = timestamp
