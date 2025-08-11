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


# Future utility functions can go here
# e.g. format_item_name(), wrap_text(), etc.
