import curses #localmud v0.1.0 started 7/12/2025

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
    stdscr.addstr(3, 2, room["description"])

    if room["items"]:
        stdscr.addstr(5, 2, f"You see: {', '.join(room['items'])}")

    stdscr.addstr(7, 2, f"Inventory: {', '.join(player['inventory']) or 'Empty'}")
    stdscr.addstr(9, 2, message)
    stdscr.addstr(11, 2, "> ")
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
        look_text = room.get("look_description", "You look around, but see nothing new.")
        return look_text


    elif tokens[0] == "inventory":
        return f"Inventory: {', '.join(player['inventory']) or 'Empty'}"

    elif tokens[0] in ["quit", "exit"]:
        return "quit"

    else:
        return "Unknown command."

def main(stdscr):
    message = ""
    while True:
        draw_ui(stdscr, message)
        curses.echo()
        command = stdscr.getstr(11, 4, 60).decode("utf-8").strip()
        curses.noecho()
        result = handle_command(command)
        if result == "quit":
            break
        message = result

curses.wrapper(main)
