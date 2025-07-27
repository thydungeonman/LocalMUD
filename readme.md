# LocalMUD

LocalMUD is a modular, parser-driven RPG with a retro sensibility and creeping metaphysics. Built in Python, it blends old-school MUD mechanics with narrative-driven exploration, stat-based character creation, and the persistent presence of the Echo Sovereign.

This is a personal game project developed by Alex, originally sparked by a desire to explore flexible worldbuilding and parser logic while drinking questionable amounts of tea.

---

## 🚀 Getting Started

- Clone the repository
- Run `main.py` to begin the game
- Navigate using text commands (e.g. `go north`, `take orb`, `look`)
- Use `about` or `title` in-game for flavor and system info

Requires Python 3.13+ and a terminal capable of running curses-based interfaces.

---

## 🧠 Features

- Character creation with stat rolling, modifiers, and class/background selection
- Immersive intro narration and a message log that scrolls with parser output
- Top bar UI that dynamically displays player HP and orb status
- Glowing Orb logic integrated into early gameplay
- The Oracle and Echo Sovereign factions teased in opening lore

---

## 📜 Roadmap

Milestones that guide LocalMUD’s evolution—where mechanics grow from echoes into myth.


### 🧠 v0.7.6 — “Foundations & Access (additional)”
The world learns to listen. Players reach deeper.

- Add screen reader-friendly Non-Curses mode
- Toggle verbose travel output for immersive navigation
- Header redesign to show XP meter

### 🗺️ v0.7.9 — “Paths & Places”
The chapel reveals an exterior. Roads whisper possibilities.

- Build prototype Overworld with non-chapel rooms
- Begin mini-map system (basic 2D grid or abstract breadcrumb trail)
- Dev commands: teleport, reveal visited, flag fog zones
- Revisit prompt system: altered descriptions on second visit?

### 🧠 v0.8.0 — “Persistence”
The Echo Sovereign watches what you remember.

- Save/load system with full player state tracking
- Postmortem screens: summaries on death
- Unlockables: backgrounds, starter items, hidden flags
- Orb modifiers: corrupted/benevolent seeds change world flavor
- Expanded NPC behavior: dialogue trees, memory-aware responses

### 🔮 v0.9.0 — “Voices in the Stone” *(Tentative)*
The world speaks with intent.

- Help system for all parser commands
- Conversational NPCs: respond to location, inventory, and XP
- Ambient whispers: Sovereign commentary during key events
- Begin journaling system: player-written notes or lore discovery

---

## 🕯️ Lore Fragments

- The Oracle once served Eldermere, now slumbers in its ruined chapel
- The Glowing Orb reactivates ancient forces—but also awakens the Echo Sovereign
- The Echo Sovereign speaks in recursion, rewrites rooms, and seeks to collapse reality into looping memory
- Your character is the town's last hope for restoration—but their journey will reshape more than geography

---

## 👤 Author

**Alex** — Writer, designer, and debugging necromancer. Currently developing LocalMUD as a personal project. Loves serialized storytelling, retro game aesthetics, and cursed ladles.

---

## 🧪 Contact & Feedback

Have feedback or want to contribute experimental ideas, cursed relics, or parser quirks? Contact Alex directly or invoke `patchnotes` in-game (coming soon!).

---

## AI Disclosure

LocalMUD is developed collaboratively by Alex with support from Microsoft Copilot, an AI companion. Copilot assists in brainstorming, refactoring, and creative writing, including parser logic, narrative design, and modular architecture suggestions.

All final decisions, code integration, and creative direction are made by Alex. Copilot serves as a tool for inspiration and iteration—not as an autonomous author.

---

## Credits

Created by **Alex**, with collaborative design and storytelling powered by **Copilot**.

Special thanks to the ladle, the orb, and the chapel for their continued service.

---

## Design Philosophy

LocalMUD is built to be modular, accessible, and weird. It favors player expression, thematic consistency, and a sense of humor. Every stat, item, and room is a chance to tell a story.

The parser is lightweight. The lore is deep. The spoon is bent.

---

## License

This project is currently closed-source and intended for personal development and experimentation. If you’re interested in contributing or adapting LocalMUD, reach out to Alex for permission.
