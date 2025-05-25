import bpy
from bpy.types import Panel, Context, Mesh, Operator
from typing import Optional, Any, Callable
from ..config import get_tool_settings  # 导入get_tool_settings函数
from ..preference.settings import MergeToolSettings  # 使用插件根目录的绝对路径

class FaceStats(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mesh Manager"
    bl_label = "Mesh Operations"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # 添加生成网格、拖动调整和生成曲线的按钮
        layout.operator("mesh.create_hair_grid", text="Create Hair Grid", icon='GRID')
        layout.operator("mesh.drag_grid", text="Drag Grid", icon='HAND')
        layout.operator("mesh.generate_curve", text="Generate Curve", icon='CURVE_PATH')
        
        # 添加曲线参数调整
        box = layout.box()
        box.label(text="Curve Settings")
        box.prop(scene.merge_tool_settings, "curve_resolution")
        box.prop(scene.merge_tool_settings, "curve_thickness")

        tool = get_tool_settings(context)

        # 统计活动物体的面类型
        if context.object and context.object.type == 'MESH':
            mesh = context.object.data
            # 检查是否存在polygons属性且该属性不为None
            if hasattr(mesh, 'polygons') and getattr(mesh, 'polygons', None) is not None:
                polygons = mesh.polygons # type: ignore
                tri = sum(1 for p in polygons if len(p.vertices) == 3)
                quad = sum(1 for p in polygons if len(p.vertices) == 4)
                ngon = len(polygons) - tri - quad
                
                col = layout.column(align=True) if layout else None
                if col:
                    col.label(text=f"三角面: {tri}")
                    col.label(text=f"四边形: {quad}")
                    col.label(text=f"多边形面: {ngon}")
                
                # 参数设置区域
                box = layout.box() if layout else None
                if box:
                    box.label(text="合并参数:")
                    col = box.column(align=True)
                    if col:
                        col.prop(tool, "angle_face")
                        col.prop(tool, "angle_shape")
                        col.prop(tool, "cmp_seam")
                        col.prop(tool, "cmp_sharp")
                        col.prop(tool, "cmp_material")
                        col.prop(tool, "cmp_texture")
                        col.prop(tool, "cmp_vertex")
                
                # 操作按钮
                if layout:
                    layout.separator()
                    row = layout.row()
                    if row:
                        # 修改: 使用 context.object 获取当前选中的对象，并传递给操作符
                        row.operator("mesh.advanced_merge_tris", text="合并三角面", icon='MOD_TRIANGULATE')
