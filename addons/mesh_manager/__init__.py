# 移除冗余导入
import bpy
from bpy.props import FloatProperty, BoolProperty
from bpy.types import Operator, PropertyGroup, Panel
from .operators.remove_duplicate_verts import RemoveDuplicateVertsOperator
from .operators.create_hair_curve import CreateHairCurveOperator
from .operators.edit_hair_curve import EditHairCurveOperator
from .operators.generate_hair_strands import GenerateHairStrandsOperator
from .operators.remove_duplicate_verts import RemoveDuplicateVertsOperator

# 插件信息
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

# 核心操作函数
def advanced_merge_tris(context):
    """执行高级三角面合并操作的主函数"""
    # 获取当前场景设置
    settings = context.scene.merge_tool_settings
    
    # 检查是否有活动对象
    if not context.active_object or context.active_object.type != 'MESH':
        return {'CANCELLED'}
    
    # 进入编辑模式
    bpy.ops.object.mode_set(mode='EDIT')
    
    # 执行合并操作（示例代码）
    # 实际应根据angle_face阈值进行智能合并
    bpy.ops.mesh.tris_convert_to_quads()
    
    # 返回物体模式
    bpy.ops.object.mode_set(mode='OBJECT')

# 参数属性组
class MergeToolSettings(bpy.types.PropertyGroup):
    """网格合并工具的参数设置组"""
    # 面间角度阈值属性
    angle_face: bpy.props.FloatProperty(
        name="面间角度阈值",
        description="最大允许的相邻面夹角（弧度）",
        default=3.14,
        min=0.01,
        max=3.14,
        subtype='ANGLE'
    )
    
    # 添加新的顶点距离阈值属性
    vert_distance: bpy.props.FloatProperty(
        name="顶点距离阈值",
        description="合并顶点的最大距离",
        default=0.001,
        min=0.0,
        max=1.0,
        subtype='DISTANCE'
    )

    # 添加缺失的属性定义
    cmp_material: bpy.props.BoolProperty(
        name="材质比较",
        description="仅合并相同材质的面",
        default=False
    )
    
    cmp_texture: bpy.props.BoolProperty(
        name="纹理比较",
        description="仅合并相同纹理坐标的面",
        default=False
    )
    
    cmp_vertex: bpy.props.BoolProperty(
        name="顶点颜色比较",
        description="仅合并相同顶点颜色的面",
        default=False
    )

# 自定义操作按钮
class AdvancedMergeTrisOperator(bpy.types.Operator):
    bl_idname = "object.advanced_merge_tris"
    bl_label = "高级三角面合并"
    bl_description = "使用增强参数控制合并三角面"
    
    def execute(self, context):
        advanced_merge_tris(context)
        return {'FINISHED'}

# 实时统计面板
class FaceStatsPanel(bpy.types.Panel):
    bl_label = "面类型统计"
    bl_idname = "VIEW3D_PT_face_stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "工具"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.merge_tool_settings
        
        # 显示参数设置
        box = layout.box()
        box.label(text="合并设置")
        box.prop(settings, "angle_face")
        box.prop(settings, "vert_distance")
        
        # 添加操作按钮
        row = layout.row()
        row.scale_y = 1.5
        row.operator("object.advanced_merge_tris", icon='AUTO')

# 注册与注销
def register():
    bpy.utils.register_class(MergeToolSettings)
    bpy.types.Scene.merge_tool_settings = bpy.props.PointerProperty(type=MergeToolSettings)
    bpy.utils.register_class(AdvancedMergeTrisOperator)
    bpy.utils.register_class(FaceStatsPanel)
    from .operators.remove_duplicate_verts import RemoveDuplicateVertsOperator
    bpy.utils.register_class(RemoveDuplicateVertsOperator)

def unregister():
    bpy.utils.unregister_class(FaceStatsPanel)
    bpy.utils.unregister_class(AdvancedMergeTrisOperator)
    del bpy.types.Scene.merge_tool_settings
    bpy.utils.unregister_class(MergeToolSettings)
    from .operators.remove_duplicate_verts import RemoveDuplicateVertsOperator
    bpy.utils.unregister_class(RemoveDuplicateVertsOperator)

if __name__ == "__main__":
    register()