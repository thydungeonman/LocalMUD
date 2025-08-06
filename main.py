import curses
import random

from game.rooms   import rooms
from game.npcs import NPC_DEFS
from game.items   import items
from game.player  import player as initial_player
from game.parser  import handle_command, verify_room_links
from config  import get_motd, VERSION, DEV_NOTE
from ui.ui      import show_title_screen, show_game_over_menu, draw_ui, wrap_text, show_settings_menu 
from game.character import (
    create_character,
    get_eligible_classes,
    get_modifier,
    create_character_non_curses
)


def return_to_title(stdscr):
    curses.flash()
    stdscr.clear()
    launch(stdscr)  # Restart the game loop


def launch(stdscr, player):
    # Outer loop lets us restart without exiting the program
    while True:
        # ——— Init per‐run state ———
        game_state = {
            "current_room": (0, 0, 0, "chapel"),
            "game_over":    False,
            "restart":      False
        }

        current_motd = get_motd()
        message_log  = []

        # Create initial blank player before title screen
        player = {
            "name":             "",
            "background":       "",
            "hp":               10,
            "max_hp":           10,
            "xp":               0,
            "inventory":        [],
            "location":         (0, 0, 0, "chapel"),
            "max_hp_bonus":     False,
            "verbose_travel":   False,
            "screen_reader_mode": False
        }

        # Show title screen and allow settings access
        choice = show_title_screen(stdscr, current_motd, player)

        if choice == "restart":
            continue
        if choice == "quit":
            return
        elif choice == "new":
            # Screen-reader (non-curses) path
            if player.get("screen_reader_mode"):
                print(f"DEBUG: Screen Reader Mode is {'ON' if player.get('screen_reader_mode') else 'OFF'}")
                run_non_curses_mode(player, rooms, items, current_motd, NPC_DEFS)
                return

            # Curses-based character creation (skip intro press‐any‐key)
            curses.curs_set(1)
            stdscr.nodelay(False)
            stdscr.keypad(True)

            # Loop until valid character created
            new_player = None
            while new_player is None:
                print("DEBUG: About to enter create_character()")
                new_player = create_character(stdscr, player)
                print("DEBUG: Returned from create_character()")

            player = new_player

            # Roll intro text
            intro_text = [
                "The chapel is dusty and quiet. Its silence feels safe—but not empty. "
                "The air is thick with memory. Spirits rest here, but their posture is unclear. "
                "You are either being welcomed... or warned.",

                "The country of Eldermere cannot be allowed to fall. Somewhere in these walls lies the answer. "
                "The Oracle lived many lifetimes ago. If anyone still knows the path, it is him.",

                "There must be a way to reach him. The time for answers is now."
            ]

            height, width = stdscr.getmaxyx()
            verify_room_links(rooms)

            for paragraph in intro_text:
                wrapped = wrap_text(paragraph, width - 4)
                message_log.extend(wrapped)
                message_log.append("")

            # Enter main game loop
            main_loop(stdscr, game_state, player, rooms, items, current_motd, message_log, NPC_DEFS)

            if not game_state.get("restart"):
                break


def run_non_curses_mode(player, rooms, items, motd, NPC_DEFS):
    print("DEBUG: Entered run_non_curses_mode()")
    print("Screen Reader Mode enabled. Switching to plain text interface...\n")
    print(f"MOTD: {motd}\n")

    # Character creation
    print("DEBUG: Starting character creation")
    player = create_character_non_curses(player)

    # Intro text
    intro_text = [
        "The chapel is dusty and quiet. Its silence feels safe—but not empty...",
        "The country of Eldermere cannot be allowed to fall...",
        "There must be a way to reach him. The time for answers is now."
    ]
    for paragraph in intro_text:
        print(paragraph)
        input("Press Enter to continue...\n")

    # Initial room description
    current_room = player["location"]
    print(f"You are in {rooms[current_room]['name']}")
    print(rooms[current_room]["look_description"])
    print()

    message_log = []

    # Main input loop
    print("DEBUG: Entering input loop")
    while True:
        command = input("> ").strip().lower()
        if command in ("quit", "exit"):
            print("Thanks for playing!")
            break

        result = handle_command(
            command,
            {"current_room": current_room},
            player,
            rooms,
            items,
            motd,
            message_log,
            NPC_DEFS
        )

        if isinstance(result, list):
            for line in result:
                print(line)
        elif isinstance(result, str):
            if result == "quit":
                print("Thanks for playing LocalMUD!")
                break
            else:
                print(result)

        current_room = player["location"]
        print()


def handle_idle_npc_actions(current_room, NPC_DEFS, message_log):
    present = NPC_DEFS.get(current_room, [])
    for npc in present:
        idle_lines = npc.get("idle_actions", [])
        if idle_lines and random.random() < 0.25:
            message_log.append(random.choice(idle_lines))


def main_loop(stdscr, game_state, player, rooms, items, current_motd, message_log, NPC_DEFS):
    curses.curs_set(1)
    stdscr.nodelay(False)

    while True:
        draw_ui(stdscr, game_state, player, rooms, message_log)

        height, width = stdscr.getmaxyx()
        input_y = height - 2
        stdscr.addstr(input_y, 2, "> ")
        stdscr.refresh()

        # ─── Get input via curses ───
        curses.echo()
        try:
            raw = stdscr.getstr(input_y, 4, width - 6).decode().strip()
        except Exception:
            raw = ""
        curses.noecho()

        if raw:
            message_log.append(f"> {raw}")

        # ─── Run parser ───
        result = handle_command(
            raw,
            game_state,
            player,
            rooms,
            items,
            current_motd,
            message_log,
            NPC_DEFS
        )

        # ─── Handle parser output ───
        if isinstance(result, list):
            message_log.extend(result)
        elif isinstance(result, str):
            if result == "quit":
                message_log.append("Thanks for playing LocalMUD!")
                break
            else:
                message_log.append(result)

        message_log.append("")

        # ─── NPC idle actions ───
        handle_idle_npc_actions(game_state["current_room"], NPC_DEFS, message_log)

        # ─── “Return to title” confirmation ───
        if result == "confirm_title":
            stdscr.clear()
            stdscr.addstr(5, 4, "Return to title screen? [Y]es / [N]o")
            stdscr.refresh()
            key = stdscr.getkey().lower()
            if key == "y":
                curses.flash()
                stdscr.clear()
                launch(stdscr, player)
                return
            else:
                message_log.append("Return canceled.")

        # ─── Check for Game Over ───
        if game_state.get("game_over"):
            choice = show_game_over_menu(stdscr, player)
            if choice == "restart":
                game_state["restart"] = True


if __name__ == "__main__":
    # Initialize blank player for launch()
    player = {
        "name":             "",
        "background":       "",
        "hp":               10,
        "max_hp":           10,
        "xp":               0,
        "inventory":        [],
        "location":         (0, 0, 0, "chapel"),
        "max_hp_bonus":     False,
        "verbose_travel":   False,
        "screen_reader_mode": False
    }

    if player.get("screen_reader_mode"):
        run_non_curses_mode(player, rooms, items, get_motd(), NPC_DEFS)
    else:
        curses.wrapper(lambda stdscr: launch(stdscr, player))
