import bpy
import bmesh
import os
from typing import Set, Any

class MESH_OT_CreateHairGrid(bpy.types.Operator):
    bl_idname = "mesh.create_hair_grid"
    bl_label = "Create Hair Grid"
    bl_description = "Create a hair grid based on the specified file"

    hair_type: bpy.props.EnumProperty(
        name="Hair Type",
        description="Select hair type",
        items=[
            ("LONG", "Long Hair", "Create long hair grid"),
            ("SHORT", "Short Hair", "Create short hair grid")
        ],
        default='LONG'
    )  # type: ignore

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context) -> Set[Any]:
        obj = context.object
        if obj and obj.type == 'MESH':
            me = obj.data
            if me:
                bm = bmesh.new()
                bm.from_mesh(me)  # type: ignore

                # 根据选择的头发类型生成网格
                if self.hair_type == 'LONG':
                    # 示例：生成一个球体作为长发网格
                    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=obj.location)
                    self.report({'INFO'}, "Long hair grid created.")
                elif self.hair_type == 'SHORT':
                    # 示例：生成一个立方体作为短发网格
                    bpy.ops.mesh.primitive_cube_add(size=2.0, location=obj.location)
                    self.report({'INFO'}, "Short hair grid created.")

                bm.free()

        return {'FINISHED'}  # type: ignore

    def invoke(self, context, event) -> Set[Any]:
        # 显示属性对话框
        wm = context.window_manager
        if wm:
            return wm.invoke_props_dialog(self)  # type: ignore
        return {'CANCELLED'}  # type: ignore

    def draw(self, context):
        layout = self.layout
        if layout:
            layout.prop(self, "hair_type")