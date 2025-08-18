# world/fellmore_cliffs.py

def build_region(region_id="fellmore_cliffs"):
    """
    Returns a dict of room_id -> room_data for Fellmore Cliffs.
    """
    rooms = {}

    # Southern approach to chapel
    rooms[f"{region_id}_1_1"] = {
        "name": "Chapel Ridge",
        "description": "A narrow path winds north toward a stone archway. The cliffs fall steeply to the west.",
        "terrain": "ridge",
        "visited": False,
        "look_description": "The path is slick with moss. You see the chapel arch rising ahead.",
        "items": [],
        "exits": {
            "north": "chapel_0_-1_0",  # Connects to Sepulchre
            "south": f"{region_id}_1_0"
        }
    }

    # Midpoint trail
    rooms[f"{region_id}_1_0"] = {
        "name": "Winding Trail",
        "description": "A winding trail hugs the cliffside. The wind howls through the rocks.",
        "terrain": "trail",
        "visited": False,
        "look_description": "Loose stones crunch underfoot. To the north, the path climbs toward the chapel.",
        "items": [],
        "exits": {
            "north": f"{region_id}_1_1",
            "south": f"{region_id}_1_-1"
        }
    }

    # Southern overlook
    rooms[f"{region_id}_1_-1"] = {
        "name": "Southern Overlook",
        "description": "You stand at the edge of the cliffs, looking out over the sea.",
        "terrain": "cliff",
        "visited": False,
        "look_description": "Far below, waves crash against jagged rocks. A faint trail leads north.",
        "items": [],
        "exits": {
            "north": f"{region_id}_1_0"
        }
    }

    # Original room preserved
    rooms[f"{region_id}_2_2"] = {
        "name": "Jagged Overlook",
        "description": "You stand atop a wind-blasted cliff. The sea crashes below.",
        "terrain": "cliff",
        "visited": False,
        "look_description": "The wind stings your face. You see distant islands on the horizon.",
        "items": [],
        "exits": {
            "north": f"{region_id}_2_1",
            "south": f"{region_id}_2_3"
        }
    }

    return rooms
