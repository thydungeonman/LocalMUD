# world/chapel.py

def build_region(region_id="chapel"):
    return {
        f"{region_id}_0_0_0": {
            "name": "Pedestal Chamber",
            "description": "A quiet chamber with a glowing orb resting on a pedestal.",
            "visited": False,
            "look_description": "Dust motes float in the air. The pedestal is carved with ancient symbols.",
            "items": ["Glowing Orb"],
            "exits": {
                "east": f"{region_id}_1_0_0",
                "north": f"{region_id}_0_1_0",
                "south": f"{region_id}_0_-1_0"
            },
            "examine_targets": {
                "pedestal": "The pedestal is carved from obsidian. Symbols etched into its surface seem to shift when you stare too long.",
                "symbols": "The symbols resemble constellations, but none you recognize. One looks like a ladle."
            }
        },
        f"{region_id}_1_0_0": {
            "name": "Altar Room",
            "description": "An ancient altar stands in silence. Something feels incomplete.",
            "visited": False,
            "look_description": "The altar is cracked and worn. Faint traces of glowing runes shimmer beneath the dust.",
            "items": [],
            "exits": {"west": f"{region_id}_0_0_0"},
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
        f"{region_id}_0_1_0": {
            "name": "Vault of the Nameless Dead",
            "description": "A dusty mausoleum with many old graves.",
            "visited": False,
            "look_description": "Graves line the walls top to bottom. Some are too worn to read. Light flickers gently through the adjacent rooms.",
            "items": [],
            "exits": {
                "south": f"{region_id}_0_0_0",
                "east": f"{region_id}_1_1_0"
            },
            "examine_targets": {
                "graves": "Honored resting places of old heroes."
            }
        },
        f"{region_id}_1_1_0": {
            "name": "Chamber of the Weeping Saints",
            "description": "Statues of angels and saints surround a table carved in stone.",
            "visited": False,
            "look_description": "Several statues are pointed towards a table in the center of the room.",
            "items": ["Rusty Key"],
            "exits": {"west": f"{region_id}_0_1_0"},
            "examine_targets": {
                "statues": "They stay put when you aren't looking. Blinking is perfectly safe."
            }
        },
        f"{region_id}_0_-1_0": {
            "name": "The Sepulchre of Ink and Dust",
            "description": "The entry area to the mausoleum.",
            "visited": False,
            "look_description": "A log book sits open on an ornate display. To the north, a stone archway leads to the mausoleum. To the south is a red curtain leading to the sanctuary.",
            "items": [],
            "exits": {
                "north": f"{region_id}_0_0_0"
            },
            "examine_targets": {
                "book": "It's filled with the names of the dead and where they are located.",
                "log book": "It's filled with the names of the dead and where they are located.",
                "log": "It's filled with the names of the dead and where they are located."
            }
        },
        f"{region_id}_0_-2_0": {
            "name": "Sanctuary",
            "description": "An old sanctuary, complete with lectern and pews.",
            "visited": False,
            "look_description": "A lectern stands in front of six old wooden pews. Very old tapestries hang from the walls. Father Ansel keeps this sanctuary open, but it has been a long time since someone has heard a sermon here.",
            "items": [],
            "exits": {
                "north": f"{region_id}_0_-1_0",
                "south": f"{region_id}_0_-3_0"
            },
            "examine_targets": {
                "pews": "Seating for visitors to hear the sermon. Carved from ancient oak.",
                "pew": "Seating for visitors to hear the sermon. Carved from ancient oak.",
                "lectern": "The lectern stands at the forefront of the sanctuary. Like the pews, it is carved of ancient oak.",
                "tapestries": "Faded scenes of judgment and harvest."
            }
        }
    }
