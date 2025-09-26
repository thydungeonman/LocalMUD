# config.py
"""
LocalMUD — Configuration & Metadata

Centralizes constants, MOTD logic, and other configurable elements.
Supports seasonal and personalized MOTDs, including birthday messages.

Typical usage:
- Called by main.py to retrieve MOTD
- Can be expanded to include game settings and flags

Author: Alex

Dev Notes:
- Seasonal MOTDs are date-driven; consider adding in-game triggers later.
- Birthday support is hardcoded—could be made dynamic for multiple devs.
- Use this file to store global flags, version info, or debug toggles.
"""




import random
from datetime import datetime


CURRENT_MOTD = "Welcome to LocalMUD. The chapel awaits."
VERSION = "v0.8.4 - “Monsters Arise"
DEV_NOTE = "Adding monsters and groundwork for combat."

#List of words to apply to the dirty word filter.
DIRTY_WORDS = [
    "damn",
    "hell",
    "shit",
    "fuck",
    "bastard",
    "bitch",
    "ass",
    "douche",
    "twat",
]

DIRECTION_ALIASES = {
    "n": "north",   "s": "south",
    "e": "east",    "w": "west",
    "u": "up",      "d": "down",

    "north": "north",
    "south": "south",
    "east":  "east",
    "west":  "west",
    "up":    "up",
    "down":  "down",
}

MOTD_LIST = [
    "Welcome to LocalMUD. The chapel awaits.",
    "The ladle remembers.",
    "You feel watched, but not judged.",
    "A hero arises. Will it be you?",
    "The altar hums with forgotten power.",
    "The orb hums with quiet energy.",
    "A chill wind whispers through the eastern passage.",
    "You feel watched, though no one is near.",
    "The dust seems freshly disturbed...",
    "Something ancient stirs beneath the chapel.",
    "To the death mug of doom!",
    "The spoon is missing. Again.",
    "You awaken with the taste of ash and memory.",
    "The chapel doors creak, though no wind blows.",
    "A ladle once saved your life. You never thanked it.",
    "The candles flicker in Morse code. You don't speak Morse.",
    "You are not the first to enter. You may not be the last.",
    "The orb pulses. It knows your name.",
    "A whisper echoes: 'Inventory is empty. So is your soul.'",
    "The pews are warm. Someone was just here.",
    "You remember a dream about soup. It felt important.",
    "The shadows stretch longer than they should.",
    "The floorboards groan. They remember your weight.",
    "You feel cursed. Statistically, you might be.",
    "The ladle is watching. Always watching.",
    "You hear a distant clatter. It might be spoons.",
    "The chapel is quiet. Too quiet.",
    "A single word is etched into the wall: 'WHY?'",
    "You feel like you're being narrated.",
    "The wind howls through forgotten halls. Something ancient stirs beneath the stone.",
    "Steel is sharpened, oaths are sworn. Tonight, the stars bear witness to your fate.",
    "The map ends here—but the story doesn’t. Beyond the edge lies the truth.",
    "They said the Oracle died centuries ago. They were wrong. He waits.",
    "The kingdom is quiet. Too quiet. Every silence hides a scream.",
    "You were not chosen. You volunteered. That makes you dangerous.",
    "The moon is red tonight. The old blood calls. Will you answer?",
    "Legends are born in fire, but remembered in shadow. Step carefully.",
    "The vault is sealed. The key is lost. The enemy is already inside.",
    "You carry no crown, no title, no prophecy. Just resolve. That will be enough."
]

#You can rotate rare entries by using weighted random choices later
#Some could be tied to player stats or curse count in future versions
#Want to add seasonal or event-based MOTDs? Easy to modularize!

SEASONAL_MOTDS = {
    "halloween": [
        "The pumpkins whisper secrets.",
        "You hear a ghostly ladle clatter in the dark.",
        "The chapel is dressed in cobwebs. You hope they're decorative.",
        "The veil is thin tonight. The dead remember, and they are not done speaking.",
        "You lit the lantern. That was the invitation. Now they know you're here.",
        "The harvest moon rises. Something has crawled out of the soil to greet it.",
        "The manor doors creak open. No one invited you in. Something just wants to watch.",
        "Every shadow has a shape. Every whisper has a name. And tonight, they walk."
    ],
    "winter": [
        "Snow falls silently through the broken roof.",
        "You feel warmth, but the fire is long dead.",
        "The orb glows like a frosted lantern.",
        "The snow never stopped. It buried the roads, the warnings, and the last survivors.",
        "Frost clings to your blade. The cold is not your enemy—but it is watching.",
        "The ice cracked last night. Something beneath it remembered your name.",
        "Winter is quiet, but not empty. The silence is a trap, and you’ve stepped into it.",
        "The fire flickers low. Outside, the wind speaks in voices no one taught it."
    ],
    "birthday": [
        "The ladle bows to you. It knows what day it is.",
        "A single candle flickers atop the altar. Happy Birthday, Alex.",
        "You feel unusually powerful. The chapel senses your birthright.",
        "The orb pulses in celebration. It’s your day.",
        "The pews hum a quiet tune. It sounds like a birthday song."
    ],
    "april_fools": [
		"You awaken in the chapel. Everything is upside down. Including you.",
		"The Oracle has been replaced by a rubber chicken. It still knows the path.",
		"You feel watched. It's the devs. They're laughing.",
		"The pews are gone. Replaced by beanbags. The tapestries are memes now.",
		"The vault is sealed. The key is a banana. Good luck.",
		"You carry no prophecy. Just a kazoo. That will be enough."
	]
}


def get_motd(debug=False):
    today = datetime.now()
    month = today.month
    day = today.day

    seasonal = []
    source = "standard"

    # Birthday: March 6
    if month == 3 and day == 6:
        seasonal.extend(SEASONAL_MOTDS["birthday"])
        source = "birthday"
        
    # April Fools: April 1
    if month == 4 and day == 1:
        seasonal.extend(SEASONAL_MOTDS["april_fools"])
        source = "april_fools"


    # Halloween: Oct 25–31
    elif month == 10 and day >= 25:
        seasonal.extend(SEASONAL_MOTDS["halloween"])
        source = "halloween"

    # Winter: Dec 20–Jan 5
    elif (month == 12 and day >= 20) or (month == 1 and day <= 5):
        seasonal.extend(SEASONAL_MOTDS["winter"])
        source = "winter"

    pool = MOTD_LIST + seasonal
    motd = random.choice(pool)

    if debug:
        print(f"[DEBUG] MOTD Source: {source}")
        print(f"[DEBUG] Selected MOTD: {motd}")

    return motd


