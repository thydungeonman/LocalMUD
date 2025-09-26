# minigames/slots.py
"""
LocalMUD Slot Machine Minigame (ASCII Edition)

Simple 3-reel slot machine using curses. Costs gold to play, pays out based on matches.
Symbols: 7, BAR, *, @, $
"""

import curses
import random
import time

SYMBOLS = ["7", "BAR", "*", "@", "$"]
PAYOUTS = {
    ("7", "7", "7"): 50,
    ("BAR", "BAR", "BAR"): 30,
    ("*", "*", "*"): 15,
    ("@", "@", "@"): 20,
    ("$", "$", "$"): 100,
}
SPIN_COST = 5

def play_slots(stdscr, player):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(2, 2, "=== LocalMUD Slot Machine ===")
    stdscr.addstr(4, 2, f"Each spin costs {SPIN_COST} gold.")
    stdscr.addstr(5, 2, f"You have {player['gold']} gold.")
    stdscr.addstr(7, 2, "Press [S] to spin or [Q] to quit.")
    stdscr.refresh()

    while True:
        key = stdscr.getkey().lower()
        if key == "q":
            break
        elif key == "s":
            if player["gold"] < SPIN_COST:
                stdscr.addstr(9, 2, "Not enough gold to spin!")
                stdscr.refresh()
                continue

            player["gold"] -= SPIN_COST
            stdscr.addstr(9, 2, "Spinning...")
            stdscr.refresh()
            time.sleep(0.5)

            reels = [random.choice(SYMBOLS) for _ in range(3)]
            stdscr.addstr(11, 4, f"[ {reels[0]} ] [ {reels[1]} ] [ {reels[2]} ]")
            stdscr.refresh()
            time.sleep(0.5)

            payout = PAYOUTS.get(tuple(reels), 0)
            if payout:
                player["gold"] += payout
                stdscr.addstr(13, 2, f"You win {payout} gold!")
            else:
                stdscr.addstr(13, 2, "No match. Better luck next time.")
            stdscr.addstr(14, 2, f"Gold: {player['gold']}")
            stdscr.addstr(16, 2, "Press [S] to spin again or [Q] to quit.")
            stdscr.refresh()
        else:
            stdscr.addstr(18, 2, "Invalid key. Use [S] or [Q].")
            stdscr.refresh()
