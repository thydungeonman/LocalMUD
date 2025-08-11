
# world/fellmore_cliffs.py

def build_region(region_id="fellmore_cliffs"):
    """
    Returns a dict of room_id -> room_data for Fellmore Cliffs.
    """
    rooms = {}

    # Example room
    rooms[f"{region_id}_2_2"] = {
        "name": "Jagged Overlook",
        "description": "You stand atop a wind-blasted cliff. The sea crashes below.",
        "terrain": "cliff",
        "exits": {
            "north": f"{region_id}_2_1",
            "south": f"{region_id}_2_3"
        }
    }

    return rooms
