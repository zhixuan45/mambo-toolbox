from typing import Optional, Union
import bpy
import bmesh
from mathutils import Vector, geometry
from bpy.types import Operator, Context

# 导入MergeToolSettings类
from ..properties import MergeToolSettings

# 定义 OperatorReturnItems 类型
OperatorReturnItems = str

class MESH_OT_AdvancedMergeTris(Operator):
    bl_idname = "mesh.advanced_merge_tris"
    bl_label = "高级三角面合并"
    bl_description = "使用增强参数控制合并三角面"
    
    # 新增属性：use_selected，用于标识是否使用选中的对象
    use_selected: bpy.props.BoolProperty(default=False)
    
    @classmethod
    def poll(cls, context: Context) -> bool:
        # 检查是否有激活对象且类型为MESH
        return context.object is not None and context.object.type == 'MESH'
    
    def execute(self, context: Context) -> set[str]:
        result = {'FINISHED'}
        
        tool = getattr(context.scene, 'merge_tool_settings', None)
        if tool is None:
            self.report({'ERROR'}, "Merge tool settings not found")
            return {'CANCELLED'}
        
        # 修改: 使用 context.object 获取当前选中的对象
        obj = context.object
        
        if obj and obj.type == 'MESH':
            try:
                # 检查对象是否有数据
                if not obj.data or not isinstance(obj.data, bpy.types.Mesh):
                    self.report({'ERROR'}, "对象没有有效的网格数据")
                    return {'CANCELLED'}
                
                # 切换到编辑模式
                if context.object.mode != 'EDIT':
                    bpy.ops.object.mode_set(mode='EDIT')
                
                # 强制更新网格数据
                bpy.ops.object.editmode_toggle()
                bpy.ops.object.editmode_toggle()
                
                me = obj.data
                if isinstance(me, bpy.types.Mesh):
                    bm = bmesh.from_edit_mesh(me) if me else None
                else:
                    self.report({'ERROR'}, "Invalid mesh data")
                    return {'CANCELLED'}
                
                if not bm:
                    self.report({'ERROR'}, "BMesh creation failed")
                    return {'CANCELLED'}
                
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
                        cmp_uvs=tool.cmp_texture,
                        cmp_vcols=tool.cmp_vertex,
                        cmp_materials=tool.cmp_material
                    )
                    self.report({'INFO'}, f"成功合并 {obj.name} 的三角面")
                except Exception as e:
                    self.report({'ERROR'}, f"处理 {obj.name} 时发生错误: {e}")
                    result = {'CANCELLED'}
                
                # 更新编辑网格
                bmesh.update_edit_mesh(me)
                
                # 确保退出编辑模式
                if context.object.mode == 'EDIT':
                    bpy.ops.object.mode_set(mode='OBJECT')
            
            except Exception as e:
                self.report({'ERROR'}, f"执行合并操作时发生意外错误: {e}")
                result = {'CANCELLED'}
        
        else:
            self.report({'ERROR'}, "请选择一个网格对象")
            return {'CANCELLED'}
        
        # 添加完成提示
        self.report({'INFO'}, "三角面合并完成")
        
        return result