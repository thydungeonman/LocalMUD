# Changelog

### 🗺️ v0.8.3 — "Finding Ourself" - ???

### Added
- [Documentation] Added documentation for Grimoir Gambit, a planned collectable card game.
- [System] Added new functions to utils/helpers.py to assist with room ID translation.



---

### 🗺️ v0.8.2 — “The Cartographer’s Backbone” — 2025-08-11

### Added
- [World] Introduced `generate_room_templates()` to procedurally create room layouts from region bounds and terrain flavor.
- [World] Added new region modules:
  - `fellmore_cliffs.py`
  - `east_mill_plains.py`
  - `chapel.py`
- [World] Implemented `load_overworld()` to merge multiple regions into a unified room map.
- [World] Linked `fellmore_cliffs_2_2` to `east_mill_plains_0_2` for cross-region navigation.
- [Utils] Added `normalize_room_id()` to support flexible room key formats (tuple or string).
- [Docs] Rebuilt and expanded `datadictionary.md` to cover new region and utility modules.
- [Docs] Created Markdown checklist for remaining region system tasks.
- [Parser] Added an easter egg when the user types "DIR" or "CLS".

### Fixed
- [UI] Refactored `draw_ui()` and `handle_command()` to use normalized room keys.
- [System] Ensured handcrafted room formats like `(0, 0, 0, "chapel")` remain compatible.
- [Logging] Updated `log_manager.py` to write timestamped logs to `logs/ERRORLOG_*.txt`.
- [Logging] Automatically creates `logs/` directory if missing.
- [System] Fixed a broken import statement that was causing the game to crash at startup for days.

### Known Issues
- [Parser] 'help' command still causes game to crash.
- [Minigames] Blackjack message formatting remains inconsistent.
- [Docs] `readme.me` is still out of date.

---

### 🗺️ v0.8.00 — “The Dawn" — 2025-08-07

### Added
- [Documentation] Added `todo.txt`. Goals will no longer be tracked by haphazardly dumping them at the top of the changelog.
- [World] Introduced `region_templates.py` in `/world` for defining region layouts and room templates.
- [World] Created `room_builder.py` with:
  - `build_region(region_name, bidirectional=True)` to instantiate rooms and wire up exits.
  - `build_room(room_id, tmpl)` to turn a template into a room dictionary.
  - `connect_rooms(rooms, bidirectional=True)` for resolving exits and automatic reverse links.
  - Demo loader under `if __name__ == "__main__":` for quick local testing.
- [World] Added stubs for future `/world` modules:
  - `npc_spawner.py` for NPC population logic.
  - `item_distributor.py` for loot and item placement.
  - `world_state.py` for persisting dynamic world variables.
- [Docs] Updated `datadictionary.md` to include the new `/world` directory and describe its components.

### Changed
- [Docs] Refined descriptions and formatting in `datadictionary.md` to reflect new world-generation files.
- [Room Builder] Enhanced logging in `room_builder.py` to warn about exits pointing to undefined room IDs.
- [Logging] Cleaned up error logging by centralizing all log output through `utils/log_manager.py`, standardizing message formats (timestamp, level, context), and pruning duplicate or noisy entries in `ERRORLOG.txt`.
- [System] Migrated codebase to GitHub.

### Known Issues
- [Parser] 'help' command causes game to crash.
- [Minigames] Still some weirdness with how blackjack displays messages.
- [Documentation] readme.me is out of date.

### Notes
- The concept of the overworld has changed to a dynamic procedural generation method rather than hand crafted rooms. Dungeons and locations will remain hand crafted. This is a huge change in direction.

---

### 🗺️ v0.7.91 — “The Distraction” - 2025-08-06

### Added
- [System] `player.py` now tracks gold.
- [Minigames] Added blackjack and dice high/low.
- [Settings] Added a debug mode to the settings menu.
- [Parser] Added `DEBUG` command (dev-only) to trigger minigames, heal the player, and grant gold.
- [System] Added `world.py` to track the game state for a persistant world.
- [Documentation] Added `DataDictionary.md` to map out the sub directories and each file and what they do.

### Changed
- [System] Refactored codebase into subdirectories (`core/`, `ui/`, `assets/`, etc.) to improve modularity and scalability.

### Fixed
- [UI] Resolved missing intro splash due to incorrect file path.

### Notes
- This update lays groundwork for future economy mechanics. Refactor was smoother than expected, and the intro splash now loads correctly from assets/.

---

### 🗺️ v0.7.9 — “Paths & Places” - 2025-08-01

### Added
- [Parser] Added "Talk To [NPC] About [Topic] command.
- [System] Added Npcs.py to handle npc data.
- [Parser] NPCs are now announced to the user when the 'LOOK' command is used while one is present.

### Changed
- [Parser] Removed the confirmation screen when selecting "New Game" on the title screen.

### Fixed
- [World] Fixed a spelling error in the room "Vault of the Nameless Dead".

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
