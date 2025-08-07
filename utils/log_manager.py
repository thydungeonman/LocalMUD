#log_manager.py

import os
import logging
from datetime import datetime, timedelta

LOG_RETENTION_DAYS = 7
LOG_DIR = "."  # Change to "logs/" if you move logs later

# Setup timestamped log file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"ERRORLOG_{timestamp}.txt"
logging.basicConfig(
    filename=log_filename,
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def cleanup_old_logs():
    now = datetime.now()
    for filename in os.listdir(LOG_DIR):
        if filename.startswith("ERRORLOG_") and filename.endswith(".txt"):
            filepath = os.path.join(LOG_DIR, filename)
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if now - file_time > timedelta(days=LOG_RETENTION_DAYS):
                os.remove(filepath)

def log_room_error(current_room, attempted_coords, attempted_direction, rooms):
    message = (
        f"\n--- Room Connection Error ---\n"
        f"Source Room: {current_room} ({rooms[current_room]['name']})\n"
        f"Attempted Direction: {attempted_direction}\n"
        f"Target Coordinates: {attempted_coords}\n"
        f"Cause: Destination room does not exist.\n"
        f"------------------------------\n"
    )
    logging.error(message)

def verify_room_links(rooms):
    broken = []
    for room_key, room_data in rooms.items():
        for direction, target in room_data.get("exits", {}).items():
            if target not in rooms:
                broken.append(
                    f"Broken exit from {room_data['name']} ({room_key}) going "
                    f"{direction} to {target}"
                )
    if broken:
        logging.error("=== Room Link Diagnostics ===")
        for line in broken:
            logging.error(line)

