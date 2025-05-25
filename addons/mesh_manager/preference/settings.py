import bpy

class MergeToolSettings(bpy.types.PropertyGroup):
     angle_face: bpy.props.FloatProperty(
         name="面间角度阈值",
         description="最大允许的相邻面夹角（弧度）",
         default=1.57,
         min=0.01,
         max=3.14,
         subtype='ANGLE'
     )
     
     angle_shape: bpy.props.FloatProperty(
         name="形状角度阈值",
         description="四边形内角允许的最大偏差（弧度）",
         default=1.57,
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

def register():
     bpy.utils.register_class(MergeToolSettings)

def unregister():
     bpy.utils.unregister_class(MergeToolSettings)
