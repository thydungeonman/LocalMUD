# minigames/grimoire_gambit.py

import curses
import random

# === Card Class ===
class Card:
    def __init__(self, name, card_type, stats, effect):
        self.name = name
        self.card_type = card_type
        self.stats = stats  # {'T': int, 'R': int, 'B': int, 'L': int} or {}
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

        
    def render(self, stdscr):
        # Column header
        stdscr.addstr("    1      2      3\n")
        # Rows with labels A-C
        for row in "ABC":
            line = f"{row} "
            for col in "123":
                cell = self.cells[f"{row}{col}"]
                if cell:
                    # show owner and up to 3 chars of name for compactness
                    cell_text = f"{cell.owner}:{cell.name[:3]}"
                    line += f"[{cell_text:^5}] "
                else:
                    line += "[     ] "
            stdscr.addstr(line + "\n")
        stdscr.addstr("\n")


# === Player Class ===
class Player:
    def __init__(self, name, deck):
        self.name = name
        self.hand = random.sample(deck, 5)

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
        Card("Whispering Shade", "Creature", {'T':1, 'R':3, 'B':2, 'L':1}, "Flip bottom stat 1"),
        Card("Frost Wyrm", "Creature", {'T':3, 'R':1, 'B':2, 'L':3}, "Freeze adjacent"),
        Card("Iron Sentinel", "Creature", {'T':2, 'R':2, 'B':2, 'L':2}, "Center buff"),
        Card("Shadow Fang", "Creature", {'T':2, 'R':3, 'B':1, 'L':1}, "Flip diagonal"),
    ]

# === Game Loop ===
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

def start_game(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr("🃏 Welcome to Grimoire Gambit Redux!\n")
    grid = Grid()
    deck = generate_test_deck("A") + generate_test_deck("B")
    playerA = Player("Player A", deck)
    playerB = Player("Player B", deck)
    players = [playerA, playerB]

    turn = 0
    while turn < 9:
        current = players[turn % 2]
        stdscr.clear()
        stdscr.addstr(f"Turn {turn+1} – {current.name}\n")
        grid.render(stdscr)
        current.show_hand(stdscr)

        # Choose card
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

        # Choose coordinate (visible input; user must press Enter)
        coord = prompt_coords(stdscr, grid)
        if coord is None:
            stdscr.addstr("Invalid coordinate. Press any key to continue...\n")
            stdscr.getkey()
            continue

        # Place card
        card = current.hand.pop(choice)
        card.owner = 'A' if current == playerA else 'B'
        if grid.place_card(coord, card):
            stdscr.addstr(f"{card.name} placed at {coord}.\n")
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

