# world/overworld.py

from world.fellmore_cliffs import build_region as build_fellmore
from world.east_mill_plains import build_region as build_east_mill
from world.chapel import build_region as build_chapel

def load_overworld():
    overworld_rooms = {}

    fellmore_rooms = build_fellmore(region_id="fellmore_cliffs")
    east_mill_rooms = build_east_mill(region_id="east_mill_plains")
    chapel_rooms = build_chapel(region_id="chapel")

    overworld_rooms.update(fellmore_rooms)
    overworld_rooms.update(east_mill_rooms)
    overworld_rooms.update(chapel_rooms)

    # Optional: Add transitions to/from chapel
    overworld_rooms["chapel_0_-1_0"]["exits"]["south"] = "fellmore_cliffs_1_1"
    overworld_rooms["fellmore_cliffs_1_1"]["exits"]["north"] = "chapel_0_-1_0"


    return overworld_rooms

"""
🧩 Notes
You can expand this with more regions by importing and calling their build_region() functions.

The "exits" dict assumes your rooms follow the format: "region_id_x_y" → e.g. "fellmore_cliffs_4_2"

You can later add terrain-based transitions, flavor text, or dynamic gates.

overworld_rooms["fellmore_cliffs_4_2"]["exits"]["east"] = "east_mill_plains_0_2
"""
