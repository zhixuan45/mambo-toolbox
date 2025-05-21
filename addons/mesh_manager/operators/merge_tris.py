import bpy
import bmesh
from mathutils import Vector, geometry
from bpy.types import Operator
from ..config import get_tool_settings

class MESH_OT_AdvancedMergeTris(Operator):
    bl_idname = "mesh.advanced_merge_tris"
    bl_label = "高级三角面合并"
    bl_description = "使用增强参数控制合并三角面"
    
    def execute(self, context):
        tool = get_tool_settings(context)
        
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
                    cmp_material=tool.cmp_material,
                    cmp_texture=tool.cmp_texture,
                    cmp_vertex=tool.cmp_vertex
                )
            except Exception as e:
                print(f"处理 {obj.name} 时