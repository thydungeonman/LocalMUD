# utils/helpers.py

def normalize_room_id(room_id):
    """
    Converts room identifiers into a consistent format.
    Accepts aliases like 'altar_room' or coordinate tuples like (1, 0, 0, 'chapel').
    Returns a string like 'chapel_1_0_0'.
    """
    if isinstance(room_id, tuple) and len(room_id) == 4:
        x, y, z, region = room_id
        return f"{region}_{x}_{y}_{z}"
    
    if isinstance(room_id, str):
        return room_id.strip().lower().replace(" ", "_")
    
    return str(room_id)


# Future utility functions can go here
# e.g. format_item_name(), wrap_text(), etc.
