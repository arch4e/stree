import bpy

from ..utils.register import dcr_register

@dcr_register
class State(bpy.types.PropertyGroup):
    head: bpy.props.StringProperty(default="")
