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

MONSTER_DEFS = {
    "kobold_bx": {
        "id": "kobold_bx",
        "name": "kobold",
        "hd": 1,                       # 1 HD creature in B/X
        "hp": 4,                       # typical HP (1d6 -> avg 3-4)
        "ac": 7,                       # B/X AC (lower is better; 7 = leather/average)
        "attack": 0,                   # baseline to-hit modifier (simple systems may ignore)
        "attacks": ["spear 1d6"],      # flavor; single attack with spear
        "damage": "1d6",               # fallback damage if needed
        "xp": 25,                      # award XP for kill (small B/X-appropriate amount)
        "loot": ["kobold_tooth"],      # item ids; optional and can be created in items table
        "description": (
            "A small, scaly humanoid with a sly grin and a crude spear. "
            "Kobolds are weak individually but can be dangerous in groups."
        )
    }
}

# Helper: expose a canonical list of monster ids (convenient for tooling)
MONSTER_IDS = list(MONSTER_DEFS.keys())
