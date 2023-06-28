# -*- coding: utf-8 -*-
import bpy


class Preference(bpy.types.PropertyGroup):
    #
    # common
    #
    collection_name: bpy.props.StringProperty(default=".stree") # noqa: F722

    #
    # snapshot
    #
    snapshot_suffix: bpy.props.StringProperty(default=".stree") # noqa: F722

