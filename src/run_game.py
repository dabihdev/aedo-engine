from game_engine import GameEngine

engine = GameEngine()

if engine.load_game("my_adventure.json"):
    engine.run()