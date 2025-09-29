# character.py
"""
LocalMUD — Character Creation Module

Handles the character creation process, including name entry, background selection,
and stat rolling using classic 3d6 mechanics. Returns a customized player dictionary
based on user input.

Typical usage:
- Called from main.py at game launch
- Builds on the base player template from player.py

Author: Alex

Dev Notes:
- Backgrounds are currently flavor-only but may influence stats or inventory in future versions.
- Stat rolling uses 3d6 for each core attribute to preserve classic RPG probability.
- Consider adding visual feedback or confirmation prompts for accessibility.
"""



import curses
import copy
import random
from utils.log_manager import log_error

'''

log_error("DEBUG: Starting class selection")
log_error(f"DEBUG: Rolled stats: {stats}")
log_error("DEBUG: Waiting for stat confirmation")
log_error("DEBUG: Copying stats into player dict")
log_error(f"DEBUG: Final player dict: {player}")
log_error("DEBUG: Calling update_modifiers()")
log_error("DEBUG: Returning player from create_character()")
'''


CORE_STATS = ["str", "dex", "int", "wis", "con", "cha"]

def safe_getkey(stdscr, timeout=5000):
    stdscr.timeout(timeout)
    try:
        return stdscr.getkey()
    except:
        return None
    finally:
        stdscr.timeout(-1)  # Reset to blocking mode

def calculate_bx_modifier(score):
    if score <= 3: return -3
    elif score <= 5: return -2
    elif score <= 8: return -1
    elif score <= 12: return 0
    elif score <= 15: return +1
    elif score <= 17: return +2
    else: return +3

def update_modifiers(player):
    for stat in ["str", "dex", "con", "int", "wis", "cha"]:
        base = player.get(stat, 10)
        temp = player.get("temp_mods", {}).get(stat, 0)
        total = base + temp
        player[f"{stat}_mod"] = calculate_bx_modifier(total)


CLASSES = {
    "Fighter": {"Strength": 9},
    "Thief": {"Dexterity": 9},
    "Cleric": {"Wisdom": 9},
    "Magic-User": {"Intelligence": 9},
    "Dwarf": {"Constitution": 9},
    "Elf": {"Intelligence": 9, "Strength": 9},
    "Halfling": {"Dexterity": 9, "Constitution": 9}
}

BACKGROUND_OPTIONS = [
    "Wandering Spoon Monk",
    "Orb Scholar",
    "Dustborn Acolyte",
    "Chapel Groundskeeper",
    "Unlicensed Curse Broker"
]

CLASS_DESCRIPTIONS = {
    "Fighter": "Strong and brave. Excels in combat.",
    "Thief": "Quick and cunning. Skilled in stealth and traps.",
    "Cleric": "Wise and faithful. Channels divine power.",
    "Magic-User": "Intelligent and mysterious. Wields arcane spells.",
    "Dwarf": "Sturdy and stoic. Masters of stone and steel.",
    "Elf": "Graceful and gifted. Combines sword and spell.",
    "Halfling": "Small and sneaky. Lucky and light-footed."
}


def safe_getkey(stdscr, timeout=None):
    if timeout is None:
        stdscr.timeout(-1)  # Blocking mode
    else:
        stdscr.timeout(timeout)

    try:
        return stdscr.getkey()
    except:
        return None


def roll_stats():
    log_error("DEBUG: Running roll_stats")
    return {stat: sum(random.randint(1, 6) for _ in range(3)) for stat in CORE_STATS}

def create_character(stdscr, base_player):
    log_error("DEBUG: running create_character")
    player = copy.deepcopy(base_player)
     
    # --- Inialize Gold ---
    player["gold"] = player.get("gold", 100)


    # ─── Name Entry ───
    curses.echo()
    stdscr.clear()
    stdscr.addstr(2, 2, "Welcome to LocalMUD Character Creation!")
    stdscr.addstr(4, 2, "Enter your name: ")
    stdscr.refresh()
    name = stdscr.getstr(4, 20, 20).decode().strip()
    curses.noecho()

    if not name:
        name = "Unnamed Wanderer"
    player["name"] = name
    log_error(f"DEBUG: Name entered: {player.get('name')}")
    
    player["curse_count"] = 0

    # ─── Stat Rolling ───
    while True:
        stats = roll_stats()
        eligible_classes = get_eligible_classes(stats)

        if not eligible_classes:
            continue

        stdscr.clear()
        stdscr.addstr(2, 2, "Your rolled stats:")
        for i, stat in enumerate(CORE_STATS):
            val = stats[stat]
            mod = get_modifier(val)
            stdscr.addstr(4 + i, 4, f"{stat}: {val} ({mod:+d})")

        stdscr.addstr(11, 2, "Available Classes:")
        for j, cls in enumerate(eligible_classes):
            description = CLASS_DESCRIPTIONS.get(cls, "")
            stdscr.addstr(12 + j, 4, f"- {cls} — {description}")

        stdscr.addstr(14 + len(eligible_classes), 2, "[A]ccept these stats or [R]eroll?")
        stdscr.refresh()

        key = safe_getkey(stdscr, timeout=None)
        if key and key.lower() == "a":
            player["stats"] = stats
            player.update(stats)  # Adds str, dex, etc. to player
            player["temp_mods"] = {stat: 0 for stat in ["str", "dex", "con", "int", "wis", "cha"]}
            update_modifiers(player)

            break
        elif key and key.lower() == "r":
            continue

    # ─── Class Selection ───
    eligible_classes = get_eligible_classes(player["stats"])
    stdscr.clear()
    stdscr.addstr(2, 2, "Choose your class:")
    for i, cls in enumerate(eligible_classes):
        description = CLASS_DESCRIPTIONS.get(cls, "")
        stdscr.addstr(4 + i, 4, f"[{i + 1}] {cls} — {description}")
    stdscr.refresh()

    while True:
        key = safe_getkey(stdscr)
        if key and key.isdigit():
            choice = int(key)
            if 1 <= choice <= len(eligible_classes):
                player["class"] = eligible_classes[choice - 1]
                break

    # ─── Background Selection ───
    stdscr.clear()
    stdscr.addstr(2, 2, f"Hello, {name}. Choose your background:")
    for i, bg in enumerate(BACKGROUND_OPTIONS):
        stdscr.addstr(4 + i, 4, f"[{i + 1}] {bg}")
    stdscr.refresh()

    while True:
        key = safe_getkey(stdscr)
        if key and key.isdigit():
            choice = int(key)
            if 1 <= choice <= len(BACKGROUND_OPTIONS):
                player["background"] = BACKGROUND_OPTIONS[choice - 1]
                break

    # ─── Hit Points ───
    hit_dice = {
        "Fighter": 8,
        "Thief": 4,
        "Cleric": 6,
        "Magic-User": 4,
        "Dwarf": 8,
        "Elf": 6,
        "Halfling": 6
    }

    con_mod = player.get("con_mod", 0)
    base_hp = random.randint(1, hit_dice[player["class"]])
    total_hp = max(1, base_hp + con_mod)

    player["max_hp"] = total_hp  # ✅ Always set max_hp
    player["hp"] = total_hp      # ✅ Start at full health

    if player.get("max_hp_bonus"):
        player["max_hp"] += 5
        player["hp"] = player["max_hp"]  # ✅ Re-sync current HP


    # ─── Calculate Ability Modifiers ───
    update_modifiers(player)

    # ─── Final Confirmation ───
    confirmed = False
    while not confirmed:
        stdscr.clear()
        stdscr.addstr(2, 2, "Your character:")
        stdscr.addstr(4, 4, f"Name: {player['name']}")
        stdscr.addstr(5, 4, f"Class: {player['class']}")
        stdscr.addstr(6, 4, f"Background: {player['background']}")
        stdscr.addstr(7, 4, f"HP: {player['hp']}")
        stdscr.addstr(8, 4, f"Max HP: {player['max_hp']}")  # ✅ Added for clarity


        

        # ─── Ability Scores and Modifiers ───
        stdscr.addstr(10, 4, "Stats:")
        
        stdscr.addstr(10, 2, "Abilities:")
        core_stats = ["str", "dex", "con", "int", "wis", "cha"]
        for i, stat in enumerate(core_stats):
            val = player.get(stat, 10)
            mod = player.get(f"{stat}_mod", 0)
            stdscr.addstr(11 + i, 6, f"{stat.upper():<3}: {val:>2} ({mod:+d})")


        stdscr.addstr(18, 2, "Is this character okay? [Y]es / [N]o")
        stdscr.refresh()

        key = safe_getkey(stdscr)
        if key and key.lower() == "y":
            confirmed = True
        elif key and key.lower() == "n":
            return None  # Signal to restart character creation externally

        for stat in CORE_STATS:
            player[stat] = stats[stat]  # Copy rolled stats into player dict

        player["temp_mods"] = {stat: 0 for stat in CORE_STATS}  # Initialize temp modifiers
        update_modifiers(player)  # Calculate final modifiers


    return player


def create_character_non_curses(player):
    print("DEBUG: Starting character creation")
    print("Character Creation (Screen Reader Mode)")
    player["name"] = input("Enter your name: ").strip()

    print("\nChoose your background:")
    backgrounds = ["Wanderer", "Scholar", "Soldier"]
    for i, bg in enumerate(backgrounds):
        print(f"{i + 1}. {bg}")
    choice = input("Enter number: ").strip()
    try:
        player["background"] = backgrounds[int(choice) - 1]
    except:
        player["background"] = "Wanderer"

    print(f"\nWelcome, {player['name']} the {player['background']}!")
    return player
    

def get_eligible_classes(stats):
    log_error("DEBUG: running get_eligible_classes")
    eligible = []
    for cls, reqs in CLASSES.items():
        if all(stats.get(stat, 0) >= value for stat, value in reqs.items()):
            eligible.append(cls)
    return eligible

def add_gold(player, amount):
    log_error("DEBUG: running add_gold")
    player["gold"] += amount
    print(f"{player['name']} now has {player['gold']} gold.")

def spend_gold(player, amount):
    if player["gold"] >= amount:
        player["gold"] -= amount
        print(f"{player['name']} spent {amount} gold. Remaining: {player['gold']}")
        return True
    else:
        print(f"{player['name']} doesn't have enough gold!")
        return False
