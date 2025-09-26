def build_region(region_id="devspace"):
    """
    Returns a dict of room_id -> room_data for Devspace.
    Small three-room test region (normalized to match other region schemas).
    """
    rooms = {}

    # Entrance / Hub
    rooms[f"{region_id}_0_0"] = {
        "name": "Devspace Entrance",
        "description": (
            "A squat, utilitarian archway marks the entrance to Devspace. "
            "Polished concrete meets patchy grass; a hand-painted sign reads "
            "\"Welcome to Devspace — Break things responsibly.\""
        ),
        "terrain": "urban",
        "visited": False,
        "look_description": (
            "The archway stands low and practical. A chipped plaque lists room names "
            "and a hastily drawn map points north to a Test Field and east to a Workshop."
        ),
        "items": [],
        "exits": {
            "north": f"{region_id}_0_1",
            "east": f"{region_id}_0_2"
        },
        "monsters": []
    }

    # Test Field (combat prototyping)
    rooms[f"{region_id}_0_1"] = {
        "name": "Test Field",
        "description": (
            "An open rectangle of trampled grass and painted target dummies. "
            "Strips of chalk form grids on the ground for measuring movement and range."
        ),
        "terrain": "plains",
        "visited": False,
        "look_description": (
            "Target dummies lean at odd angles and a scattering of practice arrows litters the soil. "
            "There's a sense that rules are meant to be tested here."
        ),
        "items": [],
        "exits": {
            "south": f"{region_id}_0_0"
        },
        "monsters": ["kobold_bx", "kobold_bx"]
    }

    # Quiet Workshop
    rooms[f"{region_id}_0_2"] = {
        "name": "Quiet Workshop",
        "description": (
            "Benches line the walls, each cluttered with tools, half-finished scripts, "
            "and a mug that still smells faintly of coffee. A single lamp casts a warm pool of light."
        ),
        "terrain": "indoor",
        "visited": False,
        "look_description": (
            "The workbench is organized chaos: labeled drawers, post-it notes, and a soldering iron cooling on a stand."
        ),
        "items": [],
        "exits": {
            "west": f"{region_id}_0_0"
        },
        "features": {
            "workbench": "A tidy workbench with labeled drawers. Good for tinkering."
        },
        "monsters": []
    }

    return rooms
