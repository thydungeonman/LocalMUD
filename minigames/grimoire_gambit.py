# minigames/grimoire_gambit.py

import curses
import random

# === Card Class ===
class Card:
    def __init__(self, name, card_type, stats, effect):
        self.name = name
        self.card_type = card_type  # 'Creature', 'Spell', etc.
        self.stats = stats  # dict or {}
        self.effect = effect
        self.owner = None

    def __str__(self):
        if self.stats:
            return f"{self.name} ({self.card_type}) T:{self.stats.get('T',0)} R:{self.stats.get('R',0)} B:{self.stats.get('B',0)} L:{self.stats.get('L',0)}"
        else:
            return f"{self.name} ({self.card_type})"

# === Grid Class ===
class Grid:
    def __init__(self):
        self.cells = {f"{row}{col}": None for row in "ABC" for col in "123"}

    def place_card(self, coord, card):
        if self.cells.get(coord) is None:
            self.cells[coord] = card
            return True
        return False

    def neighbors(self, coord):
        # Returns dict of neighbor coords with direction key relative to coord
        row, col = coord[0], coord[1]
        nbrs = {}
        # Top
        r_ord = ord(row) - 1
        if r_ord >= ord('A'):
            ncoord = f"{chr(r_ord)}{col}"
            nbrs['T'] = ncoord
        # Bottom
        r_ord = ord(row) + 1
        if r_ord <= ord('C'):
            ncoord = f"{chr(r_ord)}{col}"
            nbrs['B'] = ncoord
        # Left
        c_ord = str(int(col) - 1)
        if c_ord in "123":
            ncoord = f"{row}{c_ord}"
            nbrs['L'] = ncoord
        # Right
        c_ord = str(int(col) + 1)
        if c_ord in "123":
            ncoord = f"{row}{c_ord}"
            nbrs['R'] = ncoord
        return nbrs

    def render(self, stdscr):
        # Column header
        stdscr.addstr("    1      2      3\n")
        for row in "ABC":
            line = f"{row} "
            for col in "123":
                cell = self.cells[f"{row}{col}"]
                if cell:
                    cell_text = f"{cell.owner}:{cell.name[:3]}"
                    line += f"[{cell_text:^5}] "
                else:
                    line += "[     ] "
            stdscr.addstr(line + "\n")
        stdscr.addstr("\n")

# === Player Class ===
class Player:
    def __init__(self, name, deck, is_ai=False):
        # Ensure there are enough cards; sample without replacement
        deck_copy = list(deck)
        if len(deck_copy) < 5:
            # if deck too small, repeat it
            deck_copy = deck_copy * ((5 // max(1, len(deck_copy))) + 1)
        self.name = name
        self.hand = random.sample(deck_copy, 5)
        self.is_ai = is_ai

    def show_hand(self, stdscr):
        stdscr.addstr(f"{self.name}'s Hand:\n")
        for i, card in enumerate(self.hand):
            stdscr.addstr(f"{i+1}. {card}\n")
        stdscr.addstr("\n")

# === Sample Deck ===
def generate_test_deck(owner):
    return [
        Card("Fire Imp", "Creature", {'T':2, 'R':1, 'B':1, 'L':2}, "Burn adjacent"),
        Card("Stone Golem", "Creature", {'T':3, 'R':2, 'B':3, 'L':2}, "Immune to debuff"),
        Card("Arcane Surge", "Spell", {}, "Boost top stat"),
        Card("Mirror Trap", "Relic", {}, "Reflect spell"),
        Card("Whispering Shade", "Creature", {'T':1, 'R':2, 'B':2, 'L':3}, "Flip bottom stat 1"),
        Card("Frost Wyrm", "Creature", {'T':3, 'R':1, 'B':2, 'L':3}, "Freeze adjacent"),
        Card("Iron Sentinel", "Creature", {'T':2, 'R':1, 'B':1, 'L':2}, "Center buff"),
        Card("Shadow Fang", "Creature", {'T':2, 'R':3, 'B':1, 'L':1}, "Flip diagonal"),
    ]

# === Helper: directional comparison for flips ===
def flips_from_placement(grid, coord, card):
    flips = []
    nbrs = grid.neighbors(coord)
    for dir_, ncoord in nbrs.items():
        neighbor = grid.cells.get(ncoord)
        if neighbor and neighbor.owner != card.owner and card.stats and neighbor.stats:
            # compare card's stat toward neighbor vs neighbor's opposing stat
            if dir_ == 'T':
                atk = card.stats.get('T', 0)
                defn = neighbor.stats.get('B', 0)
            elif dir_ == 'B':
                atk = card.stats.get('B', 0)
                defn = neighbor.stats.get('T', 0)
            elif dir_ == 'L':
                atk = card.stats.get('L', 0)
                defn = neighbor.stats.get('R', 0)
            elif dir_ == 'R':
                atk = card.stats.get('R', 0)
                defn = neighbor.stats.get('L', 0)
            else:
                atk = 0; defn = 0
            if atk > defn:
                flips.append(ncoord)
    return flips

# === AI heuristic ===
def ai_choose_move(grid, player, opponent):
    best = None  # (score, tie_breaker, card_index, coord)
    empty_coords = [c for c, v in grid.cells.items() if v is None]
    center_pref = {"B2": 2, "A2": 1, "C2": 1, "B1": 1, "B3": 1}  # small preference map
    for ci, card in enumerate(player.hand):
        for coord in empty_coords:
            flips = flips_from_placement(grid, coord, card)
            score = len(flips) * 10  # flips are valuable
            score += center_pref.get(coord, 0)
            # tie breaker: sum of card stats (favor stronger cards)
            statsum = sum(card.stats.values()) if card.stats else 0
            tie = (statsum, -ci)  # prefer higher statsum, earlier card in hand
            candidate = (score, tie, ci, coord, len(flips))
            if best is None or (candidate[0] > best[0]) or (candidate[0] == best[0] and candidate[1] > best[1]):
                best = candidate
    if best:
        return best[2], best[3]
    # fallback: first card to first empty
    if player.hand and empty_coords:
        return 0, empty_coords[0]
    return None, None

# === Input helpers ===
def prompt_coords(stdscr, grid, prompt="Choose grid coordinate (e.g., B2): "):
    curses.echo()
    try:
        stdscr.addstr(prompt)
        stdscr.refresh()
        raw = stdscr.getstr().decode("utf-8").strip().upper()
    finally:
        curses.noecho()
    if raw in grid.cells:
        return raw
    return None

# === Game Loop ===
def start_game(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr("🃏 Welcome to Grimoire Gambit Redux!\n")
    grid = Grid()
    deck = generate_test_deck("A") + generate_test_deck("B")
    # Player A is human, Player B is AI (set is_ai True)
    playerA = Player("Player A", deck, is_ai=False)
    playerB = Player("Player B (AI)", deck, is_ai=True)
    players = [playerA, playerB]

    turn = 0
    while turn < 9:
        current = players[turn % 2]
        opponent = players[(turn + 1) % 2]
        stdscr.clear()
        stdscr.addstr(f"Turn {turn+1} – {current.name}\n")
        grid.render(stdscr)
        current.show_hand(stdscr)

        # Human turn
        if not current.is_ai:
            stdscr.addstr("Choose a card (1-5): ")
            stdscr.refresh()
            try:
                key = stdscr.getkey()
            except Exception:
                continue
            if key not in "12345":
                stdscr.addstr("Invalid selection. Press any key to continue...\n")
                stdscr.getkey()
                continue
            choice = int(key) - 1
            if choice >= len(current.hand):
                stdscr.addstr("Choice out of range. Press any key to continue...\n")
                stdscr.getkey()
                continue

            coord = prompt_coords(stdscr, grid)
            if coord is None:
                stdscr.addstr("Invalid coordinate. Press any key to continue...\n")
                stdscr.getkey()
                continue

        # AI turn
        else:
            stdscr.addstr("AI is thinking...\n")
            stdscr.refresh()
            # small deterministic pause for UX
            curses.napms(300)
            ai_choice, ai_coord = ai_choose_move(grid, current, opponent)
            if ai_choice is None or ai_coord is None:
                stdscr.addstr("AI had no valid moves. Press any key to continue...\n")
                stdscr.getkey()
                turn += 1
                continue
            choice = ai_choice
            coord = ai_coord
            stdscr.addstr(f"AI plays {current.hand[choice].name} at {coord}\n")
            stdscr.refresh()
            curses.napms(300)

        # Place card
        card = current.hand.pop(choice)
        card.owner = 'A' if current == playerA else 'B'
        if grid.place_card(coord, card):
            # resolve flips immediately (simple flip mechanic)
            flipped = flips_from_placement(grid, coord, card)
            for fc in flipped:
                grid.cells[fc].owner = card.owner
            if flipped:
                stdscr.addstr(f"Flipped {len(flipped)} adjacent card(s): {', '.join(flipped)}\n")
        else:
            stdscr.addstr("That square is already occupied. Press any key to continue...\n")
            current.hand.insert(choice, card)
            stdscr.getkey()
            continue

        stdscr.addstr("Press any key to continue...\n")
        stdscr.refresh()
        stdscr.getkey()
        turn += 1

    # === Endgame ===
    stdscr.clear()
    grid.render(stdscr)
    score = {'A': 0, 'B': 0}
    for cell in grid.cells.values():
        if cell:
            score[cell.owner] += 1
    stdscr.addstr(f"\nFinal Score: Player A: {score['A']} | Player B: {score['B']}\n")
    winner = "A" if score['A'] > score['B'] else "B" if score['B'] > score['A'] else "Tie"
    stdscr.addstr(f"🏆 Winner: {winner}\n")
    stdscr.addstr("Press any key to exit...\n")
    stdscr.refresh()
    stdscr.getkey()
