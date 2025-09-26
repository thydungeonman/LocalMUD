# player.py
"""
LocalMUD — Base Player Template

Defines the default player dictionary, including starting stats, inventory,
and metadata. Used as the foundation for character creation and gameplay.

Typical usage:
- Imported by character.py and main.py
- Modified during character creation and gameplay events

Author: Alex

Dev Notes:
- Keep this file clean and declarative—no logic, just data.
- Future expansions may include default traits, flags, or status effects.
- Consider separating persistent vs. session-based data if save/load is added.
"""


player = {
    "name": "Hero",
    "location": "chapel_0_0_0",
    "inventory": [],
    "visited": {"chapel_0_0_0"},  # seed with starting coords
    "hp": 6,
    "max_hp": 6,
    "ac": 7,  # Armor Class (descending) lower is better
    "str": 13, #Melee attack bonuys, Carry Weight
    "dex": 9, #AC Bonus, Ranged Attack Bonus
    "con": 12, #HP Bonus Per Level
    "int": 10, #Spell Learning
    "wis": 8, #Saving Throws, Divine Magic
    "cha": 11, #npc reactions, hirelings
    "level": 1, 
    "xp": 0,
    "gold": 100,  # Starting gold
    "status": [],
    "flags": {},
    "curse_count": 0,  # Added for dirty word tracking
    "verbose_travel": False,
    "screen_reader_mode": True,
    "debug_mode": False,
}
