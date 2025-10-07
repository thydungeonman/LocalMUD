# 🃏 Grimoire Gambit Redux – Design Document

## 🎯 Concept Overview
Grimoire Gambit Redux is a hybrid collectible card game played on a 3x3 grid, blending the spatial strategy of Final Fantasy-style grid duels with the tactical depth of Magic: The Gathering-style card effects. Designed for text-based play, it emphasizes accessibility, modularity, and lore-rich gameplay.

## 🧠 Design Goals
- Modular card definitions for easy expansion
- Strategic depth through placement and effects
- Fully playable via command line interface
- Screen-reader friendly and accessible
- Optional integration with LocalMUD or standalone fork

---

## 🗺️ Game Board
- 3x3 grid labeled A1–C3
- Players take turns placing cards onto empty grid spaces
- Grid coordinates used for interaction (e.g., `place Fire Imp at B2`)
- Optional visual rendering via Curses or ASCII

---

## 🃏 Card Anatomy

Each card has:
- **Name**
- **Type**: Creature, Spell, Relic, Trap, Lore
- **Directional Stats**: Top, Right, Bottom, Left (for grid-based combat)
- **Effect Text**: Describes ability or trigger
- **Flavor Text**: Optional lore snippet
- **Rarity**: Common, Rare, Epic, Legendary

### Example Card – Fire Imp
- Type: Creature  
- Stats: T:2 R:1 B:1 L:2  
- Effect: Burns adjacent enemy, reducing their stats by 1  
- Flavor: "Born in the ashes of forgotten spells."

---

## 🧩 Gameplay Flow

### Setup
- Each player draws 5 cards from their deck
- Grid is empty at start
- Players alternate turns

### Turn Actions
- Place a card on an empty grid space
- Trigger any placement effects
- Resolve flips or stat comparisons with adjacent cards
- Optional: Cast spells, activate relics, inspect cards

### Victory Conditions
- **Grid Conquest**: Control more grid spaces than opponent after all cards placed
- **Alternate Modes** (future): HP-based duels, monster elimination, puzzle challenges

---

## 🧙 Card Types & Effects

### Creature
- Has directional stats
- May flip adjacent cards based on stat comparisons
- Can have passive or triggered effects

### Spell
- One-time effects: buff, debuff, draw, destroy
- Target specific cards or grid zones

### Relic
- Passive effects while on the board
- May affect entire rows, columns, or player state

### Trap
- Hidden until triggered
- Can flip, destroy, or negate cards

### Lore
- Flavor-only or unlocks secrets in LocalMUD

---

## 🧮 Sample Match Snapshot

- Player A places **Fire Imp** at B2  
- Player B places **Iron Sentinel** at A2  
- Sentinel flips Fire Imp via stat comparison  
- Player A casts **Arcane Surge** to boost Fire Imp’s top stat  
- Player B places **Shadow Fang** at C2, attempts diagonal flip  
- Match ends with grid control: Player B wins 5–4

---

## 🔧 Technical Notes

- Cards stored as modular Python files or JSON objects
- Grid state tracked via 2D array or dict
- Effects resolved via rule engine or command parser
- Optional Curses rendering for visual grid
- Designed to be forkable from LocalMUD or embedded as a module

---

## ⚠️ Design Challenges

- Directional stats may be hard to visualize in pure text
- Balancing stat/effect interactions
- Ensuring accessibility for blind players
- Avoiding feature creep from complex card effects

---

## 🧪 Future Ideas

- PvE duels against NPC decks
- Card crafting and upgrades
- Seasonal card drops (e.g. April Fools, Halloween)
- Lore integration with LocalMUD regions and events
- Puzzle mode: solve grid challenges with limited cards

