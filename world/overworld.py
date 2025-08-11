# world/overworld.py

from world.fellmore_cliffs import build_region as build_fellmore
from world.east_mill_plains import build_region as build_east_mill

def load_overworld():
    """
    Loads and merges all overworld regions into a single room map.
    Returns:
        dict: A merged dictionary of room_id -> room_data
    """
    overworld_rooms = {}

    # Load individual regions
    fellmore_rooms = build_fellmore(region_id="fellmore_cliffs")
    east_mill_rooms = build_east_mill(region_id="east_mill_plains")

    # Merge regions into overworld
    overworld_rooms.update(fellmore_rooms)
    overworld_rooms.update(east_mill_rooms)

    # Add inter-region transitions
    # Example: Fellmore room connects east into East Mill Plains
    overworld_rooms["fellmore_cliffs_2_2"]["exits"]["east"] = "east_mill_plains_0_2"
    overworld_rooms["east_mill_plains_0_2"]["exits"]["west"] = "fellmore_cliffs_2_2"


    return overworld_rooms

"""
🧩 Notes
You can expand this with more regions by importing and calling their build_region() functions.

The "exits" dict assumes your rooms follow the format: "region_id_x_y" → e.g. "fellmore_cliffs_4_2"

You can later add terrain-based transitions, flavor text, or dynamic gates.

overworld_rooms["fellmore_cliffs_4_2"]["exits"]["east"] = "east_mill_plains_0_2
"""
