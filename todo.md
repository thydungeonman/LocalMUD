# 🛠️ LocalMUD Development Notes

## ✅ Task List

### Core Features
- [ ] Add a `wait` command  
- [ ] Fix the screen wrapping issue  
- [ ] Implement command history (scroll through past commands with arrow keys)  
- [ ] Add color support using `curses.color_pair()` to highlight items/NPCs in logs  
- [ ] Create separate lists of backstories for each class  
- [ ] Add `XP` command to display only XP  

---

## 📘 Contributor Guide (Draft)

_To be completed once Git is fully integrated._

- Setup steps for local development  
- Coding standards and naming conventions  
- Accessibility goals (e.g. screen reader compatibility)  
- Collaboration etiquette and pull request workflow  

---

## ⚙️ Engine Priorities (Before Overworld)

### Room Metadata Standardization
Ensure every room includes:
- `visited` flag  
- `look_description`  
- Optional: `tags`, `region`  

### Flexible Rendering Modes
Prepare for non-Curses mode with abstraction:
- `render_text()` vs `render_ui()` separation  

### Player State Encapsulation
- Wrap player logic in a `Player` class or centralized `player_state` module  

### Event Hooks
Add lightweight hooks:
- `on_enter_room()`  
- `on_gain_xp()`  
_For future systems like Sovereign whispers_

### Dev Tools Expansion
Add a `devmode` toggle with commands:
- `teleport`  
- `reveal`  
- `dump_state`  
_Useful for Overworld testing_

---

## 📖 Story Exposition: When the ORB is Placed

> The orb flares with a sickly light as the air hums—a sound like a thousand whispers tangled together.  
> From the shadows of the mausoleum, a voice scrapes against your mind:  
> **"You... you who would seek answers from the dead. I am the Oracle of Eldermere, and your touch has broken the seal of ages. Listen well, mortal, for the cost of knowledge is now your burden."**  
> The voice softens, almost weary:  
> **"To save your land, go west—where the blackened stones of {OLD_VILLAGE} crumble. Its people once kept the old ways. Revive their rites, and you may yet stem the tide."**  
> A sudden tremor shakes the chapel. Dust falls from the ceiling as the orb's light pulses violently.  
> The Oracle's voice turns urgent, fraying at the edges:  
> **"But you have also awakened that which should have slept... The Echo Sovereign stirs in its tomb, and it hungers for the light you carry. Go quickly. The balance is undone."**  
> The light snuffs out. Silence returns heavier than before.

### Additional notes

# TODO: In future, consider parser modability via command registry and mod loader.
# Idea: mods/doom_mod.py with register(register_command) pattern.
# Danger: May consume entire dev cycle. Proceed only when ready.


---

