import bpy

from .base            import BasePanel
from ..operator.stage import staged_objects
from ..utils.register import dcr_register

@dcr_register
class StagePanel(BasePanel, bpy.types.Panel):
    bl_idname  = 'VIEW3D_PT_stree_stage'
    bl_label   = 'Stage'
    bl_options = {'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):
        layout  = self.layout
        objects = bpy.data.objects.items()

        if len(objects) <= 0 or context.scene.stree_state.head != '':
            layout.label(text='N/A')
        else:
            col = layout.column()
            box = col.box().column(align=True)

            for (obj_name, obj) in objects:
                if obj.type in ['MESH', 'CURVE'] and not (context.scene.stree_preference.snapshot_suffix in obj_name):
                    row = box.row()
                    row.alignment = 'LEFT'
                    row.operator('stree.change_stage_state',
                                 icon='RADIOBUT_ON' if obj_name in staged_objects else 'RADIOBUT_OFF',
                                 text=f'{obj_name}',
                                 emboss=False).obj_name = obj_name
