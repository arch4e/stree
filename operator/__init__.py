if "bpy" not in locals():
    import bpy
    from . import snapshot
    from . import stage
else:
    import importlib
    importlib.reload(snapshot)
    importlib.reload(stage)
