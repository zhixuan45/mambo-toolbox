import bpy
from bpy.types import Panel, Context, Mesh, Operator
from typing import Optional, Any, Callable


def get_tool_settings(context: Context) -> Any:
    """临时定义工具设置获取函数"""
    # 这里应该实现实际的获取逻辑
    return context.scene

class FaceStats(Panel):
    bl_label = ""
    bl_idname = "VIEW3D_PT_face_stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "工具"
    
    def draw(self, context: Context):
        layout = self.layout
        scene = context.scene
        tool = get_tool_settings(context)

        # 添加创建头发原点的按钮
        row = layout.row() if layout else None
        if row:
            row.operator("mesh.create_hair_curve", icon='EMPTY_AXIS', text="创建头发原点")
            row.operator("mesh.search", icon='MOD_TRIANGULATE')
        
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
                        row.operator("mesh.advanced_merge_tris", icon='MOD_TRIANGULATE')
