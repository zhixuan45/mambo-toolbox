import bpy
import os

from .config import __addon_name__
from .i18n.dictionary import dictionary
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary
from bpy.props import *

# Add-on info
bl_info = {
    "name": "节点预设管理",
    "author": "zhixuan45",
    "blender": (3, 5, 0),
    "version": (1, 0, 0),
    "description": "节点预设保存与加载功能",
    "warning": "",
    "doc_url": "https://github.com/zhixuan45/node_preset_manager",
    "tracker_url": "https://github.com/zhixuan45/node_preset_manager/issues",
    "support": "COMMUNITY",
    "category": "Node"
}

_addon_properties = {
    bpy.types.Scene: {
        "name": StringProperty(name="预设名称"),
        "nodes_data": StringProperty(name="节点数据"),

        "node_preset_items": IntProperty(name="节点预设项"),
    },
}

dir_init_main = os.path.dirname(os.path.abspath(__file__))
dir_presets = os.path.join(dir_init_main, "presets")

# You may declare properties like following, framework will automatically add and remove them.
# Do not define your own property group class in the __init__.py file. Define it in a separate file and import it here.
# 注意不要在__init__.py文件中自定义PropertyGroup类。请在单独的文件中定义它们并在此处导入。
# _addon_properties = {
#     bpy.types.Scene: {
#         "property_name": bpy.props.StringProperty(name="property_name"),
#     },
# }

def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)

    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    auto_load.unregister()
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))
