# 初始化文件，启用子模块导入

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

# 移除冗余导入
import bpy
bl_info = {
    "name": "曼波工具箱-网格修改器",
    "author": "zhixuan45",
    "blender": (3, 5, 0),
    "version": (0, 0, 1),
    "description": "整理网格用",
    "warning": "",
    "doc_url": "https://github.com/zhixuan45/node_preset_manager",
    "tracker_url": "https://github.com/zhixuan45/node_preset_manager/issues",
    "support": "COMMUNITY",
    "category": "3D View"
}

import os
import sys
from .properties import MergeToolSettings
from .panels import FaceStatsPanel
from .operators import AdvancedMergeTrisOperator
# 获取当前插件目录并添加到 sys.path
plugin_dir = os.path.dirname(os.path.realpath(__file__))
if plugin_dir not in sys.path:
    sys.path.append(plugin_dir)

# 移除冗余导入


# 注册与注销
def register():

    
    bpy.utils.register_class(MergeToolSettings)
    bpy.types.Scene.merge_tool_settings = bpy.props.PointerProperty(type=MergeToolSettings)  # type: ignore[attr-defined]
    bpy.utils.register_class(AdvancedMergeTrisOperator)
    bpy.utils.register_class(FaceStatsPanel)

    # 注册依赖的操作符
    from .operators.remove_duplicate_verts import RemoveDuplicateVertsOperator  # pyright: ignore[reportMissingImports]
    bpy.utils.register_class(RemoveDuplicateVertsOperator)


def unregister():
    bpy.utils.unregister_class(FaceStatsPanel)
    bpy.utils.unregister_class(AdvancedMergeTrisOperator)
    
    from .operators.remove_duplicate_verts import RemoveDuplicateVertsOperator  # pyright: ignore[reportMissingImports]
    bpy.utils.unregister_class(RemoveDuplicateVertsOperator)

if __name__ == "__main__":
    register()