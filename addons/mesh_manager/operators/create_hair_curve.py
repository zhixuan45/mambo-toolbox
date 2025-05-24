import bpy

class CreateHairCurveOperator(bpy.types.Operator):
    bl_idname = "mesh.create_hair_curve"
    bl_label = "创建头发曲线"
    bl_description = "创建一个新的头发曲线对象"

    def execute(self, context):
        # 创建一个新的曲线数据块
        curve_data = bpy.data.curves.new(name="HairCurve", type='CURVE')
        curve_data.dimensions = '3D'

        # 创建一个新的曲线对象
        curve_object = bpy.data.objects.new("HairCurveObject", curve_data)

        # 将曲线对象链接到场景集合
        bpy.context.collection.objects.link(curve_object)

        # 选择并激活曲线对象
        bpy.context.view_layer.objects.active = curve_object
        curve_object.select_set(True)

        # 添加一个样条线到曲线数据
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(2)  # 默认添加3个点

        # 设置每个点的位置
        spline.bezier_points[0].co = (0, 0, 0)
        spline.bezier_points[1].co = (1, 0, 0)
        spline.bezier_points[2].co = (2, 0, 0)

        return {'FINISHED'}