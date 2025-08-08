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
def prune_error_logs(log_dir=".", archive=False):
    import os
    import shutil
    import time

    if not os.path.exists(log_dir):
        return "Error log directory not found."

    files = [f for f in os.listdir(log_dir)
             if f.startswith("ERRORLOG_") and f.endswith((".log", ".txt"))]
    if not files:
        return "No error logs to prune."

    skipped = []
    pruned = 0

    for f in files:
        full_path = os.path.join(log_dir, f)
        try:
            if archive:
                archive_dir = os.path.join(log_dir, "archive")
                os.makedirs(archive_dir, exist_ok=True)
                shutil.move(full_path, os.path.join(archive_dir, f))
            else:
                os.remove(full_path)
            pruned += 1
        except PermissionError:
            time.sleep(0.5)  # Wait half a second and try again
            try:
                if archive:
                    archive_dir = os.path.join(log_dir, "archive")
                    os.makedirs(archive_dir, exist_ok=True)
                    shutil.move(full_path, os.path.join(archive_dir, f))
                else:
                    os.remove(full_path)
                pruned += 1
            except PermissionError:
                skipped.append(f)

    result = f"{'Archived' if archive else 'Deleted'} {pruned} error logs."
    if skipped:
        result += f" Skipped {len(skipped)} locked file(s): {', '.join(skipped)}"
    return result




def cleanup_old_logs():
    now = datetime.now()
    for filename in os.listdir(LOG_DIR):
        if filename.startswith("ERRORLOG_") and filename.endswith((".log", ".txt")):
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

