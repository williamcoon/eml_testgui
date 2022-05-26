import enum


class HummingBirdMessages(enum.Enum):
    IDENTIFY = "*IDN?"

    # Motion Commands
    MOTION = ":MOTIon"
    START = f"{MOTION}:START"
    PAUSE = f"{MOTION}:PAUSE"
    HOME = f"{MOTION}:HOME"
    SET_CURRENT_RECIPE = f"{MOTION}:SELEctRecipe: "

    # Recipe Commands
    RECIPE = ":RECIpe"
    SAVE_RECIPE = f"{RECIPE}:SAVE: "
    LOAD_RECIPE = f"{RECIPE}:LOAD: "
    LIST_RECIPES = f"{RECIPE}:LIST "
    DELETE_RECIPE = f"{RECIPE}:DELEte: "
    UPDATE_RECIPE = f"{RECIPE}:UPDAte: "
    GET_CURRENT_RECIPE = f"{RECIPE}:GET: "
    CREATE_RECIPE = f"{RECIPE}:NEW: "

    # Configuration Commands
    CONFIG = ":CONFig"
