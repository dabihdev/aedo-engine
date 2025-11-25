# game_builder/game_data.py (New Class)

class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
    
    def to_dict(self):
        return self.__dict__

# ⚔️ Enemy Class (Inherits from Character)
class Enemy(Character):
    def __init__(self, name, health, attack_power, reward_item_id=None):
        super().__init__(name, health)
        self.attack_power = attack_power
        self.reward_item_id = reward_item_id # ID of item dropped upon defeat

    def to_dict(self):
        # Includes all attributes from Character and Enemy
        return self.__dict__

# 🤝 NPC Class (Inherits from Character)
class NPC(Character):
    def __init__(self, name, dialogue_id, trigger_event_id=None):
        # NPCs don't usually fight, so health might be optional/set high
        super().__init__(name, 1) 
        self.dialogue_id = dialogue_id  # Key to a dialogue block in GameData
        self.trigger_event_id = trigger_event_id # Event triggered after talking

    def to_dict(self):
        return {"name": self.name, "dialogue_id": self.dialogue_id, 
                "trigger_event_id": self.trigger_event_id}