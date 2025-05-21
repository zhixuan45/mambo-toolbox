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
    auto_load.init()
    auto_load.register()
    
    # Manually register classes not handled by auto_load
    bpy.utils.register_class(ExampleOperator)
    bpy.utils.register_class(MergeTrisSettings)
    bpy.utils.register_class(MESH_OT_merge_excess_edges)
    bpy.utils.register_class(MESH_OT_merge_tris)
    bpy.utils.register_class(ExampleAddonPreferences)
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
    
    # Manually unregister classes
    bpy.utils.unregister_class(ExampleOperator)
    bpy.utils.unregister_class(MergeTrisSettings)
    bpy.utils.unregister_class(MESH_OT_merge_excess_edges)
    bpy.utils.unregister_class(MESH_OT_merge_tris)
    bpy.utils.unregister_class(ExampleAddonPreferences)
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))
