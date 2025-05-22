import bpy
from bpy.types import Panel
from ..config import get_tool_settings

class VIEW3D_PT_FaceStats(Panel):
    bl_label = "面类型统计"
    bl_idname = "VIEW3D_PT_face_stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "工具"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = get_tool_settings(context)
        
        # 统计活动物体的面类型
        if context.object and context.object.type == 'MESH':
            mesh = context.object.data
            tri = sum(1 for p in mesh.polygons if len(p.vertices) == 3)
            quad = sum(1 for p in mesh.polygons if len(p.vertices) == 4)
            ngon = len(mesh.polygons) - tri - quad
            
            col = layout.column(align=True)
            col.label(text=f"三角面: {tri}")
            col.label(text=f"四边形: {quad}")
            col.label(text=f"多边形面: {ngon}")
            
            # 参数设置区域
            box = layout.box()
            box.label(text="合并参数:")
            col = box.column(align=True)
            col.prop(tool, "angle_face")
            col.prop(tool, "angle_shape")
            col.prop(tool, "cmp_seam")
            col.prop(tool, "cmp_sharp")
            col.prop(tool, "cmp_material")
            col.prop(tool, "cmp_texture")
            col.prop(tool, "cmp_vertex")
            
            # 操作按钮
            layout.separator()
            row = layout.row()
            row.operator("mesh.advanced_merge_tris", icon='MOD_TRIANGULATE')