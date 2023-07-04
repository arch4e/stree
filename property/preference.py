# -*- coding: utf-8 -*-
import bpy


class Preference(bpy.types.PropertyGroup):
    #
    # common
    #
    collection_name: bpy.props.StringProperty(default=".stree") # noqa: F722

    #
    # branch
    #
    branch_suffix: bpy.props.StringProperty(default=".sbr") # noqa: F72

    #
    # snapshot
    #
    snapshot_suffix: bpy.props.StringProperty(default=".stree") # noqa: F722

    display_limit_is_enabled: bpy.props.BoolProperty(default=True)

    display_limit: bpy.props.IntProperty(default=10)

