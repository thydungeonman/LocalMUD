# npcs.py

NPC_DEFS = {
    (0, -2, 0, "chapel"): [
        {
            "id": "father_ansel",
            "name": "Father Ansel",
            "aliases": ["ansel", "father", "father ansel"],
            "type": "stationary",
            "greeting": "He glances at you. 'The marrow remembers, even if the bones forget.'",

            # NEW: topic-based replies for “talk to … about …”
            "responses": {
                "marrow": [
                    "He leans closer. 'Marrow carries the truth that flesh cannot.'"
                ],
                "bones": [
                    "'Bones crumble, but memory endures in marrow,' he murmurs."
                ],
                "chapel": [
                    "He motions around. 'This sanctuary was blessed long before I arrived.'"
                ],
                "memory": [
                    "'Memories linger in every stone and whispered prayer.'"
                ],
                # fallback for any unmatched topic
                None: [
                    "He tilts his head. 'Speak plainly, child, so I may answer.'"
                ]
            },

            "idle_actions": [
                "Father Ansel flips slowly through a hymnal.",
                "He hums a half-remembered chant beneath his breath.",
                "His eyes drift toward the stained glass, unblinking.",
                "He traces a circle in the dust with one finger."
            ],

            "triggers": [
                {
                    "condition": "player_xp > 5",
                    "response": "'You walk heavier now. The Echo Sovereign sees your steps.'"
                }
            ]
        }
    ],



#new npcs go here



}