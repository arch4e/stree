if 'bpy' not in locals():
    import bpy
    from . import base
    from . import stage
else:
    import importlib
    importlib.reload(base)
    importlib.reload(stage)
