import bpy
import bmesh
from typing import Set, Any

class MESH_OT_DragGrid(bpy.types.Operator):
    bl_idname = "mesh.drag_grid"
    bl_label = "Drag Grid to Generate Curve"
    bl_description = "Drag the grid points to adjust the curve"

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    last_mouse_x: float = 0.0  # 记录上一次鼠标X位置

    def modal(self, context, event) -> Set[Any]:
        if event.type == 'MOUSEMOVE':
            # 更新网格顶点位置
            obj = context.object
            if obj and obj.type == 'MESH':
                me = obj.data
                if me:
                    bm = bmesh.from_edit_mesh(me)  # type: ignore
                    
                    # 计算鼠标移动的增量
                    mouse_delta = event.mouse_x - self.last_mouse_x
                    
                    # 更新所有顶点的位置
                    for vert in bm.verts:
                        vert.co.x += mouse_delta * 0.01
                    
                    bmesh.update_edit_mesh(me)  # type: ignore
                    
                    # 记录当前鼠标位置
                    self.last_mouse_x = event.mouse_x

        elif event.type in {'LEFTMOUSE', 'RET'}:
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event) -> Set[Any]:
        wm = context.window_manager
        if wm:
            # 初始化鼠标位置
            self.last_mouse_x = event.mouse_x
            try:
                wm.modal_handler_add(self)
                return {'RUNNING_MODAL'}
            except Exception as e:
                self.report({'ERROR'}, f"Modal handler error: {e}")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(MESH_OT_DragGrid)

def unregister():
    bpy.utils.unregister_class(MESH_OT_DragGrid)