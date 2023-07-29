# -*- coding: utf-8 -*-
import bpy

from .common import BasePanel


class SnapshotPanel(BasePanel, bpy.types.Panel):
    bl_idname  = "VIEW3D_PT_stree_snapshot"
    bl_label   = "Snapshot"
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        if bpy.data.collections.find(context.scene.stree_preference.collection_name) != -1:
            # +---layout -----------+
            # | ss_area | ctrl_area |
            # +---------------------+
            layout    = self.layout.row()
            ss_area   = layout.column()
            ctrl_area = layout.column()

            #
            # revert direction selecter
            #
            ss_area.prop(context.scene.stree_state, "revert_destination", text="dest")

            #
            # snapshot list
            #
            row = ss_area.row()
            row.prop(context.scene.stree_preference, "display_limit_is_enabled", text="")
            row.prop(context.scene.stree_preference, "display_limit", text="Display Limit")

            box = ss_area.box().column(align=True)
            row = box.row()
            row.alignment = "LEFT"
            row.operator("stree.view_snapshot",
                         icon="RADIOBUT_ON" if context.scene.stree_state.head == "" else "RADIOBUT_OFF",
                         text="working area",
                         emboss=False).focus = ""

            if context.scene.stree_preference.display_limit_is_enabled:
                snapshots = get_snapshot_list(
                    list(reversed(
                        bpy.data.collections[context.scene.stree_state.current_branch].children.keys()
                    ))
                )
            else:
                snapshots = list(reversed(
                    bpy.data.collections[context.scene.stree_state.current_branch].children.keys()
                ))

            for c in snapshots:
                row = box.row(align=True)
                row.operator("stree.view_snapshot",
                             icon="RADIOBUT_ON" if c == context.scene.stree_state.head else "RADIOBUT_OFF",
                             text=f"{c}",
                             emboss=False).focus = c

                # allow deleting snapshots only while viewing the working area,
                # since deleting a snapshot while viewing will cause a head reference error
                if context.scene.stree_state.head == "":
                    row.operator("stree.delete_snapshot", icon="TRASH", text="").target = c

            #
            # control button
            #
            ctrl_area.operator("stree.revert_objects", # revert
                               icon="LOOP_BACK",
                               text="",
                               emboss=False)
            ctrl_area.operator("stree.view_snapshot", # back to workarea
                               icon="CHECKMARK",
                               text="",
                               emboss=False).focus = ""
            ctrl_area.operator("stree.shift_focus", # increment head
                               icon="TRIA_UP",
                               text="",
                               emboss=False).direction = "NEW"
            ctrl_area.operator("stree.shift_focus", # decrement head
                               icon="TRIA_DOWN",
                               text="",
                               emboss=False).direction = "OLD"


def get_snapshot_list(snapshots):
    scene         = bpy.context.scene
    display_limit = scene.stree_preference.display_limit
    offset        = display_limit // 2

    # calc display index
    if scene.stree_state.head == '':
        display_start = 0
        display_end   = display_limit
    else:
        head_index    = snapshots.index(scene.stree_state.head)

        display_start = head_index - offset
        display_end   = head_index + offset + (display_limit % 2)

        # when the number displayed is even, the index is shifted by 1
        if (display_limit % 2) == 0:
            display_start += 1
            display_end   += 1

        # adjustment of list edges
        if display_start > len(snapshots) - display_limit:
            display_start = len(snapshots) - display_limit
        elif display_end < display_limit:
            display_end = display_limit

    # indexes larger than the length are automatically modified,
    # but negative values are overwritten with 0 because they are meaningful
    display_start = display_start if display_start > 0 else 0

    return snapshots[int(display_start):int(display_end)]

