import curses #localmud v0.4.0
VERSION = "v0.4.0 — A Hero Arises"
DEV_NOTE = "This build adds hero stats and cleans up with UI."

DIRECTION_ALIASES = {
    "n": "north",
    "north": "north",
    "s": "south",
    "south": "south",
    "e": "east",
    "east": "east",
    "w": "west",
    "west": "west"
}

COMMANDS = [
    "look",
    "go [direction]",
    "take [item]",
    "use [item]",
    "inventory",
    "examine [item or object]",
    "about",
    "motd",
    "clear",
    "help",
    "quit"
]

# Define the rooms
rooms = {
    (0, 0, 0, "chapel"): {
        "name": "Pedestal Chamber",
        "description": "A quiet chamber with a glowing orb resting on a pedestal.",
        "visited": False,
        "look_description": "Dust motes float in the air. The pedestal is carved with ancient symbols.",
        "items": ["Glowing Orb"],
        "exits": {"east": (1, 0, 0, "chapel")},
        "examine_targets": {
            "pedestal": "The pedestal is carved from obsidian. Symbols etched into its surface seem to shift when you stare too long.",
            "symbols": "The symbols resemble constellations, but none you recognize. One looks like a ladle."
        }
    },
    (1, 0, 0, "chapel"): {
        "name": "Altar Room",
        "description": "An ancient altar stands in silence. Something feels incomplete.",
        "visited": False,
        "look_description": "The altar is cracked and worn. Faint traces of glowing runes shimmer beneath the dust.",
        "items": [],
        "exits": {"west": (0, 0, 0, "chapel")},
        "examine_targets": {
            "altar": "The altar bears a shallow indentation, perfectly orb-shaped.",
            "runes": "The runes pulse faintly. One resembles the symbol on the pedestal."
        },
        "triggers": [
            {
                "condition": "has_item",
                "item": "Glowing Orb",
                "effect": "win"
            }
        ]
    }
}


# Define the items
items = {
    "Glowing Orb": {
        "description": "A mysterious orb that pulses with faint light.",
        "examine_text": "The orb is warm to the touch. Symbols swirl inside, forming patterns that resemble constellations.",
        "use": {
            "location": (1, 0, 0, "chapel"),
            "effect": "win",
            "message": "You place the orb on the altar. A warm light fills the room. You win!"
        }
    },
    "Rusty Key": {
        "description": "An old iron key. It looks like it could unlock something.",
        "examine_text": "The key is engraved with the number 7. Its teeth are worn but intact.",
        "use": {
            "location": (2, 0, 0, "chapel"),
            "effect": "unlock",
            "target": "door",
            "message": "You unlock the heavy door with the rusty key."
        }
    }
}


game_state = {
    "current_room": (0, 0, 0, "chapel")
}

# Player state
player = {
    "name": "Hero",
    "location": (0, 0, 0, "chapel"),
    "inventory": [],
    "hp": 6,
    "max_hp": 6,
    "ac": 7,  # Armor Class (descending) lower is better
    "str": 13, #Melee attack bonuys, Carry Weight
    "dex": 9, #AC Bonus, Ranged Attack Bonus
    "con": 12, #HP Bonus Per Level
    "int": 10, #Spell Learning
    "wis": 8, #Saving Throws, Divine Magic
    "cha": 11, #npc reactions, hirelings
    "level": 1, 
    "xp": 0,
    "status": [],
    "flags": {}
}


import random

def get_motd():
    try:
        with open("motd.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines)
    except FileNotFoundError:
        return "Welcome to LocalMUD."

CURRENT_MOTD = get_motd()

def show_intro(stdscr):
    stdscr.clear()
    try:
        with open("intro.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["Welcome to LocalMUD", "Press Enter to begin..."]

    height, width = stdscr.getmaxyx()
    for i, line in enumerate(lines):
        if i < height - 2:
            stdscr.addstr(i + 2, 2, line.strip()[:width - 4])
    stdscr.refresh()
    
    motd = get_motd()
    if motd:
        stdscr.addstr(height - 4, 2, f"MOTD: {motd[:width - 6]}")

    # Wait for Enter
    while True:
        key = stdscr.getch()
        if key in [10, 13]:  # Enter key
            break


def draw_ui(stdscr, message=""):
    stdscr.clear()
    curses.curs_set(1)

    room = rooms[game_state["current_room"]]
    stdscr.addstr(1, 2, f"Location: {room['name']}")

    # Base room description
    stdscr.addstr(3, 2, room["description"])

    # Inventory (Now removed from the UI)
    #stdscr.addstr(5, 2, f"Inventory: {', '.join(player['inventory']) or 'Empty'}")

    # Message (e.g., from 'look' or other commands)
    if message:
        lines = message.split("\n")
        for i, line in enumerate(lines):
            stdscr.addstr(7 + i, 2, line)

    # Input prompt
    stdscr.addstr(7 + len(message.split("\n")) + 2, 2, "> ")
    stdscr.refresh()

#PARSER ====================
def handle_command(command, game_state):
    room = rooms[game_state["current_room"]]
    tokens = command.lower().split()

    if not tokens:
        return "No command entered."

    elif tokens[0] == "go":
        if len(tokens) > 1:
            dir_input = tokens[1].lower()
            direction = DIRECTION_ALIASES.get(dir_input)
            if direction and direction in room["exits"]:
                new_room = room["exits"][direction]
                game_state["current_room"] = new_room
                player["location"] = new_room
                rooms[new_room]["visited"] = True  # Mark room as visited
                return [f"You go {direction}."]
            else:
                return [f"You can't go that way."]
        else:
            return ["Go where?"]
        
    elif tokens[0] == "examine":
        target = " ".join(tokens[1:]).lower()

        # Check inventory first
        for item in player["inventory"]:
            if item.lower() == target:
                item_data = items.get(item)
                if item_data:
                    return item_data.get("examine_text", f"You examine the {item}, but find nothing unusual.")

        # Check room examine targets
        examine_targets = room.get("examine_targets", {})
        if target in examine_targets:
            return examine_targets[target]

        return "You see nothing special."


    elif tokens[0] in DIRECTION_ALIASES:
        direction = DIRECTION_ALIASES[tokens[0]]
        if direction in room["exits"]:
            new_room = room["exits"][direction]
            game_state["current_room"] = new_room
            player["location"] = new_room
            rooms[new_room]["visited"] = True
            return [f"You go {direction}."]
        else:
            return [f"You can't go that way."]
            
    elif tokens[0] == "about":
        return [
            f"LocalMUD {VERSION}",
            DEV_NOTE
        ]
    
    elif tokens[0] == "help":
        help_lines = ["Available commands:"]
        for cmd in COMMANDS:
            help_lines.append(f"- {cmd}")
        return help_lines

     
    elif tokens[0] == "clear":
        message_log.clear()
        return ["Screen cleared."]

    elif tokens[0] == "motd":
        return [f"MOTD: {CURRENT_MOTD}"]

    elif tokens[0] == "take":
        item = " ".join(tokens[1:])
        for room_item in room["items"]:
            if room_item.lower() == item.lower():
                player["inventory"].append(room_item)
                room["items"].remove(room_item)
                return f"You take the {room_item}."
        return "That item isn't here."
       
    elif tokens[0] == "use":
        item_name = " ".join(tokens[1:])
        for inv_item in player["inventory"]:
            if inv_item.lower() == item_name.lower():
                item_data = items.get(inv_item)
                if item_data and "use" in item_data:
                    use_data = item_data["use"]
                    if use_data.get("location") == player["location"]:
                        effect = use_data.get("effect")
                        message = use_data.get("message", f"You use the {inv_item}.")
                        if effect == "win":
                            return message
                        elif effect == "unlock":
                            # Example: set a flag or modify room state
                            rooms[player["location"]]["flags"] = {"door_unlocked": True}
                            return message
                    else:
                        return f"You can't use the {inv_item} here."
                return f"You use the {inv_item}, but nothing happens."
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
            "north": "an exit north",
            "east": "an exit east",
            "west": "an exit west",
            "south": "an exit south"
        }
        exits = room.get("exits", {})
        exit_descriptions = [exit_texts.get(dir, dir) for dir in exits]
        if exit_descriptions:
            look_parts.append("Exits: " + ", ".join(exit_descriptions))

        return look_parts




    elif tokens[0] == "inventory":
        if not player["inventory"]:
            return "Your inventory is empty."
        lines = ["You are carrying:"]
        for item in player["inventory"]:
            desc = items.get(item, {}).get("description", "")
            lines.append(f"- {item}: {desc}")
        return "\n".join(lines)


    elif tokens[0] in ["quit", "exit"]:
        return "quit"

    else:
        return "Unknown command."

message_log = []  # Global or top-level list to store output history

def main(stdscr):
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

        # ┌──── Static Top Bar ────┐
        title = "LocalMUD v0.4.0"
        hp = 10  # You can make this dynamic later
        orb_status = "Carried" if "Glowing Orb" in player["inventory"] else "Missing"
        top_bar = f"{title} — HP: {hp} | Orb: {orb_status}"
        stdscr.addstr(0, 2, top_bar[:width - 4])

        # ├──── Room Info ────┤
        room = rooms[game_state["current_room"]]
        stdscr.addstr(1, 2, f"Location: {room['name']}")
        stdscr.addstr(2, 2, room["description"])

        # ├──── Message Log ────┤

        # Calculate how many lines can fit with single-line spacing
        max_visible_lines = height - 7

        # Get the last N messages that fit
        visible_messages = message_log[-max_visible_lines:]

        # Display them with tighter spacing
        for i, line in enumerate(visible_messages):
            line_y = 4 + i  # Starts one line lower, uses single spacing
            if line_y < height - 3:
                stdscr.addstr(line_y, 2, line[:width - 4])


                
        # └──── Input Prompt ────┘
        input_y = height - 2
        stdscr.addstr(input_y - 1, 2, " ")
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
        if command:
            message_log.append(f"> {command}")

        result = handle_command(command, game_state)
        if isinstance(result, list):
            message_log.extend(result)
        elif isinstance(result, str) and result:
            message_log.append(result)

        # Add a blank line after each response
        message_log.append("")




def launch(stdscr):
    show_intro(stdscr)
    main(stdscr)

curses.wrapper(launch)

