import bpy
import json
import os

class NODE_OT_save_node_preset(bpy.types.Operator):
    bl_idname = "node.save_node_preset"
    bl_label = "保存节点预设"
    
    filepath = str(bpy.props.StringProperty(subtype='FILE_PATH'))
    
    def execute(self, context):
        node_tree = context.space_data.edit_tree
        nodes_data = {
            'nodes': [{
                'bl_idname': n.bl_idname,
                'location': list(n.location),
                'inputs': [{
                    'default_value': getattr(i, 'default_value', None),
                    'name': i.name
                } for i in n.inputs],
                'outputs': [{
                    'default_value': getattr(o, 'default_value', None),
                    'name': o.name
                } for o in n.outputs]
            } for n in node_tree.nodes]
        }
        
        with open(self.filepath, 'w') as f:
            json.dump(nodes_data, f, indent=2)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class NODE_OT_load_node_preset(bpy.types.Operator):
    bl_idname = "node.load_node_preset"
    bl_label = "加载节点预设"
    filepath = bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        node_tree = context.space_data.edit_tree
        for n in node_tree.nodes:
            node_tree.nodes.remove(n)

        with open(self.filepath, 'r') as f:
            nodes_data = json.load(f)

        for node_info in nodes_data['nodes']:
            node = node_tree.nodes.new(node_info['bl_idname'])
            node.location = node_info['location']
            
            for i, input_info in enumerate(node_info['inputs']):
                if i < len(node.inputs) and input_info['default_value'] is not None:
                    node.inputs[i].default_value = input_info['default_value']
            
            for o, output_info in enumerate(node_info['outputs']):
                if o < len(node.outputs) and output_info['default_value'] is not None:
                    node.outputs[o].default_value = output_info['default_value']

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class NODE_OT_load_builtin_preset(bpy.types.Operator):
    bl_idname = "node.load_builtin_preset"
    bl_label = "加载内置预设"

    def execute(self, context):
        #preset_name = context.scene.node_preset_items
        #preset_path = os.path.join(os.path.dirname(__file__), 'presets', preset_name + '.json')
        preset_path = os.path.join(os.path.dirname(__file__), 'presets', 'builtin_preset_1.json')
        if os.path.exists(preset_path):
            bpy.ops.node.load_node_preset(filepath=preset_path)
        return {'FINISHED'}