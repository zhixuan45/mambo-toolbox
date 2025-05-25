# 新增代码
# properties.py 文件内容
import bpy

class MergeToolSettings(bpy.types.PropertyGroup):
    """合并工具设置类，用于存储插件的配置选项"""
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
    
    curve_resolution: bpy.props.IntProperty(
        name="曲线分辨率",
        description="生成曲线的分辨率",
        default=10,
        min=1,
        max=100
    )
    
    curve_thickness: bpy.props.FloatProperty(
        name="曲线厚度",
        description="生成曲线的厚度",
        default=0.1,
        min=0.01,
        max=1.0
    )

    
