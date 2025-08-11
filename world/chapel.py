# world/chapel.py

def build_region(region_id="chapel"):
    return {
        "0_0_0_chapel": {
            "name": "Dusty Chapel",
            "description": "The chapel is dusty and quiet. Its silence feels safe—but not empty...",
            "exits": {
                "south": "fellmore_cliffs_2_2"
            },
            "terrain": "interior",
            "items": [],
            "npcs": []
        }
    }
