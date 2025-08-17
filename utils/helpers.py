# utils/helpers.py

def normalize_room_id(room_id):
    """
    Converts a room_id to a string key for lookup.
    Supports both tuple-based and string-based formats.

    Examples:
        (0, 0, 0, "chapel") → "0_0_0_chapel"
        "fellmore_cliffs_2_2" → "fellmore_cliffs_2_2"
    """
    if isinstance(room_id, tuple):
        return "_".join(map(str, room_id))
    return room_id


def convert_room_dict_keys(room_dict):
    """
    Converts all keys in a room dictionary to normalized string format.
    Returns a new dictionary with updated keys.
    """
    return {
        normalize_room_id(key): value
        for key, value in room_dict.items()
    }


def get_room(room_dict, key):
    """
    Safely retrieves a room from the dictionary using either format.
    """
    normalized_key = normalize_room_id(key)
    return room_dict.get(normalized_key)


# Optional: reverse conversion if needed later
def parse_room_id(room_id_str):
    """
    Converts a string room ID back to a tuple, if applicable.
    Example: "0_0_0_chapel" → (0, 0, 0, "chapel")
    """
    parts = room_id_str.split("_")
    if len(parts) == 4:
        try:
            return (int(parts[0]), int(parts[1]), int(parts[2]), parts[3])
        except ValueError:
            pass
    return room_id_str  # fallback
