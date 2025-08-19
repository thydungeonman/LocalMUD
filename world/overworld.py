# world/overworld.py

from world.fellmore_cliffs import build_region as build_fellmore
from world.east_mill_plains import build_region as build_east_mill
from world.chapel import build_region as build_chapel
from utils.log_manager import verify_room_links

def load_overworld():
    overworld_rooms = {}

    # Load regions
    fellmore_rooms = build_fellmore(region_id="fellmore_cliffs")
    east_mill_rooms = build_east_mill(region_id="east_mill_plains")
    chapel_rooms = build_chapel(region_id="chapel")

    # Aggregate
    overworld_rooms.update(fellmore_rooms)
    overworld_rooms.update(east_mill_rooms)
    overworld_rooms.update(chapel_rooms)

    # Add transitions
    try:
        overworld_rooms["chapel_0_-2_0"]["exits"]["south"] = "fellmore_cliffs_1_1"
        overworld_rooms["fellmore_cliffs_1_1"]["exits"]["north"] = "chapel_0_-2_0"
    except KeyError as e:
        import logging
        logging.error(f"[ERROR] Failed to link overworld rooms: {e}")

    # Validate and log broken links
    verify_room_links(overworld_rooms)

    return overworld_rooms
