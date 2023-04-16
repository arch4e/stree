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
        col = self.layout.column()
        if bpy.data.collections.find(context.scene.stree_preference.collection_name) != -1:
            #
            # snapshot list
            #
            box = col.box().column(align=True)
            row = box.row()
            row.alignment = "LEFT"
            row.operator("stree.view_snapshot",
                         icon="RADIOBUT_ON" if context.scene.stree_state.head == "" else "RADIOBUT_OFF",
                         text=f"working area",
                         emboss=False).focus = ""
            for c, _ in bpy.data.collections[context.scene.stree_preference.collection_name].children.items():
                row = box.row()
                row.alignment = "LEFT"
                row.operator("stree.view_snapshot",
                             icon="RADIOBUT_ON" if c == context.scene.stree_state.head else "RADIOBUT_OFF",
                             text=f"{c}",
                             emboss=False).focus = c
