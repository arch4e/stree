# -*- coding: utf-8 -*-
import bpy


#
# import local modules
#
from .operator.branch import CreateBranch
from .operator.snapshot import RevertObjects, TakeSnapshot, ViewSnapshot, ShiftFocus
from .operator.stage import ChangeStageState
from .property.preference import Preference as PreferenceProps
from .property.state import State as StateProps
from .ui.branch import BranchPanel
from .ui.snapshot import SnapshotPanel
from .ui.stage import StagePanel
from .util.props_register import register as props_register, unregister as props_unregister


#
# addon information
#
bl_info = {
    "name"       : "stree",
    "category"   : "3D View",
    "location"   : "View3D > Sidebar > stree",
    "description": "",
    "version"    : (0,0,1),
    "blender"    : (3,0,0),
    "author"     : "arch4e"
}


classes = [
    # operator
    CreateBranch,
    RevertObjects,
    TakeSnapshot,
    ViewSnapshot,
    ShiftFocus,
    ChangeStageState,

    # property
    PreferenceProps,
    StateProps,

    # ui
    BranchPanel,
    StagePanel,
    SnapshotPanel
]


def check_blender_version():
    if bpy.app.version < bl_info.get("blender"):
        unregister()
        raise ImportError("error: unsupported version")


def register():
    # Returns an exception current Blender version is not supported
    check_blender_version()

    try:
        for cls in classes:
            bpy.utils.register_class(cls)

        props_register()
    except Exception as e:
        print("error: registration failed")
        print(repr(e))
        pass


def unregister():
    try:
        for cls in classes:
            bpy.utils.unregister_class(cls)

        props_unregister()
    except Exception as e:
        print("error: unregistration failed")
        print(repr(e))
        pass


if __name__ == "__main__":
    register()

