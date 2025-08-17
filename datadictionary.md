# 📁 LocalMUD Data Dictionary  
_Last updated: 2025-08-07_  

This document outlines the file structure and purpose of each component in the LocalMUD project.  

---

## Root Directory  

| File/Folder            | Description                                            |
|------------------------|--------------------------------------------------------|
| `main.py`              | Entry point for the game.                              |
| `config.py`            | Configuration settings.                                |
| `run.bat`              | Batch file to launch the game.                         |
| `readme.md`            | Project overview and setup instructions.               |
| `changelog.md`         | Tracks changes and updates.                            |
| `ERRORLOG.txt`         | Logs runtime errors.                                   |
| `ScreenReaderMode.txt` | Notes and debugging status for screen reader support.  |
| `datadictionary.md`    | This file. Describes the file layout and purpose.      |

---

## `/assets`  

_Stores sound and art files._  

| File         | Description                             |
|--------------|-----------------------------------------|
| `intro.txt`  | Introductory text or narration.         |
| `Lore.txt`   | Game lore and world-building content.   |

---

## `/data`  

_Data files and placeholders._  

| File         | Description                                               |
|--------------|-----------------------------------------------------------|
| `items.json` | Placeholder for item data. Full logic still in `items.py`.|

---

## `/game`  

_Core game logic and mechanics._  

| File           | Description                                |
|----------------|--------------------------------------------|
| `character.py` | Character creation and stats.              |
| `events.py`    | Event handling and triggers.               |
| `items.py`     | Item definitions and logic.                |
| `npcs.py`      | NPC behavior and dialogue.                 |
| `parser.py`    | Command parser and input handling.         |
| `player.py`    | Player-specific logic.                     |
| `rooms.py`     | Room definitions and navigation.           |
| `save.py`      | Save/load functionality.                   |
| `world.py`     | Legacy world generation (superseded).      |

---

## `/logs`  

_Error logs._  

| File/Folder           | Description                                   |
|-----------------------|-----------------------------------------------|
| *(various txt files)* | Log files Get dumped here                     |

---

## `/minigames`  

_Self-contained mini-games._  

| File              | Description                               |
|-------------------|-------------------------------------------|
| `blackjack.py`    | Blackjack mini-game.                      |
| `dicehighlow.py`  | Dice-based high/low guessing game.        |

---

## `/old`  

_Archived versions._  

| File/Folder           | Description                                   |
|-----------------------|-----------------------------------------------|
| *(various zip files)* | Old program versions. Git migration pending.  |

---

## `/saves`  

_Saved game files._  

| File/Folder           | Description                          |
|-----------------------|--------------------------------------|
| *(various save files)*| Stores user save data.               |

---

## `/ui`  

_User interface components._  

| File       | Description                   |
|------------|-------------------------------|
| `ui.py`    | UI logic and rendering.       |

---

## `/utils`  

_Helper modules and utilities._  

| File              | Description                          |
|-------------------|--------------------------------------|
| `log_manager.py`  | Manage error and debug logging.      |
| `helpers.py`      | General-purpose utility functions.   |

---

## `/world`  

_World generation, templates, and future spawners._  

| File                   | Description                                                                                       |
|------------------------|---------------------------------------------------------------------------------------------------|
| `region_templates.py`  | Predefined region layouts and room templates.                                                     |
| `room_builder.py`      | Logic to construct room dictionaries from templates and wire up exits (bidirectional by default). |
| `npc_spawner.py`       | (Future) Populate rooms with NPC instances based on spawn rules and densities.                    |
| `item_distributor.py`  | (Future) Assign items and loot to rooms according to distribution logic and rarity.               |
| `world_state.py`       | (Optional) Track persistent world variables, dynamic events, and region states.                   |
| `chapel.py`            |
| `east_mill_plains.py`  |
| `fellmore_cliffs.py`   |
| `overworld.py`         |
