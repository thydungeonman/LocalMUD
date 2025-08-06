# rooms.py
"""
LocalMUD — Room Definitions

Contains all room data, including descriptions, connections, and any special flags.
Each room is defined as a dictionary entry with relevant metadata.

Typical usage:
- Accessed by parser.py to handle movement
- Used by UI to display room descriptions

Author: Alex

Dev Notes:
- Room keys should be unique and descriptive.
- Consider adding room-specific events, triggers, or lore hooks.
- Modular room loading from external files could be added later.
"""

"""
        (0, 1, 0, "chapel"): {
        "name": "Vault of the Namless Dead",
        "description": "A dusty mausoleum with many old graves.",
        "visited": False,
        "look_description": "Graves line the walls top to bottom. Some are too to read. Light flickers gently through the adjacent rooms.",
        "items": [],
        "exits": {"south": (0, 0, 0, "chapel")},
        "examine_targets": {
            "graves": "Honored resting places of old heroes."
        }
    },


"""




rooms = {
    (0, 0, 0, "chapel"): {
        "name": "Pedestal Chamber",
        "description": "A quiet chamber with a glowing orb resting on a pedestal.",
        "visited": False,
        "look_description": "Dust motes float in the air. The pedestal is carved with ancient symbols.",
        "items": ["Glowing Orb"],
        "exits": {
            "east": (1, 0, 0, "chapel"),
            "north": (0, 1, 0, "chapel"),
            "south": (0, -1, 0, "chapel")
        },
        "examine_targets": {
            "pedestal": "The pedestal is carved from obsidian. Symbols etched into its surface seem to shift when you stare too long.",
            "symbols": "The symbols resemble constellations, but none you recognize. One looks like a ladle."
        }
    },
    (1, 0, 0, "chapel"): {
        "name": "Altar Room",
        "description": "An ancient altar stands in silence. Something feels incomplete.",
        "visited": False,
        "look_description": "The altar is cracked and worn. Faint traces of glowing runes shimmer beneath the dust.",
        "items": [],
        "exits": {"west": (0, 0, 0, "chapel")},
        "examine_targets": {
            "altar": "The altar bears a shallow indentation, perfectly orb-shaped.",
            "runes": "The runes pulse faintly. One resembles the symbol on the pedestal."
        },
        "triggers": [
            {
                "condition": "has_item",
                "item": "Glowing Orb",
                "effect": "win"
            },
            {
                "condition": "requires_item",
                "item": "Rusty Key"
            }
        ]
    },

        (0, 1, 0, "chapel"): {
        "name": "Vault of the Nameless Dead",
        "description": "A dusty mausoleum with many old graves.",
        "visited": False,
        "look_description": "Graves line the walls top to bottom. Some are too worn to read. Light flickers gently through the adjacent rooms.",
        "items": [],
        "exits": {
            "south": (0, 0, 0, "chapel"),
            "east": (1, 1, 0, "chapel")
            },
        "examine_targets": {
            "graves": "Honored resting places of old heroes."
        }
    },
        (1, 1, 0, "chapel"): {
        "name": "Chamber of the Weeping Saints",
        "description": "Statues of angels and saints surround a table carved in stone.",
        "visited": False,
        "look_description": "Several statues are pointed towards a table in the center of the room.",
        "items": ["Rusty Key"],
        "exits": {"west": (0, 1, 0, "chapel")},
        "examine_targets": {
            "statues": "They stay put when you arent looking. Blinking is perfectly safe."
        }
    },
    
        (0, -1, 0, "chapel"): {
        "name": "The Sepulchure of Ink and Dust",
        "description": "The entry area to the mausoleum.",
        "visited": False,
        "look_description": "A log book sits open on an ornate display. To the north, a stone archway leads to the mausoleum. To the south is a red curtain leading to the sanctuary.",
        "items": [],
        "exits": {
            "north": (0, 0, 0, "chapel"),
            "south": (0, -2, 0, "chapel")
            },
        "examine_targets": {
            "book": "It's filled with the names of the dead and where they are located.",
            "log book": "It's filled with the names of the dead and where they are located.",
            "log": "It's filled with the names of the dead and where they are located."
        }
    },

        (0, -2, 0, "chapel"): {
        "name": "Sanctuary",
        "description": "An old sanctuary, complete with lectern and pews..",
        "visited": False,
        "look_description": "A lectern stands in front of six old wooden pews. Very old tapestries hang from the walls. Father Ansel keeps this sanctuary open, but it has been a long time since someone has heard a sermon here.",
        "items": [],
        "exits": {
            "north": (0, -1, 0, "chapel"),
            "south": (0, -3, 0, "chapel")
            },
        "examine_targets": {
            "pews": "Seating for visiters to hear the sermon. Carved from ancient oak.",
            "pew": "Seating for visiters to hear the sermon. Carved from ancient oak.",
            "lectern": "The lectern stands at the forefront of the sanctuary. Like the pews, it is carved of ancient oak.",
            "tapestries": "Faded scenes of judgment and harvest."
        }
    },
    
    
    
}
