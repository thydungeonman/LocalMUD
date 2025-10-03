# game/spawn.py
import uuid
import random
import time
from game.monsters import MONSTER_DEFS

# Runtime registries
INSTANCES = {}         # instance_id -> instance dict
ROOM_INDEX = {}        # room_key -> set of instance_ids

def create_instance(template_key, room_key):
    """Create a runtime monster instance from a template and place it in a room."""
    template = MONSTER_DEFS.get(template_key)
    if not template:
        return None

    instance_id = f"{template_key}:{uuid.uuid4().hex[:6]}"
    hp = template.get("hp", random.randint(1, 6))  # fallback if not defined
    stats = template.get("base_stats", {})
    instance = {
        "id": instance_id,
        "template": template_key,
        "name": template["name"],
        "hp": hp,
        "max_hp": hp,
        "ac": template.get("ac", 10),
        "stats": stats,
        "room": room_key,
        "hostile": template.get("hostile", True),
        "created_at": time.time(),
        "description": template.get("description", ""),
        "xp": template.get("xp", 0),
        "loot": template.get("loot", []),
    }

    INSTANCES[instance_id] = instance
    ROOM_INDEX.setdefault(room_key, set()).add(instance_id)
    return instance

def get_room_instances(room_key):
    """Return a list of instance dicts currently in the room."""
    ids = ROOM_INDEX.get(room_key, set())
    return [INSTANCES[i] for i in ids if i in INSTANCES]

def remove_instance(instance_id):
    """Remove a monster instance from the world."""
    inst = INSTANCES.pop(instance_id, None)
    if inst:
        room_key = inst["room"]
        ROOM_INDEX.get(room_key, set()).discard(instance_id)

def init_region_spawns(region_data):
    """Spawn initial monsters based on room spawn metadata."""
    for room_key, room in region_data.items():
        for spawn in room.get("spawns", []):
            if spawn.get("type") != "monster":
                continue
            key = spawn.get("key")
            count = spawn.get("initial_count", 0)
            for _ in range(count):
                create_instance(key, room_key)
