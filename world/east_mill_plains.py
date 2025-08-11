# world/east_mill_plains.py

def build_region(region_id="east_mill_plains"):
    """
    Returns a dict of room_id -> room_data for East Mill Plains.
    """
    rooms = {}

    # Example room
    rooms[f"{region_id}_0_2"] = {
        "name": "Grassy Verge",
        "description": "Tall grass sways gently in the breeze. A dirt path leads west.",
        "terrain": "plains",
        "exits": {
            "west": f"{region_id}_0_1",
            "east": f"{region_id}_0_3"
        }
    }

    return rooms
