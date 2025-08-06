# minigames/dicehighlow.py

import random
import curses

def play(player, stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(2, 2, "🎲 High-Low Dice Duel")
        stdscr.addstr(4, 2, f"You have {player['gold']} gold.")
        stdscr.addstr(5, 2, "Enter your bet amount:")
        stdscr.refresh()

        curses.echo()
        bet_input = stdscr.getstr(6, 2, 10).decode().strip()
        curses.noecho()

        try:
            bet = int(bet_input)
            if bet <= 0:
                raise ValueError
            if bet > player["gold"]:
                bet = player["gold"]
        except ValueError:
            bet = min(25, player["gold"])

        stdscr.addstr(8, 2, f"Bet accepted: {bet} gold")
        stdscr.refresh()
        stdscr.getch()

        # --- Roll Dice ---
        def roll_pair():
            return random.randint(1, 6) + random.randint(1, 6)

        player_roll = roll_pair()
        dealer_roll = roll_pair()

        stdscr.clear()
        stdscr.addstr(2, 2, f"You roll: {player_roll}")
        stdscr.addstr(3, 2, f"Dealer rolls: {dealer_roll}")

        if player_roll > dealer_roll:
            stdscr.addstr(5, 2, f"You win! +{bet} gold")
            player["gold"] += bet
        elif player_roll == dealer_roll:
            stdscr.addstr(5, 2, "It's a tie. No gold won or lost.")
        else:
            stdscr.addstr(5, 2, f"You lose. -{bet} gold")
            player["gold"] = max(0, player["gold"] - bet)

        stdscr.addstr(7, 2, f"Your current gold: {player['gold']}")
        stdscr.addstr(9, 2, "Play again? [Y/N]")
        stdscr.refresh()

        key = stdscr.getkey().lower()
        if key != "y":
            break
