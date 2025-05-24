from ...common.types.framework import is_extension

# https://docs.blender.org/manual/en/latest/advanced/extensions/addons.html#extensions-and-namespace
# This is the unique package name of the addon, it is different from the add-on name in bl_info.
# This name is used to identify the add-on in python code. It should also be the same to the package name of the add-on.
__addon_name__ = "mesh_manager"  # 直接设置插件名称


def get_tool_settings(context):
    return context.scene.merge_tool_settings  # 确保返回MergeToolSettings实例
