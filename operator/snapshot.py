import bpy
import re

from .stage             import staged_objects
from ..utils.collection import hide_collections
from ..utils.register   import dcr_register

@dcr_register
class TakeSnapshot(bpy.types.Operator):
    bl_idname      = 'stree.take_snapshot'
    bl_label       = "Take Snapshot"
    bl_description = 'Take snapshot of selected objects'

    def execute(self, context):
        # this function works only in object mode only
        if bpy.context.mode != 'OBJECT':
            return { 'CANCELLED' }

        try:
            #
            # init
            #
            if bpy.data.collections.find(context.scene.stree_preference.collection_name) == -1:
                create_new_collection(context.scene.stree_preference.collection_name, bpy.context.scene.collection)

            #
            # create snapshot collection
            #
            snapshot_name = f'{len(bpy.data.collections[context.scene.stree_preference.collection_name].children.items())}' \
                            + f'{context.scene.stree_preference.snapshot_suffix}'
            create_new_collection(snapshot_name, bpy.data.collections[context.scene.stree_preference.collection_name])

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
                object_name = re.sub(r'\.\d*$', '', object_name)
                o.name = o.data.name = snapshot_name + '.' + object_name + context.scene.stree_preference.snapshot_suffix

            hide_collections([root_collection.name, snapshot_collection.name])

            return { 'FINISHED' }
        except Exception as e:
            print(e)
            return { 'CANCELLED' }

def create_new_collection(collection_name, parent_collection):
    # create collection
    collection = bpy.data.collections.new(collection_name)

    # link collection to scene
    if parent_collection != None:
        parent_collection.children.link(collection)

def select_staged_objects():
    bpy.ops.object.select_all(action='DESELECT')

    for obj_name in staged_objects:
        if obj_name in [x for (x, _) in bpy.data.objects.items()]:
            bpy.data.objects[obj_name].select_set(True)
