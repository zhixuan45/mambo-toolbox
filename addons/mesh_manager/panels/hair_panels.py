#写一个创建头发原点的按钮面板

import bpy
from bpy.types import Panel
from ..operators.create_hair_curve import CreateHairCurveOperator

class HairTools(Panel):
    bl_label = "头发工具"
    bl_idname = "VIEW3D_PT_hair_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "头发工具"

    def draw(self, context):
        layout = self.layout

        # 添加创建头发原点的按钮
        row = layout.row() if layout else None
        row.operator("mesh.create_hair_curve", icon='EMPTY_AXIS', text="创建头发原点")
