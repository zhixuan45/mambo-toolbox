import bpy
import bmesh
import mathutils
from bpy.types import Operator

class RemoveDuplicateVertsOperator(Operator):
    bl_idname = "mesh.remove_duplicate_verts"
    bl_label = "合并重复顶点"
    bl_description = "自动选择并合并距离小于阈值的重复顶点"
    
    distance: bpy.props.FloatProperty(
        name="距离阈值",
        description="顶点间最大允许距离",
        default=0.0001,
        min=0.00001,
        max=1.0,
        step=0.001
    )
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
                
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            
            # 标记要删除的顶点
            verts_to_remove = set()
            for i, v1 in enumerate(bm.verts):
                for j, v2 in enumerate(bm.verts):
                    if i >= j:
                        continue
                    if (v1.co - v2.co).length < self.distance:
                        verts_to_remove.add(v2)
            
            # 合并顶点
            if verts_to_remove:
                bmesh.ops.remove_doubles(
                    bm,
                    verts=list(verts_to_remove),
                    dist=self.distance
                )
            
            bmesh.update_edit_mesh(me)
            bpy.ops.object.mode_set(mode='OBJECT')
        
        return {'FINISHED'}
