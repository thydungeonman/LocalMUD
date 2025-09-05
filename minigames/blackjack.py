import random
import curses

def play(player, stdscr):
    # --- Deck Construction ---
    def build_deck():
        suits = ["♠", "♥", "♦", "♣"]
        ranks = {
            "A": 11,
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
            "7": 7, "8": 8, "9": 9, "10": 10,
            "J": 10, "Q": 10, "K": 10
        }
        deck = [{"rank": rank, "suit": suit, "value": value}
                for suit in suits for rank, value in ranks.items()]
        random.shuffle(deck)
        return deck

    # --- Draw a Card from Deck ---
    def draw_card(deck):
        return deck.pop() if deck else None

    # --- Compute Hand Value ---
    def hand_value(hand):
        total = sum(card["value"] for card in hand)
        aces = sum(1 for card in hand if card["rank"] == "A")
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    # --- Format Hand for Display ---
    def format_hand(hand):
        return " ".join([f"{card['rank']}{card['suit']}" for card in hand])

    while True:
        # --- Betting Phase ---
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
            if bet > player['gold']:
                bet = player['gold']
        except ValueError:
            bet = min(25, player['gold'])

        stdscr.addstr(8, 2, f"Bet accepted: {bet} gold")
        stdscr.refresh()
        stdscr.getch()

        # --- Initial Deal ---
        deck = build_deck()
        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        # --- Player Turn ---
        busted = False
        while True:
            total = hand_value(player_hand)
            stdscr.clear()
            stdscr.addstr(2, 2, f"Your hand: {format_hand(player_hand)} (Total: {total})")
            stdscr.addstr(3, 2, f"Dealer shows: {dealer_hand[0]['rank']}{dealer_hand[0]['suit']}")
            stdscr.addstr(5, 2, "[H]it or [S]tand?")
            stdscr.refresh()

            key = stdscr.getkey().lower()
            if key == "h":
                player_hand.append(draw_card(deck))
                total = hand_value(player_hand)
                if total > 21:
                    busted = True
                    stdscr.clear()
                    stdscr.addstr(2, 2, f"Your hand: {format_hand(player_hand)} (Total: {total})")
                    stdscr.addstr(4, 2, "You busted!")
                    stdscr.addstr(5, 2, f"You lose. -{bet} gold")
                    player['gold'] = max(0, player['gold'] - bet)
                    stdscr.addstr(7, 2, f"Your current gold: {player['gold']}")
                    stdscr.refresh()
                    stdscr.getch()
                    break
            elif key == "s":
                break

        # --- Dealer Turn & Outcome ---
        if not busted:
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(draw_card(deck))

            player_total = hand_value(player_hand)
            dealer_total = hand_value(dealer_hand)

            stdscr.clear()
            stdscr.addstr(2, 2, f"Your hand: {format_hand(player_hand)} (Total: {player_total})")
            stdscr.addstr(3, 2, f"Dealer hand: {format_hand(dealer_hand)} (Total: {dealer_total})")

            if dealer_total > 21:
                stdscr.addstr(5, 2, "Dealer busted!")
                stdscr.addstr(6, 2, f"You win! +{bet} gold")
                player['gold'] += bet
            elif player_total > dealer_total:
                stdscr.addstr(5, 2, f"You win! +{bet} gold")
                player['gold'] += bet

            elif player_total == dealer_total:
                stdscr.addstr(5, 2, "Push. No gold won or lost.")
            else:
                stdscr.addstr(5, 2, f"Dealer wins. -{bet} gold")
                player['gold'] = max(0, player['gold'] - bet)

            stdscr.addstr(7, 2, f"Your current gold: {player['gold']}")
            stdscr.refresh()
            stdscr.getch()

        # --- Play Again Prompt ---
        stdscr.addstr(9, 2, "Play again? [Y/N]")
        stdscr.refresh()
        if stdscr.getkey().lower() != "y":
            break
