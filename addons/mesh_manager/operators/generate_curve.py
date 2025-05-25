import bpy
import bmesh
from typing import Set, Any

class MESH_OT_GenerateCurve(bpy.types.Operator):
    bl_idname = "mesh.generate_curve"
    bl_label = "Generate Hair Curve"
    bl_description = "Generate hair curve based on the adjusted grid"

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.type == 'MESH'

    def execute(self, context) -> Set[Any]:
        obj = context.object
        if obj and obj.type == 'MESH':
            me = obj.data
            if me:
                bm = bmesh.from_edit_mesh(me)  # type: ignore

                # 根据网格顶点位置生成曲线
                curve_data = bpy.data.curves.new(name="HairCurve", type='CURVE')
                curve_data.dimensions = '3D'
                spline = curve_data.splines.new(type='BEZIER')
                spline.bezier_points.add(len(bm.verts) - 1)

                for i, vert in enumerate(bm.verts):
                    spline.bezier_points[i].co = vert.co

                curve_obj = bpy.data.objects.new("HairCurve", curve_data)
                if context.collection:
                    context.collection.objects.link(curve_obj)  # type: ignore

                self.report({'INFO'}, "Hair curve generated.")

        return {'FINISHED'}  # type: ignore

def register():
    bpy.utils.register_class(MESH_OT_GenerateCurve)

def unregister():
    bpy.utils.unregister_class(MESH_OT_GenerateCurve)