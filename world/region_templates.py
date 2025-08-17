#region_templates.py
import random

REGIONS = {
    "fellmore_cliffs": {
        "bounds": {"x_min": 0, "x_max": 4, "y_min": 0, "y_max": 4},
        "terrain": ["rocky ledge", "crumbling path", "windy bluff"],
        "flavor": [
            "Jagged cliffs loom overhead.",
            "Loose stones crunch underfoot.",
            "A raven circles in the distance."
        ]
    },
    "east_mill_plains": {
        "bounds": {"x_min": 5, "x_max": 9, "y_min": 0, "y_max": 4},
        "terrain": ["grassy field", "gentle hill", "streambed"],
        "flavor": [
            "The wind rustles through tall grass.",
            "A faint trail leads east.",
            "You hear distant birdsong."
        ]
    }
}

def generate_room_templates(region_name: str) -> Dict[str, dict]:
    region = REGIONS.get(region_name)
    if not region:
        raise ValueError(f"Unknown region: {region_name}")

    x_min, x_max = region["bounds"]["x_min"], region["bounds"]["x_max"]
    y_min, y_max = region["bounds"]["y_min"], region["bounds"]["y_max"]
    terrain = region["terrain"]
    flavor = region["flavor"]

    rooms = {}

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            room_id = f"{region_name}_{x}_{y}"
            room = {
                "name": room_id,
                "description": random.choice(flavor),
                "terrain": random.choice(terrain),
                "exits": {},
                "items": [],
                "npcs": []
            }

            # Add exits based on adjacency
            if y < y_max:
                room["exits"]["north"] = f"{region_name}_{x}_{y + 1}"
            if y > y_min:
                room["exits"]["south"] = f"{region_name}_{x}_{y - 1}"
            if x < x_max:
                room["exits"]["east"] = f"{region_name}_{x + 1}_{y}"
            if x > x_min:
                room["exits"]["west"] = f"{region_name}_{x - 1}_{y}"

            rooms[room_id] = room

    return rooms
