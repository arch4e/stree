if 'bpy' not in locals():
    import bpy
    from . import base
else:
    import importlib
    importlib.reload(base)
