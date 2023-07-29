# -*- coding: utf-8 -*-
import bpy

from .common import BasePanel


class BranchPanel(BasePanel, bpy.types.Panel):
    bl_idname  = "VIEW3D_PT_stree_branch"
    bl_label   = "Branch"
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        layout = self.layout
        col    = layout.column()

        col.enabled = True if context.scene.stree_state.head == "" else False

        # selected branch
        col.label(text="Current Branch")
        col.prop(bpy.context.scene.stree_state, "current_branch", text="", icon="OUTLINER_COLLECTION")

        # branch creater
        col.separator(factor=1.0)
        col.label(text="Create New Branch")
        row = col.row()
        row.prop(bpy.context.scene.stree_state, "new_branch", text="Name")
        row.operator("stree.create_branch", icon="ADD", text="")

