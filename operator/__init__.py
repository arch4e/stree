if "bpy" not in locals():
    import bpy
    from . import stage
else:
    import importlib
    importlib.reload(stage)
