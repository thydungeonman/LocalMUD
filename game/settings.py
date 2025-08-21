import os
import json

SETTINGS_PATH = os.path.join("save", "settings.json")

DEFAULT_SETTINGS = {
    "max_hp_bonus": False,
    "verbose_travel": False,
    "screen_reader_mode": False,
    "debug_mode": False
}

def save_settings(player):
    os.makedirs("save", exist_ok=True)
    settings = {key: player.get(key, DEFAULT_SETTINGS[key]) for key in DEFAULT_SETTINGS}
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()
