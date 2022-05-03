import enum


class HummingBirdMessages(enum.Enum):
    IDENTIFY = "*IDN?"

    # Motion Commands
    MOTION = ":MOTIon"
    START = f"{MOTION}:START"
    PAUSE = f"{MOTION}:PAUSE"

    # Recipe Commands
    RECIPE = ":RECIpe"
    SAVE_RECIPE = f"{RECIPE}:SAVE: "
    LOAD_RECIPE = f"{RECIPE}:LOAD: "
    LIST_RECIPES = f"{RECIPE}:LIST "

    # Configuration Commands
    CONFIG = ":CONFig"
    SET_CURRENT_RECIPE = f"{CONFIG}:SETRecipe: "