# game/combat.py
"""
Lightweight combat helpers for parser-integrated combat.

Assumptions about inputs (keep these in sync with your parser / monster manager):
- player is a dict with at least:
    - "hp": int, "max_hp": int
    - "stats": dict with keys like "strength" and "endurance" (optional)
    - "xp": int (optional)
    - "inventory": list (optional)
- monster is a dict instance with at least:
    - "id": template id, "instance_id": runtime id
    - "name": display name
    - "hp": int, "max_hp": int
    - "attack": int, "defense": int
    - "xp": int (xp awarded on kill)
    - "loot": list of item ids (optional)

The module exposes small, well-documented functions the parser can call.
"""

from typing import Dict, List, Iterable, Optional, Tuple
import random

# -----------------------
# Low-level utilities
# -----------------------
def _roll_damage(base: int) -> int:
    """Return an integer damage roll between 1 and base (inclusive)."""
    if base <= 0:
        return 1
    return random.randint(1, base)

def _safe_get_stat(entity: Dict, key: str, default: int = 0) -> int:
    return int(entity.get("stats", {}).get(key, default) or default)

# -----------------------
# Core attack functions
# -----------------------
def player_attack_monster(player: Dict, monster: Dict) -> List[str]:
    """
    Perform the player's attack against the monster.
    Mutates monster['hp'].
    Returns a list of textual lines to show to the player.
    """
    lines: List[str] = []
    atk_stat = _safe_get_stat(player, "strength", 1)
    roll = _roll_damage(atk_stat)
    damage = max(0, roll - int(monster.get("defense", 0)))
    monster["hp"] = monster.get("hp", 0) - damage
    lines.append(f"You strike {monster['name']} for {damage} damage.")
    if monster["hp"] > 0:
        lines.append(f"{monster['name']} has {monster['hp']} HP left.")
    else:
        lines.append(f"You have slain {monster['name']}!")
    return lines

def monster_attack_player(player: Dict, monster: Dict) -> List[str]:
    """
    Monster performs its retaliatory attack.
    Mutates player['hp'].
    Returns lines describing the result.
    """
    lines: List[str] = []
    roll = _roll_damage(int(monster.get("attack", 1)))
    defense = _safe_get_stat(player, "endurance", 0)
    damage = max(0, roll - defense)
    player["hp"] = player.get("hp", player.get("max_hp", 0)) - damage
    lines.append(f"{monster['name']} attacks you for {damage} damage.")
    if player.get("hp", 0) > 0:
        lines.append(f"You have {player['hp']} HP left.")
    else:
        lines.append("You have been slain.")
    return lines

# -----------------------
# Round resolver (parser-friendly)
# -----------------------
def resolve_combat_round(player: Dict, monster: Dict, *, monster_manager=None) -> List[str]:
    """
    Execute one round: player attack first, then monster retaliates if alive.
    Handles death detection for monster and player but does NOT handle:
      - awarding XP/loot (award_xp_and_loot helper below does that)
      - removing monsters from manager (caller should remove on death using monster_manager)
    monster_manager is optional and only used by the caller to perform removal/persistence.
    Returns a list of lines suitable for the message log.
    """
    out: List[str] = []
    out.extend(player_attack_monster(player, monster))

    if monster.get("hp", 0) <= 0:
        # monster is dead; caller should handle XP/loot and removal
        return out

    # monster alive → retaliate
    out.extend(monster_attack_player(player, monster))
    return out

# -----------------------
# Kill handling helpers
# -----------------------
def award_xp_and_loot(player: Dict, monster: Dict, room: Dict, *, add_item_fn=None) -> List[str]:
    """
    Award XP and drop loot into the given room data structure.
    - player: mutated in place; ensures player["xp"] exists and is increased
    - monster: monster template/instance (read for xp/loot)
    - room: room dict where loot should be placed; caller provides shape (e.g., room.setdefault("items", []))
    - add_item_fn: optional callable add_item_fn(item_id, room) to control how items are inserted.
    Returns lines describing XP/loot awarded.
    """
    lines: List[str] = []
    xp = int(monster.get("xp", 0))
    player["xp"] = player.get("xp", 0) + xp
    if xp:
        lines.append(f"You gain {xp} XP.")

    loot = monster.get("loot") or []
    if not loot:
        return lines

    # drop items into room, using caller-provided function if present
    for item_id in loot:
        if callable(add_item_fn):
            add_item_fn(item_id, room)
        else:
            room.setdefault("items", []).append(item_id)
    lines.append(f"The {monster['name']}'s belongings are left behind.")
    return lines

# -----------------------
# Helpers
# -----------------------
def find_target_by_name_or_index(name: str, monsters_in_room: Iterable[Dict]) -> Optional[Dict]:
    """
    Resolve a target by name or by name with index suffix ("kobold 2" or "kobold#2").
    - name: raw user input (already lowercased)
    - monsters_in_room: iterable of monster instances (must contain "name" and "instance_id")
    Returns the matched monster instance or None.
    """
    name = name.strip()
    # handle "name#n" or "name n" suffix
    parts = name.replace("#", " ").rsplit(" ", 1)
    target_name = parts[0]
    idx = None
    if len(parts) == 2 and parts[1].isdigit():
        idx = int(parts[1])

    # build list of matches in display order
    matches = [m for m in monsters_in_room if m.get("name", "").lower() == target_name.lower()]

    if not matches:
        # try substring match (first match)
        for m in monsters_in_room:
            if target_name.lower() in m.get("name", "").lower():
                return m
        return None

    if idx is None:
        return matches[0]
    if idx <= 0 or idx > len(matches):
        return None
    return matches[idx - 1]

def is_dead(entity: Dict) -> bool:
    return int(entity.get("hp", 0)) <= 0
