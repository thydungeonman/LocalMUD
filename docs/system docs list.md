# 📁 LocalMUD System Docs – Suggested Breakdown

## 🗺️ Region & Room Loading
- Purpose of `overworld.py` as central coordinator
- How regions are defined and loaded
- Room structure, metadata, and modding support
- Hooks for spawning monsters, NPCs, or events

## 👥 NPC Mechanics (Legacy & Refactor Plan)
- Overview of pre-refactor NPC system
- What’s broken, what’s salvageable
- Vision for modular, event-driven NPC behavior
- Dialogue, movement, and interaction scaffolding

## ⚔️ Combat System
- B/X rules implementation
- Stat handling, equipment, turn order
- Monster vs player logic
- Active development notes and TODOs

## 🧠 Parser & Command Handling
- Structure of `handle_command()`
- Known limitations and refactor roadmap
- Command categories and parsing quirks

## 📦 Persistence & Save System
- Current state (TBD)
- Goals for player and world state saving
- Accessibility considerations (e.g. screen reader compatibility)

## 📊 Debugging & Logging
- Breadcrumb system design
- What’s broken and why
- Plans for modular, readable logs
