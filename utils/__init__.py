if 'bpy' not in locals():
    import bpy
    from . import collection
    from . import register
else:
    import importlib
    importlib.reload(collection)
    importlib.reload(register)
