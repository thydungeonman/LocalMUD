# /world/room_builder.py

import logging
from typing import Dict, Optional
from . import region_templates

# Map directions to their opposites for automatic two-way linking
OPPOSITE_DIRECTIONS = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
    "up": "down",
    "down": "up",
    "northeast": "southwest",
    "northwest": "southeast",
    "southeast": "northwest",
    "southwest": "northeast",
}


def build_region(region_name: str, bidirectional: bool = True) -> Dict[str, dict]:
    """
    Create all rooms for `region_name` and wire up exits.
    Returns a dict of room_id -> room_dict.
    """
    tmpl = region_templates.REGION_TEMPLATES.get(region_name)
    if not tmpl:
        raise ValueError(f"Unknown region: {region_name}")

    # Step 1: Instantiate room dicts
    rooms: Dict[str, dict] = {}
    for room_id, room_t in tmpl["rooms"].items():
        rooms[room_id] = build_room(room_id, room_t)

    # Step 2: Resolve exits to actual room dicts (or None)
    connect_rooms(rooms, bidirectional=bidirectional)

    return rooms


def build_room(room_id: str, tmpl: dict) -> dict:
    """
    Build a single room dict from its template.
    """
    return {
        "id": room_id,
        "name": tmpl.get("name", room_id),
        "description": tmpl.get("description", ""),
        "exits": dict(tmpl.get("exits", {})),  # direction -> target room_id
        "items": list(tmpl.get("items", [])),
        "npcs": list(tmpl.get("npcs", [])),
        # you can add more keys here (terrain, flags, etc.)
    }


def connect_rooms(
    rooms: Dict[str, dict], bidirectional: bool = True
) -> None:
    """
    Replace each room's exit targets (room_ids) with actual room dicts.
    If bidirectional is True, automatically add reverse exits where possible.
    """
    # First resolve forward links
    for room in rooms.values():
        resolved = {}
        for direction, target_id in room["exits"].items():
            target = rooms.get(target_id)
            if not target:
                logging.warning(
                    f"{room['id']} has exit '{direction}' -> unknown room '{target_id}'"
                )
            resolved[direction] = target
        room["exits"] = resolved

    # Then optionally add missing reverse exits
    if bidirectional:
        for room in rooms.values():
            for direction, target_room in room["exits"].items():
                if not target_room:
                    continue
                opposite = OPPOSITE_DIRECTIONS.get(direction)
                if not opposite:
                    continue
                # if reverse link is missing, add it
                rev_exits = target_room["exits"]
                if rev_exits.get(opposite) is None:
                    rev_exits[opposite] = room


if __name__ == "__main__":
    # Simple test/demo loader
    import pprint

    region = build_region("forest")
    pprint.pprint(region)

"""
Next steps you might consider:

Hooking this into your main game loop or world loader.

Writing unit tests to verify exit connectivity and missing-room warnings.

Adding hooks for npc_spawner.py or item_distributor.py right after connect_rooms().
"""