# parser.py
"""
LocalMUD — Command Parser

Handles all player input and command logic. Supports aliases, dirty word tracking,
and command routing to appropriate game functions.

Typical usage:
- Called during main game loop to interpret input
- Interacts with player, rooms, and items modules

Author: Alex

Dev Notes:
- Keep command logic modular—each command should be easy to isolate and test.
- Aliases should be intuitive and documented.
- Consider adding command history or auto-complete in future UI upgrades.
"""

from character import CORE_STATS, get_modifier, roll_stats
from config import VERSION, DEV_NOTE
from datetime import datetime

def log_room_error(current_room, attempted_coords, attempted_direction, rooms):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("ERRORLOG.txt", "a") as log_file:
        log_file.write(f"\n--- Room Connection Error ---\n")
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Source Room: {current_room} ({rooms[current_room]['name']})\n")
        log_file.write(f"Attempted Direction: {attempted_direction}\n")
        log_file.write(f"Target Coordinates: {attempted_coords}\n")
        log_file.write(f"Cause: Destination room does not exist.\n")
        log_file.write(f"------------------------------\n")


DIRECTION_ALIASES = {
    "n": "north",
    "north": "north",
    "s": "south",
    "south": "south",
    "e": "east",
    "east": "east",
    "w": "west",
    "west": "west",
    "u": "up",
    "up": "up",
    "d": "down",
    "down": "down"
}

COMMANDS = [
    "look",
    "go [direction]",
    "take [item] / get [item]",
    "use [item]",
    "inventory (or i)",
    "examine [item or object] (or x)",
    "character (or c)",
    "about",
    "motd",
    "clear",
    "help",
    "title",
    "quit"
]

DIRTY_WORDS = ["shit", "fuck", "ass", "bitch", "cunt", "arse"]

def verify_room_links(rooms):
    broken_links = []

    for room_key, room_data in rooms.items():
        for direction, target_room in room_data.get("exits", {}).items():
            if target_room not in rooms:
                broken_links.append(
                    f"Broken exit from {room_data['name']} ({room_key}) going {direction} to {target_room}"
                )

    if broken_links:
        with open("ERRORLOG.txt", "a") as log_file:
            log_file.write("=== Room Link Diagnostics ===\n")
            for line in broken_links:
                log_file.write(line + "\n")
            log_file.write("\n")



def handle_command(raw, game_state, player, rooms, items, current_motd, message_log):

    output = []
    room = rooms[game_state["current_room"]]

    tokens = raw.lower().split()

    # Dirty word filter
    for word in tokens:
        if word in DIRTY_WORDS:
            player["curse_count"] += 1
            return [
                "Let's try to keep it clean.",
                "*The narrator sighs and adjusts your character sheet.*"
            ]

    if not tokens:
        return "No command entered."

    elif tokens[0] == "go":
        if len(tokens) > 1:
            dir_input = tokens[1].lower()
            direction = DIRECTION_ALIASES.get(dir_input)

            if direction and direction in room["exits"]:
                new_room = room["exits"][direction]

                # 🚨 Check if the destination room exists
                if new_room not in rooms:
                    log_room_error(game_state["current_room"], new_room, direction, rooms)
                    return [f"You step toward the {direction}, but the threshold dissolves—no room lies that way."]

                # 🔐 Check for required items
                triggers = rooms[new_room].get("triggers", [])
                for trigger in triggers:
                    if trigger.get("condition") == "requires_item":
                        required_item = trigger["item"]
                        if required_item not in player["inventory"]:
                            return [f"The way to the {rooms[new_room]['name']} is locked. You need the {required_item}."]

                # Check if this is the first visit
                is_first_visit = not rooms[new_room]["visited"]
                rooms[new_room]["visited"] = True

                # Compose movement message
                if direction in ["up", "down"]:
                    message = [f"You move {direction.upper()}. - {rooms[new_room]['name']}"]
                else:
                    message = [f"You go {direction}. - {rooms[new_room]['name']}"]

                # Award XP for first-time discovery
                if is_first_visit:
                    player["xp"] += 1
                    message.append(f"You gain 1 XP for discovering {rooms[new_room]['name']}.")

                # Show room description if first visit OR verbose mode is enabled
                if is_first_visit or player.get("verbose_travel"):
                    message.append(rooms[new_room]["look_description"])

                # 🗺️ Update game state
                game_state["current_room"] = new_room
                player["location"] = new_room

                return message
            else:
                return ["You can't go that way."]
        else:
            return ["Go where?"]

        
    elif tokens[0] in ['examine', 'x']:
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


    # Handle the shortcut keys for the GO command
    elif tokens[0] in DIRECTION_ALIASES:
        direction = DIRECTION_ALIASES[tokens[0]]
        if direction in room["exits"]:
            new_room = room["exits"][direction]

            # 🚨 Check if destination room exists
            if new_room not in rooms:
                log_room_error(game_state["current_room"], new_room, direction, rooms)
                return [f"You step toward the {direction}, but reality falters... No room exists there."]

            # 🔐 Check for required items
            triggers = rooms[new_room].get("triggers", [])
            for trigger in triggers:
                if trigger.get("condition") == "requires_item":
                    required_item = trigger["item"]
                    if required_item not in player["inventory"]:
                        return [f"The way to the {rooms[new_room]['name']} is locked. You need the {required_item}."]

            # ✅ Check for first visit
            is_first_visit = not rooms[new_room]["visited"]
            rooms[new_room]["visited"] = True

            # 🧠 Award XP
            if is_first_visit:
                player["xp"] += 1

            # 🗺️ Update game state
            game_state["current_room"] = new_room
            player["location"] = new_room

            # 📝 Compose movement message
            if direction in ["up", "down"]:
                message = [f"You move {direction.upper()}. - {rooms[new_room]['name']}"]
            else:
                message = [f"You go {direction}. - {rooms[new_room]['name']}"]

            if is_first_visit:
                message.append(f"You gain 1 XP for discovering {rooms[new_room]['name']}.")
            if is_first_visit or player.get("verbose_travel"):
                message.append(rooms[new_room]["look_description"])

            return message
        else:
            return ["You can't go that way."]

    #TALK TO [NPC]
    elif tokens[0] == "talk" and len(tokens) > 2 and tokens[1] == "to":
        target_name = " ".join(tokens[2:]).lower()
        current_npcs = npcs.get(game_state["current_room"], [])

        # Find matching NPC by id or name
        npc = next((n for n in current_npcs if target_name in [n["id"], n["name"].lower()]), None)

        if not npc:
            return [f"There is no one named '{tokens[2]}' here."]

        responses = []

        # Check triggers
        for trigger in npc.get("triggers", []):
            if trigger["condition"] == "player_xp > 5" and player["xp"] > 5:
                responses.append(trigger["response"])

        # If no triggers matched, use greeting or idle
        if not responses:
            responses.append(npc.get("greeting", f"{npc['name']} has nothing to say."))

        return responses

 
    elif tokens[0] == "about":
        return [
            f"LocalMUD {VERSION}",
            DEV_NOTE
        ]
    
    elif raw == "title":
        output.append("Are you sure you want to return to the title screen? [Y]es / [N]o")
        return "confirm_title"
    
    elif raw in ["character", "c"]:
        output.append(f"Name: {player.get('name', 'Unknown')}")
        output.append(f"Background: {player.get('background', 'None')}")

        # Show XP
        xp = player.get("xp", 0)
        output.append(f"XP: {xp}")

        stats = player.get("stats", {})
        modifiers = player.get("modifiers", {})

        output.append("Stats:")
        for stat in CORE_STATS:
            value = stats.get(stat, 0)
            mod = modifiers.get(stat, 0)
            output.append(f"  {stat}: {value} ({mod:+d})")

        # Show curse count if greater than 0
        curse_count = player.get("curse_count", 0)
        if curse_count > 0:
            output.append(f"Curses: {curse_count}")


    elif tokens[0] == "help":
        if len(tokens) == 1:
            help_lines = ["Available commands:"]
            for cmd in COMMANDS:
                help_lines.append(f"- {cmd}")
            help_lines.append("Type HELP [COMMAND] for more details.")
            return help_lines
        elif len(tokens) == 2:
            cmd = tokens[1].lower()
            if cmd == "look":
                return [
                    "LOOK — Displays the description of your current location.",
                    "If you're in verbose mode, this will always show the full room description.",
                    "Otherwise, it only shows the full description the first time you enter a room."
                ]
            elif cmd == "go":
                return [
                    "GO - Usage GO [Direction] (East/West/North/South) or (E/W/N/S).",
                    "Moves the player into a new room.",
                    "Discovering a room for the first time grants an XP bonus!"
                    
                ]
            else:
                return [f"No detailed help available for '{tokens[1]}'. Try HELP for a list of commands."]
        else:
            return ["Invalid HELP syntax. Use HELP or HELP [COMMAND]."]


     
    elif tokens[0] == "clear":
        message_log.clear()
        return ["Screen cleared."]

    elif tokens[0] == "motd":
        return [f"MOTD: {current_motd}"]

    elif tokens[0] in ["take", "get"]:
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

    elif tokens[0] in ["look", "l"]:
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




    elif tokens[0] in ["inventory", "i"]:
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
        
    return output