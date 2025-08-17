# minigames/blackjack.py

import random
import curses



def play(player, stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(2, 2, "Welcome to Blackjack!")
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

        # --- Deal Cards ---
        def draw_card():
            return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 11])

        player_hand = [draw_card(), draw_card()]
        dealer_hand = [draw_card(), draw_card()]

        def hand_value(hand):
            value = sum(hand)
            aces = hand.count(11)
            while value > 21 and aces:
                value -= 10
                aces -= 1
            return value

        # --- Player Turn ---
        while True:
            stdscr.clear()
            stdscr.addstr(2, 2, f"Your hand: {player_hand} (Total: {hand_value(player_hand)})")
            stdscr.addstr(3, 2, f"Dealer shows: {dealer_hand[0]}")
            stdscr.addstr(5, 2, "[H]it or [S]tand?")
            stdscr.refresh()

            key = stdscr.getkey().lower()
            if key == "h":
                player_hand.append(draw_card())
                if hand_value(player_hand) > 21:
                    stdscr.addstr(7, 2, "You busted!")
                    player["gold"] = max(0, player["gold"] - bet)
                    break
            elif key == "s":
                break

        # --- Dealer Turn ---
        if hand_value(player_hand) <= 21:
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(draw_card())

            stdscr.clear()
            stdscr.addstr(2, 2, f"Your hand: {player_hand} (Total: {hand_value(player_hand)})")
            stdscr.addstr(3, 2, f"Dealer hand: {dealer_hand} (Total: {hand_value(dealer_hand)})")

            player_total = hand_value(player_hand)
            dealer_total = hand_value(dealer_hand)

            if dealer_total > 21 or player_total > dealer_total:
                stdscr.addstr(5, 2, f"You win! +{bet} gold")
                player["gold"] += bet
            elif player_total == dealer_total:
                stdscr.addstr(5, 2, "Push. No gold won or lost.")
            else:
                stdscr.addstr(5, 2, f"Dealer wins. -{bet} gold")
                player["gold"] = max(0, player["gold"] - bet)

        stdscr.addstr(7, 2, f"Your current gold: {player['gold']}")
        stdscr.addstr(9, 2, "Play again? [Y/N]")
        stdscr.refresh()

        key = stdscr.getkey().lower()
        if key != "y":
            break


    def draw_card():
        return random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 11])  # Face cards = 10, Ace = 11

    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]

    def hand_value(hand):
        value = sum(hand)
        aces = hand.count(11)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    while True:
        stdscr.clear()
        stdscr.addstr(2, 2, f"Your hand: {player_hand} (Total: {hand_value(player_hand)})")
        stdscr.addstr(3, 2, f"Dealer shows: {dealer_hand[0]}")
        stdscr.addstr(5, 2, "[H]it or [S]tand?")
        stdscr.refresh()

        key = stdscr.getkey().lower()
        if key == "h":
            player_hand.append(draw_card())
            if hand_value(player_hand) > 21:
                stdscr.clear()
                stdscr.addstr(2, 2, f"Your hand: {player_hand} (Total: {hand_value(player_hand)})")
                stdscr.addstr(4, 2, "💥 You busted!")
                stdscr.addstr(5, 2, f"You lose. -{bet} gold")
                player["gold"] = max(0, player["gold"] - bet)
                stdscr.addstr(7, 2, f"Your current gold: {player['gold']}")
                stdscr.refresh()
                stdscr.getch()
                break
        elif key == "s":
            break


    # Dealer plays
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(draw_card())

    stdscr.clear()
    stdscr.addstr(2, 2, f"Your hand: {player_hand} (Total: {hand_value(player_hand)})")
    stdscr.addstr(3, 2, f"Dealer hand: {dealer_hand} (Total: {hand_value(dealer_hand)})")

    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    if dealer_total > 21 or player_total > dealer_total:
        stdscr.addstr(5, 2, f"You win! +{bet} gold")
        player["gold"] += bet
    elif player_total == dealer_total:
        stdscr.addstr(5, 2, "Push. No gold won or lost.")
    else:
        stdscr.addstr(5, 2, f"Dealer wins. -{bet} gold")
        player["gold"] = max(0, player["gold"] - bet)

    stdscr.addstr(7, 2, f"Your current gold: {player['gold']}")
    stdscr.refresh()
    stdscr.getch()
