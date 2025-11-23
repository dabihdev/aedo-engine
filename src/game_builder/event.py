# game_builder/game_data.py (GameData Extension)

class Event:
    def __init__(self, event_id, event_type, data):
        self.event_id = event_id
        self.event_type = event_type  # e.g., "dialogue", "read", "chest"
        self.data = data # Varies based on type (e.g., list of lines, key to unlock, item list)
    
    def to_dict(self):
        return self.__dict__

class GameData:
    def __init__(self, start_room_id):
        # ... existing attributes
        self.events = {} # New dictionary to store Event objects

    def add_event(self, event):
        self.events[event.event_id] = event

    def to_dict(self):
        return {
            # ... existing fields
            "events": {id: event.to_dict() for id, event in self.events.items()}
        }