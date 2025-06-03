import bpy
import json
import os
from ..__init__ import dir_init_main, dir_presets

from ..config import __addon_name__
from ..preference.AddonPreferences import ExampleAddonPreferences

class NODE_OT_save_node_preset(bpy.types.Operator):
    bl_idname = "node.save_node_preset"
    bl_label = "保存节点预设"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')  # type: ignore

    def execute(self, context):
        try:
            space_data = context.space_data
            if not hasattr(space_data, 'edit_tree') or space_data.edit_tree is None:
                self.report({'ERROR'}, "无效的编辑树")
                return {'CANCELLED'}
            node_tree = space_data.edit_tree  # type: ignore
            
            def convert_blender_data(value):
                """统一处理Blender数据类型转换"""
                if hasattr(value, '__iter__'):
                    return [float(v) for v in value]  # 处理Vector/Color等可迭代类型
                try:
                    return float(value)  # 处理普通数值
                except (TypeError, ValueError):
                    return str(value)  # 其他类型转为字符串
        
            # 为每个节点添加序号
            nodes_data = {
                'nodes': [],
                'links': []
            }
            node_name_map = {}  # 新增节点名称到索引的映射表

            for index, n in enumerate(node_tree.nodes):
                node_info = {
                    'index': index,
                    'bl_idname': n.bl_idname,
                    'name': n.name,
                    'location': [float(x) for x in n.location],
                    'inputs': [{
                        'default_value': convert_blender_data(getattr(i, 'default_value', None)),
                        'name': i.name
                    } for i in n.inputs],
                    'outputs': [{
                        'default_value': convert_blender_data(getattr(o, 'default_value', None)),
                        'name': o.name
                    } for o in n.outputs]
                }
            
                # 特殊处理 NodeFrame 和 NodeReroute 类型的节点
                if n.bl_idname == 'NodeFrame':
                    node_info['label'] = n.label  # 保存帧标签
                elif n.bl_idname == 'NodeReroute':
                    node_info['is_reroute'] = True  # 标记为转接点
                
                node_name_map[n.name] = index  # 记录节点名称到索引的映射
                nodes_data['nodes'].append(node_info)

                # 重构节点连接保存逻辑（支持转接点）
                for link in node_tree.links:
                    from_node = link.from_node
                    to_node = link.to_node
                    from_index = node_name_map.get(from_node.name, -1)
                    to_index = node_name_map.get(to_node.name, -1)
                    if from_index != -1 and to_index != -1:  # 仅保存有效连接
                        # 处理转接点输入输出的特殊连接方式
                        from_socket = link.from_socket.identifier
                        to_socket = link.to_socket.identifier
                                    
                        # 如果是转接点输出，记录所有输出连接
                        nodes_data['links'].append({
                            'from_index': from_index,
                            'from_socket': from_socket,
                            'to_index': to_index,
                            'to_socket': to_socket,
                            'is_reroute': from_node.bl_idname == 'NodeReroute' or to_node.bl_idname == 'NodeReroute'
                        })

            with open(self.filepath, 'w') as f:
                json.dump(nodes_data, f, indent=2)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"保存预设失败: {str(e)}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        if not hasattr(context.window_manager, 'fileselect_add'):
            self.report({'ERROR'}, "文件选择器不可用")
            return {'CANCELLED'}
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class NODE_OT_load_node_preset(bpy.types.Operator):
    bl_idname = "node.load_node_preset"
    bl_label = "加载节点预设"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH') # type: ignore

    def execute(self, context):
        try:
            node_tree = context.space_data.edit_tree
            # 仅清除当前插件创建的节点，保留其他插件节点
            for node in list(node_tree.nodes):
                if node.bl_idname.startswith('NODE_'):
                    node_tree.nodes.remove(node)
            
            with open(self.filepath, 'r') as f:
                nodes_data = json.load(f)
            
            # 加载节点数据
            node_instances = []  # 新增节点实例数组
            for node_info in nodes_data['nodes']:
                node = node_tree.nodes.new(node_info['bl_idname'])
                node.name = node_info['name']
                node.location = node_info['location']
                
                # 特殊处理 NodeFrame 类型的节点
                if node.bl_idname == 'NodeFrame':
                    node.label = node_info.get('label', '')  # 设置帧标签
                
                node_instances.append(node)  # 按索引顺序保存节点

                # 处理输入值
                for i, input_info in enumerate(node_info.get('inputs', [])):
                    if i < len(node.inputs) and input_info['default_value'] is not None:
                        try:
                            val = input_info['default_value']
                            if isinstance(val, list):
                                node.inputs[i].default_value = tuple(val)
                            else:
                                node.inputs[i].default_value = float(val)
                        except Exception as e:
                            print(f"输入值设置失败：{node.name}.{i} - {str(e)}")
                
                # 处理输出值
                for o, output_info in enumerate(node_info.get('outputs', [])):
                    if o < len(node.outputs):
                        try:
                            val = output_info.get('default_value', [])
                            node.outputs[o].default_value = val if isinstance(val, float) else tuple(val)
                        except Exception as e:
                            print(f"输出值设置失败：{node.name}.{o} - {str(e)}")

            # 重构节点连接恢复逻辑（支持转接点）
            for link_info in nodes_data.get('links', []):
                from_index = link_info['from_index']
                to_index = link_info['to_index']
                if from_index < len(node_instances) and to_index < len(node_instances):
                    from_node = node_instances[from_index]
                    to_node = node_instances[to_index]
                    
                    # 处理转接点连接的特殊逻辑
                    try:
                        from_socket = next(s for s in from_node.outputs if s.identifier == link_info['from_socket'])
                        to_socket = next(s for s in to_node.inputs if s.identifier == link_info['to_socket'])
                        
                        # 如果是转接点连接，确保正确处理单输入多输出
                        node_tree.links.new(to_socket, from_socket)
                    except StopIteration:
                        print(f"找不到对应socket: {from_node.name} -> {to_node.name}")
        except Exception as e:
            self.report({'ERROR'}, f"加载预设失败: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}  # type: ignore

    def invoke(self, context, event):
        wm = context.window_manager
        if wm is None or not hasattr(wm, 'fileselect_add'):
            self.report({'ERROR'}, "文件选择器不可用")
            return {'CANCELLED'}  # type: ignore
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}  # type: ignore

class NODE_OT_load_builtin_preset(bpy.types.Operator):
    bl_idname = "node.load_builtin_preset"
    bl_label = "加载内置预设"
    preset_name: bpy.props.StringProperty() # type: ignore

    def execute(self, context):
        preset_name = self.preset_name
        preset_path = os.path.join(dir_presets, f"builtin_preset_{preset_name}.json")
        if os.path.exists(preset_path):
            print(f"加载内置预设：{preset_name}")
            # 直接调用 load_node_preset 操作符，不传递 filepath
            bpy.ops.node.load_node_preset(filepath=preset_path)
        return {'FINISHED'}