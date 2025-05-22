import bpy
import bmesh
from bpy.types import Operator, Panel

bl_info = {
    "name": "网格修改器",
    "author": "zhixuan45",
    "blender": (3, 5, 0),
    "version": (0, 0, 1),
    "description": "整理网格用",
    "warning": "",
    "doc_url": "https://github.com/zhixuan45/node_preset_manager",
    "tracker_url": "https://github.com/zhixuan45/node_preset_manager/issues",
    "support": "COMMUNITY",
    "category": "3D View"
}

# --------------------------
# 核心操作函数
# --------------------------
def advanced_merge_tris(context):
    scene = context.scene
    tool = scene.merge_tool_settings
    
    for obj in context.selected_objects:
        if obj.type != 'MESH':
            continue
            
        # 切换到编辑模式
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        # 获取所有三角面
        faces = [f for f in bm.faces if len(f.verts) == 3]
        
        # 执行内置算法
        try:
            bmesh.ops.join_triangles(
                bm,
                faces=faces,
                angle_face_threshold=tool.angle_face,
                angle_shape_threshold=tool.angle_shape,
                cmp_seam=tool.cmp_seam,
                cmp_sharp=tool.cmp_sharp,

            )
        except Exception as e:
            print(f"处理 {obj.name} 时出错: {e}")
        
        bmesh.update_edit_mesh(me)
    
    # 返回物体模式
    bpy.ops.object.mode_set(mode='OBJECT')

# --------------------------
# 参数属性组
# --------------------------
class MergeToolSettings(bpy.types.PropertyGroup):
    angle_face: bpy.props.FloatProperty(
        name="面间角度阈值",
        description="最大允许的相邻面夹角（弧度）",
        default=3.14,
        min=0.01,
        max=3.14,
        subtype='ANGLE'
    )
    
    angle_shape: bpy.props.FloatProperty(
        name="形状角度阈值",
        description="四边形内角允许的最大偏差（弧度）",
        default=3.14,
        min=0.01,
        max=3.14,
        subtype='ANGLE'
    )
    
    cmp_seam: bpy.props.BoolProperty(
        name="缝合线比较",
        description="仅合并共享缝合线的面",
        default=False
    )
    
    cmp_sharp: bpy.props.BoolProperty(
        name="锐边比较",
        description="仅合并共享锐边的面",
        default=False
    )
    

# --------------------------
# 自定义操作按钮
# --------------------------
class AdvancedMergeTrisOperator(Operator):
    bl_idname = "object.advanced_merge_tris"
    bl_label = "高级三角面合并"
    bl_description = "使用增强参数控制合并三角面"
    
    def execute(self, context):
        advanced_merge_tris(context)
        return {'FINISHED'}

# --------------------------
# 实时统计面板
# --------------------------
class FaceStatsPanel(Panel):
    bl_label = "面类型统计"
    bl_idname = "VIEW3D_PT_face_stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "工具"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.merge_tool_settings
        
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
            row.operator("object.advanced_merge_tris", icon='MOD_TRIANGULATE')

# --------------------------
# 注册与注销
# --------------------------
def register():
    bpy.utils.register_class(MergeToolSettings)
    bpy.types.Scene.merge_tool_settings = bpy.props.PointerProperty(type=MergeToolSettings)
    bpy.utils.register_class(AdvancedMergeTrisOperator)
    bpy.utils.register_class(FaceStatsPanel)

def unregister():
    bpy.utils.unregister_class(FaceStatsPanel)
    bpy.utils.unregister_class(AdvancedMergeTrisOperator)
    del bpy.types.Scene.merge_tool_settings
    bpy.utils.unregister_class(MergeToolSettings)

if __name__ == "__main__":
    register()