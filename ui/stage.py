# -*- coding: utf-8 -*-
import bpy

from .common import BasePanel
from ..operator.stage import staged_objects


class StagePanel(BasePanel, bpy.types.Panel):
    bl_idname  = "VIEW3D_PT_stree_stage"
    bl_label   = "Stage"
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        layout  = self.layout
        objects = bpy.data.objects.items()

        col = layout.column()
        col.enabled = True if context.scene.stree_state.head == "" else False
        col.operator("stree.take_snapshot", text="take snapshot")

        box = col.box().column(align=True)
        for (obj_name, obj) in objects:
            if obj.type in ["MESH", "CURVE"] and not (context.scene.stree_preference.snapshot_suffix in obj_name):
                row = box.row()
                row.alignment = "LEFT"
                row.operator("stree.change_stage_state",
                             icon="CHECKBOX_HLT" if obj_name in staged_objects else "CHECKBOX_DEHLT",
                             text=f"{obj_name}",
                             emboss=False).obj_name = obj_name

