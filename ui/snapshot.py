import bpy

from .base            import BasePanel
from ..operator.stage import staged_objects
from ..utils.register import dcr_register

@dcr_register
class SnapshotPanel(BasePanel, bpy.types.Panel):
    bl_idname  = 'VIEW3D_PT_stree_snapshot'
    bl_label   = 'Snapshot'
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):
        if bpy.data.collections.find(context.scene.stree_preference.collection_name) != -1:
            # +---layout -----------+
            # | ss_area | ctrl_area |
            # +---------------------+
            layout    = self.layout.row()
            ss_area   = layout.column()
            ctrl_area = layout.column()

            #
            # revert direction selecter
            #
            ss_area.prop(context.scene.stree_state, "revert_destination", text="dest")

            #
            # snapshot list
            #
            box = ss_area.box().column(align=True)
            row = box.row()
            row.alignment = "LEFT"
            row.operator("stree.view_snapshot",
                         icon="RADIOBUT_ON" if context.scene.stree_state.head == "" else "RADIOBUT_OFF",
                         text=f"working area",
                         emboss=False).focus = ""
            for c, _ in reversed(bpy.data.collections[context.scene.stree_preference.collection_name].children.items()):
                row = box.row()
                row.alignment = "LEFT"
                row.operator("stree.view_snapshot",
                             icon="RADIOBUT_ON" if c == context.scene.stree_state.head else "RADIOBUT_OFF",
                             text=f"{c}",
                             emboss=False).focus = c

            #
            # control button
            #
            ctrl_area.operator("stree.revert_objects", # revert
                               icon="LOOP_BACK",
                               text="",
                               emboss=False)
            ctrl_area.operator("stree.view_snapshot", # back to workarea
                               icon="CHECKMARK",
                               text="",
                               emboss=False).focus = ""
            ctrl_area.operator("stree.shift_focus", # increment head
                               icon="TRIA_UP",
                               text="",
                               emboss=False).direction = "NEW"
            ctrl_area.operator("stree.shift_focus", # decrement head
                               icon="TRIA_DOWN",
                               text="",
                               emboss=False).direction = "OLD"

