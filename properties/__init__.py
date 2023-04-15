import bpy

from .preference import Preference

properties = {
    bpy.types.Scene: {
        "stree_preference": bpy.props.PointerProperty(type=Preference)
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
