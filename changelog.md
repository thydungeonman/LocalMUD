# Changelog

GOALS:
-Add a wait command.
-Fix the screenwrapping issue.
Command History: Let players scroll through past commands with arrow keys.
Color Support: Use curses.color_pair() to highlight items/NPCs in logs.
-Create seperate lists of backstories for each class
-XP command, display only XP

Expand on NPC dialog with father Ansel

When the ORB is placed:

The orb flares with a sickly light as the air hums—a sound like a thousand whispers tangled together.
From the shadows of the mausoleum, a voice scrapes against your mind:
"You... you who would seek answers from the dead. I am the Oracle of Eldermere, and your touch has broken the seal of ages. Listen well, mortal, for the cost of knowledge is now your burden."
The voice softens, almost weary:
"To save your land, go west—where the blackened stones of {OLD_VILLAGE} crumble. Its people once kept the old ways. Revive their rites, and you may yet stem the tide."
A sudden tremor shakes the chapel. Dust falls from the ceiling as the orb's light pulses violently.
The Oracle's voice turns urgent, fraying at the edges:
"But you have also awakened that which should have slept... The Echo Sovereign stirs in its tomb, and it hungers for the light you carry. Go quickly. The balance is undone."
The light snuffs out. Silence returns heavier than before.
-Look should display the title of the room.





🧠 Suggested Engine Priorities Before Overworld
Room metadata standardization Ensure every room has visited, look_description, and maybe tags or region.

Flexible rendering modes Prep for Non-Curses mode with a clean abstraction layer: render_text() vs render_ui().

Player state encapsulation Consider wrapping player in a Player class or at least a player_state module to keep logic centralized.

Event hooks Add lightweight hooks like on_enter_room() or on_gain_xp() so future systems (e.g. Sovereign whispers) can plug in without rewriting core logic.

Dev tools expansion Add a devmode toggle and commands like teleport, reveal, dump_state, etc. These will be invaluable during Overworld testing.

---

### 🧠 v0.7.6 — “Foundations & Access - Vertical Slice” - 2025-07-25

### Added
- [System] Added a 'verbose' mode which displays the full description every time you switch rooms, rather than only on the first visit.
- [System] Added a Screen Reader mode (experimental). Currently, starting a new game in this mode may freeze at the title screen.
- [System] Created ScreenReaderMode.txt do document how the screenreader mode is supposed to function so I can return to it later.
- [System] Added 10 new high-adventure MOTDs.
- [System] Added 10 seasonal MOTDs (5 Halloween, 5 Winter).
- [Parser] 'Get' now functions as an alias for 'Take'.
- [Parser] Added 'Up' and 'Down' functionality to the 'GO' command.

### Changed
- [UI] Cleaned up the settings menu.

### Fixed
- [System] Resolved crash when rejecting a character during confirmation.

### Known Issues
- [Accessibility] Screen Reader mode may freeze when starting a new game from the title screen. Workaround: use standard mode for now.

---

## [0.7.5] — "Foundations & Access" — 2025-07-23

### Changed

- [Title Screen] Refactored intro splash into an interactive menu with options for New Game, Settings, and Quit.
- [Parser] Directional shortcuts for movement (e.g. n, s, e) now award XP on first-time room entry, matching full go command behavior.

### Added
- [Parser] Character command now displays XP.
- [System] Discovering a new room now awards the player 1xp.
- [DevTools] Added automatic room link verification on launch. Broken exits are logged to ERRORLOG.txt.
- [UI] Added a settings menu accessible from the title screen.
- [System] Players can now toggle an optional max HP bonus during character creation.

---

## [0.7.0] — "The World Opens" — 2025-07-21

### Added
- [World] Added four new rooms to the chapel.
- [System] Added error handling for moving between rooms. Moving to a room that doesn't exist wont crash the game and also produces ERRORLOG.txt to help diagnose the issue.
- [System] Added the beginnings of an NPC system.
- [World] Father Ansel, residing in the Sanctuary, is now LocslMUD's first NPC.

### Changed
- [Parser] When using the GO command to switch rooms, the new room name now prints with the output.
- [Parser] Description now prints when entering a room for the first time.
- [Parser] Having 'e' as a shortcut for the examine command turned out to conflict with the go command shortcuts. Changed the examine shortcut to 'x'
- [Parser] Fixed the 'help' command. Title was listed twice for some reason.
- [System] NPCs now perform passive, randomized idle behaviors when the player lingers in a room.

---

## [0.6.0] — "The Fleshening" — 2025-07-18

### Added
- [System] Introduced `character.py` to manage character creation logic. Not to be confused with `player.py`, which stores the base player template and non-stat defaults.
- [Core] Implemented a character generation sequence triggered at launch: name entry, stat rolling, class/background selection, and HP assignment.
- [World] Intro paragraph now displays upon entering the chapel, establishing tone and player motivation.
- [Parser] Added `title` command to return to the title screen with confirmation prompt.

### Changed
- [Dev Experience] Added verbose comment headers to all modules for improved clarity and onboarding.
- [UI] Updated top bar to reflect character's actual HP values post-creation.

---

## [0.5.0] — "The Great Refactor" — 2025-07-17

### Added
- [System] `rooms.py` now holds all room data.
- [System] `player.py` now holds all player stat data.
- [System] `items.py` now holds all item data.
- [System] `parser.py` now holds all command and parser logic.
- [System] `config.py` now centralizes configurable constants and metadata.
- [System] `ui.py` now holds all UI code.
- [Parser] Added a dirty word filter that tracks curse usage and logs it as a harmless statistic in the character sheet.
- [Parser] Added a `character` command to display player stats. Also works with just `C`.
- [UI] Added a game over screen with restart/load/quit options.

### Changed
- [System] Trimmed down the functionality crammed into `main.py`, delegating to modular files.
- [Parser] `inventory` command now also works with `I`.
- [Parser] `examine` command now also works with `X`.
- [Parser] `look` command now also works with `L`.
- [System] Retired `MOTD.txt` in favor of centralized MOTD handling in `config.py`.
- [System] MOTD logic now lives in `config.py`, with seasonal and birthday support.
- [UI] Intro screen now displays MOTD with proper reverence.
- [Flavor] The ladle now celebrates Halloween, winter, and Alex’s birthday.

---

## [0.4.0] — "A Hero Arises" — 2025-07-16

### Added
- [Parser] Added 'Examine' command to the parser allowing the user to examine items in thier possesion as well as objects in the room.
- [System] Added a verbose description propery to each item that can only be seen by using the examine command.
- [World] Room data now supports examinable environmental objects, enriching world detail and interactivity.

### Changed
- [UI] Refined spacing and layout for cleaner message log readability and improved input/output flow.
- [Player] Expanded player data to include a full OSR-style stat block, laying groundwork for future combat and progression.
- [World] Rooms now track whether they’ve been visited, enabling exploration-based logic and flavor.
- [System] Room coordinates upgraded from (x, y) to (x, y, z, instance), supporting multi-level maps and alternate realities.
- [Feature] MOTD now dynamically selected at launch from a curated list in the `config.py` file.
- [Dev Note] Refactor complete. Codebase now modular, scalable, and easier to maintain.
- [Parser] Fixed the previously broken quit command.

---

## [0.3.0] — "Orb Awakens" — 2025-07-15

### Added
- [Parser] Added 'HELP' and 'ABOUT' commands to the parser.
- [UI] Added a splash screen when starting LocalMUD
- [UI] Added message of the day to startup splash screen which pulls from MOTD.txt

### Changed
- [UI] Updated the layout to resemble a scrolling chat log with a static top bar, inspired by Infocom games.
- [Parser] Fixed the 'use' command so the orb is now usable.
- [System] Separated the orb item logic from the parser; items are now modular.
- [UI] Expanded 'go' command to support shorthand inputs like 'e', 'east', or standalone direction commands.

### Removed
- [System] Removed the dev instance. It made more trouble than it was preventing.
- [UI] Removed constant inventory display from the interface.

---

## [0.2.0] — "Looking Clearly" — 2025-07-14

### Added
- [World] Added 'look_description' to rooms for richer environmental detail.
- [Parser] Made the 'look' command dynamically list exits and items in the room.

### Changed
- [UI] Improved window resizing behavior for better layout stability.

### Development
- [System] Created a development instance (main_dev.py) for testing changes.

---

## [0.1.0] — "In the beginning, there was nothingness." — 2025-07-12

### Added
- [Core] Built the first playable prototype: two rooms, a parser, and a collectable item.

### Setup
- [System] Established the project using Python and a console-based interface.
