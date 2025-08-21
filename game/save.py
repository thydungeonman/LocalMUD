# save.py

import os
import json

def save_player(player):
    save_dir = "save"
    os.makedirs(save_dir, exist_ok=True)  # ✅ Create 'save/' if it doesn't exist

    save_path = os.path.join(save_dir, "player.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(player, f, indent=2)


def load_player():
    try:
        with open("save/player.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None



