# items.py
"""
LocalMUD — Item Definitions

Stores all item data, including names, descriptions, and any special properties.
Items can be referenced in player inventory or room contents.

Typical usage:
- Accessed by parser.py for item interactions
- Used by character.py or future loot systems

Author: Alex

Dev Notes:
- Items are currently static; future versions may support dynamic effects or scripting.
- Consider tagging items with rarity, type, or lore categories.
- Modular item loading from external files could support modding.
"""

items = {
    "glowing_orb": {
        "name": "Glowing Orb",
        "description": "A mysterious orb that pulses with faint light.",
        "examine_text": "The orb is warm to the touch. Symbols swirl inside, forming patterns that resemble constellations.",
        "type": "quest",
        "spawn": {
            "rooms": ["chapel_1_0_0"],  # Converted from (1, 0, 0, "chapel")
            "spawn_chance": 1.0,        # Always appears in this room
            "unique": True              # Only one exists
        },
        "use": {
            "effect": "win",
            "location": "chapel_1_0_0",
            "message": "You place the orb on the altar. A warm light fills the room. You win!"
        }
    },

    "rusty_key": {
        "name": "Rusty Key",
        "description": "An old iron key. It looks like it could unlock something.",
        "examine_text": "The key is engraved with the number 7. Its teeth are worn but intact.",
        "type": "key",
        "spawn": {
            "rooms": ["chapel_2_0_0"],
            "spawn_chance": 1.0,
            "unique": True
        },
        "use": {
            "effect": "unlock",
            "location": "chapel_2_0_0",
            "target": "door",
            "message": "You unlock the heavy door with the rusty key."
        }
    }
}
