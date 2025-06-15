
import bpy

bl_info = {
    "name": "菌菌阻尼追踪器",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "视图3D > 工具架 > 菌菌阻尼追踪器",
    "description": "为选中的骨骼生成阻尼追踪约束并控制参数",
    "category": "绑定",
}


class GenerateDampingTrack(bpy.types.Operator):
    """为选中的骨骼生成阻尼追踪约束"""
    bl_idname = "rig.generate_damping_track"
    bl_label = "生成阻尼追踪"

    def execute(self, context):
        armature = context.active_object
        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, "活动对象不是骨骼对象。")
            return {'CANCELLED'}

        # 获取选中的骨骼，并按它们在世界空间中的Z轴坐标排序
        selected_bones = [bone for bone in armature.pose.bones if bone.bone.select]
        selected_bones.sort(key=lambda bone: bone.head[2])

        # 解锁选中骨骼的位置和旋转锁定属性
        for bone in selected_bones:
            bone.lock_location = [False, False, False]
            bone.lock_rotation = [False, False, False]

        for i in range(len(selected_bones) - 1):
            constraint = selected_bones[i + 1].constraints.new(type='DAMPED_TRACK')
            constraint.target = armature
            constraint.subtarget = selected_bones[i].name
            constraint.influence = 0.5  # 设置默认影响力为 0.5
            constraint.track_axis = 'TRACK_Y'  # 默认追踪轴

        return {'FINISHED'}


class ControlDampingTrackParams(bpy.types.Operator):
    """控制选中骨骼的阻尼追踪参数"""
    bl_idname = "rig.control_damping_track_params"
    bl_label = "控制阻尼追踪参数"

    influence: bpy.props.FloatProperty(name="影响力", default=0.5, min=0.0, max=1.0)
    track_axis: bpy.props.EnumProperty(
        name="追踪轴",
        items=[
            ('TRACK_X', "X轴", ""),
            ('TRACK_Y', "Y轴", ""),
            ('TRACK_Z', "Z轴", ""),
            ('TRACK_NEGATIVE_X', "-X轴", ""),
            ('TRACK_NEGATIVE_Y', "-Y轴", ""),
            ('TRACK_NEGATIVE_Z', "-Z轴", ""),
        ],
        default='TRACK_Y'
    )

    def execute(self, context):
        armature = context.active_object
        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, "活动对象不是骨骼对象。")
            return {'CANCELLED'}

        bones = [bone for bone in armature.pose.bones if bone.bone.select]
        for bone in bones:
            for constraint in bone.constraints:
                if constraint.type == 'DAMPED_TRACK':
                    constraint.influence = self.influence
                    constraint.track_axis = self.track_axis

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class ClearDampingTrack(bpy.types.Operator):
    """清除选中骨骼的阻尼追踪约束"""
    bl_idname = "rig.clear_damping_track"
    bl_label = "清除阻尼追踪"

    def execute(self, context):
        armature = context.active_object
        if armature.type != 'ARMATURE':
            self.report({'ERROR'}, "活动对象不是骨骼对象。")
            return {'CANCELLED'}

        bones = [bone for bone in armature.pose.bones if bone.bone.select]
        for bone in bones:
            for constraint in bone.constraints:
                if constraint.type == 'DAMPED_TRACK':
                    bone.constraints.remove(constraint)

        return {'FINISHED'}


class HairPhysicsPanel(bpy.types.Panel):
    """在3D视图工具架中创建一个面板"""
    bl_label = "菌菌阻尼追踪器"
    bl_idname = "VIEW3D_PT_hair_physics"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "菌菌阻尼追踪器"

    def draw(self, context):
        layout = self.layout
        # 设置面板标题样式
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text="菌菌阻尼追踪器", icon='CONSTRAINT_BONE')

        # 分割线
        layout.separator()

        # 按钮容器
        button_box = layout.box()
        button_box.alignment = 'CENTER'
        button_box.operator("rig.generate_damping_track", icon='CONSTRAINT_BONE')
        button_box.operator("rig.control_damping_track_params", icon='PREFERENCES')
        button_box.operator("rig.clear_damping_track", icon='X')  # 新增清除按钮

        # 添加防盗文字
        layout.separator()
        layout.alignment = 'CENTER'
        layout.label(text="除菌菌菌Well制作")


def register():
    bpy.utils.register_class(GenerateDampingTrack)
    bpy.utils.register_class(ControlDampingTrackParams)
    bpy.utils.register_class(ClearDampingTrack)  # 注册新类
    bpy.utils.register_class(HairPhysicsPanel)


def unregister():
    bpy.utils.unregister_class(GenerateDampingTrack)
    bpy.utils.unregister_class(ControlDampingTrackParams)
    bpy.utils.unregister_class(ClearDampingTrack)  # 注销新类
    bpy.utils.unregister_class(HairPhysicsPanel)


if __name__ == "__main__":
    register()

