# -*- coding: utf-8 -*-
import bpy


def change_parent_collection(src_collection, dst_collection, tgt_collection):
    src_collection.children.unlink(tgt_collection)
    dst_collection.children.link(tgt_collection)


def create_collection(collection_name, parent_collection):
    # create collection
    collection = bpy.data.collections.new(collection_name)

    # link collection to scene
    if parent_collection is not None:
        parent_collection.children.link(collection)


def hide_collections(collection_name_list):
    for c in collection_name_list:
        bpy.data.collections[c].hide_render   = True
        bpy.data.collections[c].hide_select   = True
        bpy.data.collections[c].hide_viewport = True

