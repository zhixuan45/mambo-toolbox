import bpy

class GenerateHairStrandsOperator(bpy.types.Operator):
    bl_idname = "mesh.generate_hair_strands"
    bl_label = "生成发丝"
    bl_description = "基于选定的曲线生成发丝"

    def execute(self, context):
        # 获取活动对象（假设为曲线对象）
        curve_obj = context.active_object

        if curve_obj and curve_obj.type == 'CURVE':
            # 在曲线对象上添加粒子系统
            bpy.ops.object.particle_system_add()

            # 获取粒子系统
            psys = curve_obj.particle_systems[0]

            # 配置粒子系统设置
            settings = psys.settings
            settings.type = 'HAIR'
            settings.count = 1000  # 发丝数量
            settings.hair_length = 1.0  # 发丝长度

            # 使用曲线作为发丝路径
            modifier = curve_obj.modifiers.new(name="CurveGuide", type='PARTICLE_SYSTEM')
            modifier.particle_system = psys

        return {'FINISHED'}