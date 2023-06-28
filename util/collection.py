# -*- coding: utf-8 -*-
import bpy


def hide_collections(collection_name_list):
    for c in collection_name_list:
        bpy.data.collections[c].hide_render   = True
        bpy.data.collections[c].hide_select   = True
        bpy.data.collections[c].hide_viewport = True

