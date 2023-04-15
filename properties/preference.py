import bpy

from ..utils.register import dcr_register

@dcr_register
class Preference(bpy.types.PropertyGroup):
    #
    # common
    #
    collection_name: bpy.props.StringProperty(default=".stree")
