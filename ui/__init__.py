if 'bpy' not in locals():
    import bpy
    from . import base
    from . import snapshot
    from . import stage
else:
    import importlib
    importlib.reload(base)
    importlib.reload(snapshot)
    importlib.reload(stage)
