import curses #localmud v0.2.0

# Define the rooms
rooms = {
    (0, 0): {
        "name": "Pedestal Chamber",
        "description": "A quiet chamber with a glowing orb resting on a pedestal.",
        "look_description": "Dust motes float in the air. The pedestal is carved with ancient symbols.",
        "items": ["Glowing Orb"],
        "exits": {"east": (1, 0)}
    },
    (1, 0): {
        "name": "Altar Room",
        "description": "An ancient altar stands in silence. Something feels incomplete.",
        "look_description": "The altar is cracked and worn. Faint traces of glowing runes shimmer beneath the dust.",
        "items": [],
        "exits": {"west": (0, 0)},
        "triggers": [
            {
                "condition": "has_item",
                "item": "Glowing Orb",
                "effect": "win"
            }
        ]
    }
}

# Player state
player = {
    "location": (0, 0),
    "inventory": []
}

def draw_ui(stdscr, message=""):
    stdscr.clear()
    curses.curs_set(1)

    room = rooms[player["location"]]
    stdscr.addstr(1, 2, f"Location: {room['name']}")

    # Base room description
    stdscr.addstr(3, 2, room["description"])

    # Inventory
    stdscr.addstr(5, 2, f"Inventory: {', '.join(player['inventory']) or 'Empty'}")

    # Message (e.g., from 'look' or other commands)
    if message:
        lines = message.split("\n")
        for i, line in enumerate(lines):
            stdscr.addstr(7 + i, 2, line)

    # Input prompt
    stdscr.addstr(7 + len(message.split("\n")) + 2, 2, "> ")
    stdscr.refresh()


def handle_command(command):
    room = rooms[player["location"]]
    tokens = command.lower().split()

    if not tokens:
        return "No command entered."

    if tokens[0] == "go":
        direction = tokens[1] if len(tokens) > 1 else ""
        if direction in room["exits"]:
            player["location"] = room["exits"][direction]
            return f"You move {direction}."
        else:
            return "You can't go that way."

    elif tokens[0] == "take":
        item = " ".join(tokens[1:])
        for room_item in room["items"]:
            if room_item.lower() == item.lower():
                player["inventory"].append(room_item)
                room["items"].remove(room_item)
                return f"You take the {room_item}."
        return "That item isn't here."

    elif tokens[0] == "use":
        item = " ".join(tokens[1:])
        if item in player["inventory"]:
            for trigger in room.get("triggers", []):
                if trigger["condition"] == "has_item" and trigger["item"].lower() == item.lower():
                    if trigger["effect"] == "win":
                        return "You place the orb on the altar. A warm light fills the room. You win!"
            return f"You use the {item}, but nothing happens."
        else:
            return "You don't have that item."

    elif tokens[0] == "look":
        look_parts = []

        # Base description
        look_text = room.get("look_description", room["description"])
        look_parts.append(look_text)

        # Items
        if room["items"]:
            look_parts.append("Items here: " + ", ".join(room["items"]))
        else:
            look_parts.append("There are no items here.")

        # Exits
        exit_texts = {
            "north": "a crumbling archway",
            "east": "a narrow passage",
            "west": "a heavy wooden door",
            "south": "a dark tunnel"
        }
        exits = room.get("exits", {})
        exit_descriptions = [exit_texts.get(dir, dir) for dir in exits]
        if exit_descriptions:
            look_parts.append("Exits: " + ", ".join(exit_descriptions))

        return "\n".join(look_parts)



    elif tokens[0] == "inventory":
        return f"Inventory: {', '.join(player['inventory']) or 'Empty'}"

    elif tokens[0] in ["quit", "exit"]:
        return "quit"

    else:
        return "Unknown command."

def main(stdscr):
    message = ""
    curses.curs_set(1)
    stdscr.nodelay(False)  # Make getch() blocking

    while True:
        stdscr.clear()

        # Get current terminal size
        height, width = stdscr.getmaxyx()

        # Minimum size check
        min_height, min_width = 15, 40
        if height < min_height or width < min_width:
            stdscr.addstr(0, 0, "Window too small. Please resize.")
            stdscr.refresh()
            continue

        # Draw UI
        room = rooms[player["location"]]
        stdscr.addstr(1, 2, f"Location: {room['name']}")
        stdscr.addstr(3, 2, room["description"])
        stdscr.addstr(5, 2, f"Inventory: {', '.join(player['inventory']) or 'Empty'}")

        # Display message (e.g., from 'look')
        if message:
            lines = message.split("\n")
            for i, line in enumerate(lines):
                if 7 + i < height - 3:
                    stdscr.addstr(7 + i, 2, line)

        # Input prompt near bottom
        input_y = height - 2
        stdscr.addstr(input_y, 2, "> ")
        stdscr.refresh()

        # Get user input
        curses.echo()
        try:
            command = stdscr.getstr(input_y, 4, width - 6).decode("utf-8").strip()
        except Exception:
            command = ""
        curses.noecho()

        # Handle command
        if command.lower() in ["quit", "exit"]:
            break
        result = handle_command(command)
        message = result


curses.wrapper(main)
