# -*- coding: utf-8 -*-
import bpy


def generate_snapshot_prop(self, context):
    try:
        snapshot_list = [
            c for c in bpy.data.collections.keys()
            if not (context.scene.stree_preference.collection_name in c)
        ]

        prop = []
        for s in snapshot_list:
            prop.append((s, s, ""))

        return prop
    except Exception as e:
        print(e)
        return []


class State(bpy.types.PropertyGroup):
    head: bpy.props.StringProperty(default="") # noqa: F722

    revert_destination: bpy.props.EnumProperty(
        items=generate_snapshot_prop,
        description="revert objects to selected collection" # noqa: F722
    )

