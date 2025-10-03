# parser.py
"""
LocalMUD — Command Parser

Handles all player input and command logic. Supports aliases, dirty word tracking,
and command routing to appropriate game functions.

Author: Alex
"""

from game.character import CORE_STATS
from config    import VERSION, DEV_NOTE, DIRTY_WORDS, DIRECTION_ALIASES
from datetime  import datetime
import traceback
import random
import curses
from utils.log_manager import log_room_error, verify_room_links, prune_error_logs
from utils.helpers import normalize_room_id


COMMANDS = [
    "examine", "talk to", "go",
    "look", "inventory", "take", "get", "use",
    "about", "title", "drop", "character", "help",
    "clear", "motd", "quit", "exit"
]


def run_curses_game(game_func):
    def wrapper(stdscr):
        curses.curs_set(0)
        stdscr.clear()
        game_func(stdscr)
        stdscr.refresh()
    curses.wrapper(wrapper)
    return ""  # Return empty string to avoid printing extra text

def handle_command(
    command,
    game_state,
    player,
    rooms,
    items,
    current_motd,
    message_log,
    npcs
):
    """
    Interpret a player's text command and return either:
    - a string
    - a list of strings
    - special tokens like "quit" or "confirm_title"
    """

    room_id = normalize_room_id(game_state["current_room"])
    room = rooms.get(room_id)

    if not room:
        return [f"ERROR: Room '{room_id}' not found. You may be stuck in the void."]

    tokens = command.lower().split()

    # Dirty‐word filter
    for w in tokens:
        if w in DIRTY_WORDS:
            player["curse_count"] = player.get("curse_count", 0) + 1
            return [
                "Let's try to keep it clean.",
                "*The narrator sighs and adjusts your character sheet.*"
            ]

    if not tokens:
        return "No command entered."

    # EXAMINE
    if tokens[0] in ("examine", "x"):
        target = " ".join(tokens[1:])
        # inventory first
        for inv in player["inventory"]:
            if inv.lower() == target:
                data = items.get(inv, {})
                return data.get("examine_text",
                                f"You examine the {inv}, but find nothing unusual.")
        # room examine targets
        desc = room.get("examine_targets", {}).get(target)
        if desc:
            return desc
        return "You see nothing special."

    # -----------------------------------------------------------------------------
    # TALK TO branch:
    if tokens[0] == "talk" and len(tokens) > 2 and tokens[1] == "to":
        # 1) split off any "about <topic>"
        parts = tokens[2:]
        if "about" in parts:
            idx = parts.index("about")
            target_tokens = parts[:idx]
            topic = " ".join(parts[idx+1:]).lower()
        else:
            target_tokens = parts
            topic = None

        target_name = " ".join(target_tokens).lower()
        room_key    = game_state["current_room"]

        message_log.append(f"[DEBUG] room_key: {room_key}, looking for '{target_name}', topic={topic}")

        # 2) find NPCs in this room
        present = npcs.get(room_key, [])
        if not present:
            message_log.append(f"[DEBUG] no NPCs in this room")
            return f"You don't see anyone named '{target_name}' here."

        for npc in present:
            npc_key   = npc["id"]
            npc_name  = npc.get("name", "<unnamed>").lower()
            aliases   = [a.lower() for a in npc.get("aliases", [])]

            message_log.append(f"[DEBUG] checking NPC: {npc_name}, aliases={aliases}")

            if target_name in [npc_name] + aliases:
                # 3) triggers
                try:
                    for trig in npc.get("triggers", []):
                        # you can expand this to eval arbitrary conditions
                        if trig["condition"] == "player_xp > 5" and player.get("xp", 0) > 5:
                            return trig["response"]

                    # 4) topic-based responses
                    responses = npc.get("responses", {})
                    # exact match, then fallback on None
                    replies  = responses.get(topic) or responses.get(None)

                    if replies:
                        return random.choice(replies)

                    # 5) final fallback: greeting
                    return npc.get("greeting", f"{npc['name']} has nothing to say.")

                except Exception as e:
                    message_log.append(f"[ERROR] exception in talk-to: {e}")
                    for line in traceback.format_exc().splitlines():
                        message_log.append(f"  {line}")
                    return "Something went wrong while talking."

        # no match found
        return f"You don't see anyone named '{target_name}' here."
    # -----------------------------------------------------------------------------

    # MOVE: GO [direction]
    if tokens[0] == "go":
        if len(tokens) < 2:
            return "Go where?"
        dir_input = tokens[1]
        direction = DIRECTION_ALIASES.get(dir_input)
        if not direction or direction not in room.get("exits", {}):
            return ["You can't go that way."]
        new_room = room["exits"][direction]

        # room exists?
        if new_room not in rooms:
            log_room_error(game_state["current_room"], new_room, direction, rooms)
            return [
                f"You step toward the {direction}, but the threshold dissolves—"
                " no room lies that way."
            ]

        # door locked?
        for trig in rooms[new_room].get("triggers", []):
            if trig.get("condition") == "requires_item":
                req = trig["item"]
                if req not in player["inventory"]:
                    return [f"The way is locked. You need the {req}."]

        # update visited & xp (tolerant to missing "visited" key)
        first = not rooms[new_room].get("visited", False)
        rooms[new_room]["visited"] = True
        if first:
            player["xp"] = player.get("xp", 0) + 1


        # update location
        game_state["current_room"] = new_room
        player["location"] = new_room

        msg = []
        if direction in ("up", "down"):
            msg.append(f"You move {direction.upper()}. - {rooms[new_room]['name']}")
        else:
            msg.append(f"You go {direction}. - {rooms[new_room]['name']}")
        if first:
            msg.append(f"You gain 1 XP for discovering {rooms[new_room]['name']}.")
        if first or player.get("verbose_travel"):
            msg.append(rooms[new_room]["look_description"])
        return msg

    # DIRECTION SHORTCUTS (n, s, e, w, u, d)
    if tokens[0] in DIRECTION_ALIASES:
        return handle_command(f"go {tokens[0]}", game_state, player,
                              rooms, items, current_motd, message_log, npcs)

    # LOOK / L
    if tokens[0] in ("look", "l"):
        out = []
        # description
        out.append(room.get("look_description", room["description"]))
        # items
        items_here = room.get("items", [])
        out.append(
            items_here and "Items here: " + ", ".join(items_here)
            or "There are no items here."
        )
        # NPCs (Depricated)
        present_npcs = npcs.get(game_state["current_room"], [])
        if present_npcs:
            npc_names = [npc["name"] for npc in present_npcs]
            out.append("You see here: " + ", ".join(npc_names))

        # Monsters
        from game.spawn import get_room_instances
        monster_instances = get_room_instances(game_state["current_room"])
        if monster_instances:
            monster_names = [m["name"] for m in monster_instances]
            out.append("You see: " + ", ".join(monster_names))


        # exits
        exits = room.get("exits", {})
        if exits:
            exit_names = [DIRECTION_ALIASES[d] for d in exits]
            out.append("Exits: " + ", ".join(exit_names))
        return out

    # INVENTORY
    if tokens[0] in ("inventory", "i"):
        inv = player.get("inventory", [])
        if not inv:
            return "Your inventory is empty."
        lines = ["You are carrying:"]
        for it in inv:
            desc = items.get(it, {}).get("description", "")
            lines.append(f"- {it}: {desc}")
        return lines

    # TAKE / GET
    if tokens[0] in ("take", "get"):
        want = " ".join(tokens[1:])
        for it in list(room.get("items", [])):
            if it.lower() == want:
                player["inventory"].append(it)
                room["items"].remove(it)
                return f"You take the {it}."
        return "That item isn't here."

    # USE
    if tokens[0] == "use":
        want = " ".join(tokens[1:])
        for inv in player.get("inventory", []):
            if inv.lower() == want:
                data = items.get(inv, {})
                use_data = data.get("use")
                if use_data:
                    item_room = normalize_room_id(use_data.get("location"))
                    current_room = normalize_room_id(game_state["current_room"])

                    if item_room == current_room:
                        effect  = use_data.get("effect")
                        message = use_data.get("message", f"You use the {inv}.")
                        if effect == "win":
                            return message
                        if effect == "unlock":
                            rooms[game_state["current_room"]].setdefault("flags", {})["door_unlocked"] = True
                            return message
                    return f"You can't use the {inv} here."
                return f"You use the {inv}, but nothing happens."
        return "You don't have that item."

    # ABOUT
    if tokens[0] == "about":
        return [f"LocalMUD {VERSION}", DEV_NOTE]

    # DIR
    if tokens[0] == "dir":
        return [f"Bro, this isn't DOS. Sorry."]

    # TITLE
    if tokens[0] == "title":
        return "confirm_title"

    # DROP [ITEM]
    if tokens[0] == "drop" and len(tokens) > 1:
        item_name = " ".join(tokens[1:])
        room = rooms[player["location"]]

        if item_name not in player["inventory"]:
            return f"You don't have '{item_name}' to drop."

        player["inventory"].remove(item_name)
        room.setdefault("items", []).append(item_name)

        return f"You dropped '{item_name}'. It now lies here."


    # CHARACTER SHEET
    if tokens[0] in ("character", "c"):
        out = []
        out.append(f"Name: {player.get('name', 'Unknown')}")
        out.append(f"Background: {player.get('background', 'None')}")
        xp = player.get("xp", 0)
        out.append(f"XP: {xp}")
        
        gold = player.get("gold", 0)
        out.append(f"Gold: {gold}")  # 💰 Add this line

        out.append("Stats:")
        stats     = player.get("stats", {})
        modifiers = player.get("modifiers", {})
        for stat in CORE_STATS:
            val = stats.get(stat, 0)
            mod = modifiers.get(stat, 0)
            out.append(f"  {stat}: {val} ({mod:+d})")
        
        curses = player.get("curse_count", 0)
        if curses:
            out.append(f"Curses: {curses}")
        
        return out

    # HELP
    if tokens[0] == "help":
        if len(tokens) == 1:
            lines = ["Available commands:"] + [f"- {c}" for c in COMMANDS]
            lines.append("Type HELP [COMMAND] for details.")
            return lines
        cmd = tokens[1]
        if cmd == "go":
            return [
                "GO [direction] — Move to another room (N/S/E/W/U/D).",
                "First discovery grants XP; revisit uses look_description only if verbose."
            ]
        if cmd == "look":
            return [
                "LOOK — Show this room's description, items, and exits.",
                "L is a shortcut."
            ]
        return [f"No detailed help for '{cmd}'."]

    # DEBUG COMMANDS
    if tokens[0].lower() == "debug":
        if not player.get("debug_mode", False):
            return "Debug mode is not enabled."

        if len(tokens) < 2:
            lines = [
                "Specify a debug action. Example: DEBUG BLACKJACK",
                "Available commands:",
                " - BLACKJACK",
                " - DICEHIGHLOW",
                " - SLOTS",
                " - GIVEGOLD",
                " - HEAL",
                " - PRUNELOGS",
            ]
            return lines

        action = tokens[1].lower()

        if action == "blackjack":
            import minigames.blackjack as blackjack
            return run_curses_game(lambda stdscr: blackjack.play(player, stdscr))

        elif action == "slots":
            import minigames.slots as slots
            return run_curses_game(lambda stdscr: slots.play_slots(stdscr, player))

        elif action == "dicehighlow":
            import minigames.dicehighlow as dicehighlow
            return run_curses_game(lambda stdscr: dicehighlow.play(player, stdscr))
            
        elif action == "heal":
            player["hp"] = player.get("max_hp", 6)
            return f"Player healed to full HP ({player['hp']}/{player['max_hp']})."
            
        elif action == "givegold":
            if len(tokens) < 3 or not tokens[2].isdigit():
                return "Usage: DEBUG GIVEGOLD <amount>"
            amount = int(tokens[2])
            player["gold"] = player.get("gold", 0) + amount
            return f"Gave {amount} gold. Player now has {player['gold']} gold."

        elif action == "teleport":
            # Usage: DEBUG TELEPORT <room_id>
            if len(tokens) < 3:
                return "Usage: DEBUG TELEPORT <room_id>"

            # Join the rest of the tokens to allow room ids with punctuation or underscores
            target_room = " ".join(tokens[2:])

            # Validate rooms mapping is available
            if "rooms" not in locals() and "rooms" not in globals():
                return "Teleport failed: room data (rooms) is not available in this context."

            # Prefer local then global
            _rooms = locals().get("rooms") or globals().get("rooms")

            if target_room not in _rooms:
                # Offer a short helpful hint listing similarly named rooms
                similar = [r for r in _rooms.keys() if target_room.lower() in r.lower()]
                hint = f" Did you mean: {', '.join(similar)}?" if similar else ""
                return f"Teleport failed: unknown room id '{target_room}'.{hint}"

            # Apply the teleport: prefer game_state current room if available, else player location
            if "game_state" in locals() or "game_state" in globals():
                gs = locals().get("game_state") or globals().get("game_state")
                gs["current_room"] = target_room
            else:
                player["location"] = target_room

            # Optionally call spawn logic if provided (keeps dev workflow fast)
            # If you have a spawn helper like spawn_by_room in utils/monster_manager, call it.
            try:
                spawn_fn = None
                if "spawn_by_room" in globals():
                    spawn_fn = globals()["spawn_by_room"]
                elif "spawn_by_room" in locals():
                    spawn_fn = locals()["spawn_by_room"]
                else:
                    # try common import without failing if module missing
                    try:
                        from utils.monster_manager import spawn_by_room as spawn_fn  # type: ignore
                    except Exception:
                        spawn_fn = None
                if callable(spawn_fn):
                    spawn_fn(_rooms, target_room)
            except Exception:
                # Don't let spawn errors break debug teleport; swallow and continue
                pass

            # Return confirmation
            return f"Teleported to {target_room} ({_rooms[target_room].get('name','Unnamed room')})."


        elif action == "prunelogs":
            result = prune_error_logs()
            return f"[DEBUG] {result}"

        return f"Unknown debug action: {action}"

    # CLEAR
    if tokens[0] == "clear":
        message_log.clear()
        return "Screen cleared."
        
    # CLS
    if tokens[0] == "cls":
        message_log.clear()
        return "Fine, I’ll clear the screen. But just so you know, I’m judging you."

    # MOTD
    if tokens[0] == "motd":
        return f"MOTD: {current_motd}"

    # QUIT / EXIT
    if tokens[0] in ("quit", "exit"):
        return "quit"

    # FALL-THROUGH
    return "Unknown command."
