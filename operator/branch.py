# -*- coding: utf-8 -*-
import bpy

from ..util.collection import change_parent_collection, create_collection


class CreateBranch(bpy.types.Operator):
    bl_idname      = "stree.create_branch"
    bl_label       = "Create Branch"
    bl_description = ""

    def execute(self, context):
        branch_suffix = context.scene.stree_preference.branch_suffix

        #
        # root collection
        #
        if bpy.data.collections.find(context.scene.stree_preference.collection_name) == -1:
            create_collection(context.scene.stree_preference.collection_name, bpy.context.scene.collection)

        #
        # move the snapshot before branch creation to the main branch
        #
        if context.scene.stree_state.current_branch == context.scene.stree_preference.collection_name:
            snapshots = bpy.data.collections[context.scene.stree_preference.collection_name].children.items()
            create_collection(
                f"main{branch_suffix}",
                bpy.data.collections[context.scene.stree_preference.collection_name]
            )

            root_collection = bpy.data.collections[context.scene.stree_preference.collection_name]
            main_collection = bpy.data.collections[f"main{branch_suffix}"]
            for c in [c_data for (c_name, c_data) in snapshots if context.scene.stree_preference.snapshot_suffix in c_name]:
                change_parent_collection(root_collection, main_collection, c)

        #
        # create new branch
        #
        create_collection(
            f"{context.scene.stree_state.new_branch}{branch_suffix}",
            bpy.data.collections[context.scene.stree_preference.collection_name]
        )

        context.scene.stree_state.current_branch = f"{context.scene.stree_state.new_branch}{branch_suffix}"
        context.scene.stree_state.new_branch = ""

        return { "FINISHED" }

