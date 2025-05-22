import bpy

from .config import __addon_name__
from .i18n.dictionary import dictionary
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

from .preference.settings import MergeToolSettings
from .panels.face_stats import VIEW3D_PT_FaceStats
from .operators.merge_tris import MESH_OT_AdvancedMergeTris
from core import *

# Add-on info
bl_info = {
    "name": "网格修改器",
    "author": "zhixuan45",
    "blender": (3, 5, 0),
    "version": (0, 0, 1),
    "description": "This is a template for building addons",
    "warning": "",
    "doc_url": "[documentation url]",
    "tracker_url": "[contact email]",
    "support": "COMMUNITY",
    "category": "3D View"
}

_addon_properties = {}


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
    #auto_load.init()
    #auto_load.register()
    bpy.utils.register_class(MergeToolSettings)
    bpy.types.Scene.merge_tool_settings = bpy.props.PointerProperty(type=MergeToolSettings)
    bpy.utils.register_class(AdvancedMergeTrisOperator)
    bpy.utils.register_class(FaceStatsPanel)
    # Manually register classes not handled by auto_load

    
    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    #auto_load.unregister()
    bpy.utils.unregister_class(FaceStatsPanel)
    bpy.utils.unregister_class(AdvancedMergeTrisOperator)
    del bpy.types.Scene.merge_tool_settings
    bpy.utils.unregister_class(MergeToolSettings)

    # Manually unregister classes


    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))

