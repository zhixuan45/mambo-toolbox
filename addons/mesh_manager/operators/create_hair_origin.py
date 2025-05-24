import bpy

class CreateHairOriginOperator(bpy.types.Operator):
    """创建头发原点"""
    bl_idname = "object.create_hair_origin"
    bl_label = "创建头发原点"
    bl_description = "创建一个特殊标记的空对象作为头发的原点"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 创建一个新的空对象
        empty = bpy.data.objects.new("Hair_Origin", None)
        
        # 设置空对象的显示类型为轴
        empty.empty_display_type = 'AXIS'
        empty.empty_display_size = 0.5
        
        # 将空对象链接到场景集合
        bpy.context.collection.objects.link(empty)
        
        # 选择并激活空对象
        bpy.context.view_layer.objects.active = empty
        empty.select_set(True)
        
        # 添加自定义属性标记这是一个头发原点
        empty["is_hair_origin"] = True
        
        return {'FINISHED'}
