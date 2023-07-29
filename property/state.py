# -*- coding: utf-8 -*-
import bpy


def generate_branch_prop(self, context):
    preference = context.scene.stree_preference

    if bpy.data.collections.find(preference.collection_name) == -1:
        return [(preference.collection_name, "(None)", "")]

    branches = list(filter(
        lambda x: preference.branch_suffix in x,
        bpy.data.collections[preference.collection_name].children.keys()
    ))

    if len(branches) <= 0:
        return [(preference.collection_name, "(None)", "")]

    prop = []
    for branch in branches:
        prop.append((branch, branch, ""))

    return prop


def generate_snapshot_prop(self, context):
    try:
        preference = context.scene.stree_preference

        collections = list(filter(
            lambda x: not (
                preference.branch_suffix in x
                or preference.snapshot_suffix in x # noqa: W503
            ),
            bpy.data.collections.keys()
        ))

        prop = []
        for s in collections:
            prop.append((s, s, ""))

        return prop
    except Exception as e:
        print(e)
        return []


class State(bpy.types.PropertyGroup):
    #
    # branch
    #
    current_branch: bpy.props.EnumProperty(
        items=generate_branch_prop,
        description="stree branch list" # noqa: F722
    )

    new_branch: bpy.props.StringProperty(default="") # noqa: F722

    #
    # snapshot
    #
    head: bpy.props.StringProperty(default="") # noqa: F722

    revert_destination: bpy.props.EnumProperty(
        items=generate_snapshot_prop,
        description="revert objects to selected collection" # noqa: F722
    )

