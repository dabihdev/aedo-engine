"""Initialization for the game_builder package."""
from .game_data import GameData, Room, Item, Character, Enemy, NPC, Event
from .builder import GameBuilder

# Expose core classes for easy import: from game_builder import GameBuilder, Room, Item, etc.
__all__ = ['GameData', 'Room', 'Item', 'Character', 'Enemy', 'NPC', 'Event', 'GameBuilder']