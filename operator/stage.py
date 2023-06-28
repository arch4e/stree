# -*- coding: utf-8 -*-
import bpy


staged_objects = []


class ChangeStageState(bpy.types.Operator):
    bl_idname      = "stree.change_stage_state"
    bl_label       = "stree: Change Stage State"
    bl_description = "The selected object is the target of the snapshot."

    obj_name: bpy.props.StringProperty()

    def execute(self, context):
        try:
            if self.obj_name in staged_objects:
                staged_objects.remove(self.obj_name)
            else:
                staged_objects.append(self.obj_name)

            return { "FINISHED" }

        except Exception as e:
            print(e)
            return { "CANCELLED" }

