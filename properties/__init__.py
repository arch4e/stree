import bpy

from .preference import Preference
from .state      import State

properties = {
    bpy.types.Scene: {
        "stree_preference": bpy.props.PointerProperty(type=Preference),
        "stree_state"     : bpy.props.PointerProperty(type=State)
    }
}

def register():
    for _type, data in properties.items():
        for attr, prop in data.items():
            if hasattr(_type, attr):
                logging.warning(f"WARN: overwrite {_type} {attr}")

            try:
                setattr(_type, attr, prop)
            except Exception as e:
                print(e)

def unregister():
    for _type, data in properties.items():
        for attr in data.keys():
            delattr(_type, attr)
