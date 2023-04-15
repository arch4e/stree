bl_info = {
    'name'       : 'stree',
    'category'   : '3D View',
    'location'   : 'View3D > Sidebar > stree',
    'description': '',
    'version'    : (0,0,1),
    'blender'    : (3,0,0),
    'author'     : 'arch4e'
}

if 'bpy' not in locals():
    import bpy
    from . import utils
else:
    import importlib
    importlib.reload(utils)

def check_blender_version():
    if bpy.app.version < bl_info.get('blender'):
        unregister()
        raise ImportError('error: unsupported version')

def register():
    # Returns an exception current Blender version is not supported
    check_blender_version()

    try:
        for cls in utils.register.class_list:
            bpy.utils.register_class(cls)
    except Exception as e:
        print('error: registration failed')
        print(repr(e))
        pass

def unregister():
    try:
        for cls in reversed(utils.register.class_list):
            bpy.utils.unregister_class(cls)
    except Exception as e:
        print('error: unregistration failed')
        print(repr(e))
        pass

if __name__ == '__main__':
    register()
