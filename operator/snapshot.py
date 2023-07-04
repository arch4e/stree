# -*- coding: utf-8 -*-
import bpy
import re


from .stage import staged_objects
from ..util.collection import create_collection, hide_collections


class RevertObjects(bpy.types.Operator):
    bl_idname      = "stree.revert_objects"
    bl_label       = "Revert Objects"
    bl_description = "Revert Objects"

    def execute(self, context):
        # this function works only in object mode only
        if bpy.context.mode != "OBJECT":
            return { "CANCELLED" }

        try:
            bpy.ops.object.select_all(action="DESELECT")

            backup_values = (
                bpy.data.collections[context.scene.stree_preference.collection_name].hide_select,
                bpy.data.collections[context.scene.stree_state.current_branch].hide_select,
                bpy.data.collections[context.scene.stree_state.head].hide_select
            )
            bpy.data.collections[context.scene.stree_preference.collection_name].hide_select = False
            bpy.data.collections[context.scene.stree_state.current_branch].hide_select       = False
            bpy.data.collections[context.scene.stree_state.head].hide_select                 = False

            #
            # select revert objects
            #
            if context.scene.stree_state.head != "":
                revert_objects = [x for (_, x) in bpy.data.collections[context.scene.stree_state.head].objects.items()]

            for obj in revert_objects:
                obj.select_set(True)

            #
            # revert objects
            #
            duplicated_objects = [obj.copy() for obj in bpy.context.selected_objects]
            for o in duplicated_objects:
                o.data = o.data.copy()
                bpy.data.collections[context.scene.stree_state.revert_destination].objects.link(o)

            #
            # rename objects
            #
            for o in duplicated_objects:
                object_name = o.name
                object_name = re.sub(rf"^\d*{context.scene.stree_preference.snapshot_suffix}.", "", object_name)
                object_name = re.sub(rf"{context.scene.stree_preference.snapshot_suffix}\.\d*$", "", object_name)
                o.name = o.data.name = f"rev_{object_name}"

            #
            # restore backup values
            #
            (
                bpy.data.collections[context.scene.stree_preference.collection_name].hide_select,
                bpy.data.collections[context.scene.stree_state.current_branch].hide_select,
                bpy.data.collections[context.scene.stree_state.head].hide_select
            ) = backup_values

            #
            # back to workspace
            #
            context.scene.stree_state.head = ""
            switch_all_collection_visibility("show")
            bpy.data.collections[context.scene.stree_preference.collection_name].hide_viewport = True

            return { "FINISHED" }
        except Exception as e:
            print(e)
            return { "CANCELLED" }


class TakeSnapshot(bpy.types.Operator):
    bl_idname      = "stree.take_snapshot"
    bl_label       = "Take Snapshot"
    bl_description = "Take snapshot of selected objects"

    def execute(self, context):
        # this function works only in object mode only
        if bpy.context.mode != "OBJECT":
            return { "CANCELLED" }

        try:
            #
            # init
            #
            if bpy.data.collections.find(context.scene.stree_preference.collection_name) == -1:
                create_collection(context.scene.stree_preference.collection_name, bpy.context.scene.collection)

            #
            # create snapshot collection
            #
            snapshot_name = f"{len(bpy.data.collections[context.scene.stree_state.current_branch].children.items())}" \
                            + context.scene.stree_preference.snapshot_suffix

            if context.scene.stree_state.current_branch != context.scene.stree_preference.collection_name \
               and context.scene.stree_state.current_branch != f"main{context.scene.stree_preference.branch_suffix}":
                snapshot_name += f".{context.scene.stree_state.current_branch}"

            create_collection(snapshot_name, bpy.data.collections[context.scene.stree_state.current_branch])

            #
            # define variables
            #
            root_collection     = bpy.data.collections[context.scene.stree_preference.collection_name]
            snapshot_collection = bpy.data.collections[snapshot_name]

            #
            # take snapshot
            #
            select_staged_objects()
            duplicated_objects = [obj.copy() for obj in bpy.context.selected_objects]
            for o in duplicated_objects:
                o.data = o.data.copy()
                snapshot_collection.objects.link(o)

            # rename objects
            for o in duplicated_objects:
                object_name = o.name
                object_name = re.sub(r"\.\d*$", "", object_name)
                o.name = o.data.name = snapshot_name + "." + object_name + context.scene.stree_preference.snapshot_suffix

            hide_collections([root_collection.name, snapshot_collection.name])

            return { "FINISHED" }
        except Exception as e:
            print(e)
            return { "CANCELLED" }


class ViewSnapshot(bpy.types.Operator):
    bl_idname      = "stree.view_snapshot"
    bl_label       = "View Snapshot"
    bl_description = "View snapshot"

    focus: bpy.props.StringProperty()

    def execute(self, context):
        if bpy.context.mode != "OBJECT" \
           or bpy.context.scene.stree_state.head == self.focus:
            return { "CANCELLED" }

        try:
            #
            # view snapshot
            #
            if bpy.context.scene.stree_state.head == "":
                switch_all_collection_visibility("hide")

                # show snapshot
                bpy.data.collections[context.scene.stree_preference.collection_name].hide_viewport = False
                bpy.data.collections[context.scene.stree_state.current_branch].hide_viewport       = False
                bpy.data.collections[self.focus].hide_viewport = False

            #
            # back to workspace
            #
            else:
                if self.focus == "":
                    switch_all_collection_visibility("show")

                    # hide snapshots
                    bpy.data.collections[context.scene.stree_preference.collection_name].hide_viewport = True
                    bpy.data.collections[context.scene.stree_state.current_branch].hide_viewport       = True
                else:
                    bpy.data.collections[bpy.context.scene.stree_state.head].hide_viewport = True
                    bpy.data.collections[self.focus].hide_viewport = False

            #
            # update head
            #
            context.scene.stree_state.head = self.focus

            return { "FINISHED" }
        except Exception as e:
            context.scene.stree_state.head = ""
            print(e)
            return { "CANCELLED" }


class ShiftFocus(bpy.types.Operator):
    bl_idname      = "stree.shift_focus"
    bl_label       = "Shift Focus"
    bl_description = "Shift Focus"

    direction: bpy.props.StringProperty()

    def execute(self, context):
        try:
            target = ""
            ss_id = context.scene.stree_state.head

            if self.direction == "NEW":
                if ss_id == "":
                    return { "FINISHED" }
                else:
                    ss_id = int(ss_id.split(".")[0]) + 1
            elif self.direction == "OLD":
                if ss_id == "":
                    ss_id = len(bpy.data.collections[context.scene.stree_state.current_branch].children.items()) - 1
                else:
                    ss_id = int(ss_id.split(".")[0]) - 1
                    if ss_id < 0:
                        return { "FINISHED" }
            else:
                return { "CANCELLED" }

            target = "".join([str(ss_id), context.scene.stree_preference.snapshot_suffix])

            # main branch or None
            if context.scene.stree_state.current_branch != context.scene.stree_preference.collection_name \
               and context.scene.stree_state.current_branch != f"main{context.scene.stree_preference.branch_suffix}":
                target += f".{context.scene.stree_state.current_branch}"

            if bpy.data.collections.find(target) != -1:
                bpy.ops.stree.view_snapshot(focus=target)
            else:
                bpy.ops.stree.view_snapshot(focus="")

            return { "FINISHED" }
        except Exception as e:
            context.scene.stree_state.head = ""
            print(e)
            return { "CANCELLED" }


def select_staged_objects():
    bpy.ops.object.select_all(action="DESELECT")

    for obj_name in staged_objects:
        if obj_name in [x for (x, _) in bpy.data.objects.items()]:
            bpy.data.objects[obj_name].select_set(True)


def switch_all_collection_visibility(flag):
    for _, collection in bpy.data.collections.items():
        collection.hide_viewport = False if flag == "show" else True

