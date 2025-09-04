# items.py


items = {
    "rusty_key": {
        "name": "Rusty Key",
        "description": "An old iron key. It looks like it could unlock something.",
        "examine_text": "The key is engraved with the number 7. Its teeth are worn but intact.",
        "type": "key",
        "spawn": {
            "rooms": ["chapel_2_0_0"],  # normalized room ID
            "spawn_chance": 1.0,        # guaranteed spawn
            "unique": True              # only one copy exists
        },
        "use": {
            "effect": "unlock",
            "use_location": "chapel_2_0_0",
            "target": "door",
            "message": "You unlock the heavy door with the rusty key."
        }
    },

    "glowing_orb": {
        "name": "Glowing Orb",
        "description": "A mysterious orb that pulses with faint light.",
        "examine_text": "The orb is warm to the touch. Symbols swirl inside, forming patterns that resemble constellations.",
        "type": "quest",
        "spawn": {
            "rooms": ["chapel_1_0_0"],
            "spawn_chance": 1.0,
            "unique": True
        },
        "use": {
            "effect": "win",
            "use_location": "chapel_1_0_0",
            "message": "You place the orb on the altar. A warm light fills the room. You win!"
        }
    }
}
