# app/models.py  ← Week 11 OOP
class Incident:
    def __init__(self, date, incident_type, severity, status, description, reported_by):
        self.date = date
        self.type = incident_type
        self.severity = severity
        self.status = status
        self.description = description
        self.reporter = reported_by

    def to_dict(self):
        return self.__dict__  # For easy DB insert