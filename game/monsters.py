"""
game/monsters.py

Small collection of monster definitions (data-only) for LocalMUD.

Format notes (each monster is a dict):
- id            : unique string id
- name          : display name
- hd            : B/X Hit Dice (string or int; kept as int for simple math)
- hp            : typical hit points (int). If omitted, use hd * average per-die.
- ac            : Armor Class (B/X style: lower is better; e.g., 6)
- attack        : a simple attack bonus / to-hit baseline (int)
- attacks       : list of attack strings e.g., "bite 1d4"
- damage        : fallback damage expression string (e.g., "1d6")
- xp            : XP awarded for defeating the creature
- loot          : list of item ids to drop on death (optional)
- spawn_rooms   : list of room ids where this monster may spawn (optional)
- description   : short examine text

This file keeps definitions data-only so you can expand later.
"""

# Monsters:
# - Kobold - "kobold_bx"
# - (add new monsters below this line, one per line)


MONSTER_DEFS = {
    "kobold_bx": {
        "id": "kobold_bx",
        "name": "Kobold",
        "hd": 1,
        "hp": 4,
        "ac": 7,
        "attack": 0,
        "attacks": ["spear 1d6"],
        "damage": "1d6",
        "xp": 25,
        "loot": ["kobold_tooth"],
        "base_stats": {
            "str": 8,
            "dex": 13,
            "con": 10,
            "int": 8,
            "wis": 7,
            "cha": 8
        },
        "hostile": True,
        "description": (
            "A small, scaly humanoid with a sly grin and a crude spear. "
            "Kobolds are weak individually but can be dangerous in groups."
        )
    }
}


# Helper: expose a canonical list of monster ids (convenient for tooling)
MONSTER_IDS = list(MONSTER_DEFS.keys())
