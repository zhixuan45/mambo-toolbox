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
                # 处理None值
                if value is None:
                    return 0.0
                
                # 特殊处理Vector/Euler/Color等特殊类型
                if 'bpy.types' in str(type(value)):
                    try:
                        # 特殊处理Vector类型
                        if 'Vector' in str(type(value)):
                            return [float(v) for v in value[:]]
                        # 特殊处理Euler类型
                        elif 'Euler' in str(type(value)):
                            return [float(v) for v in value.to_quaternion()]
                        # 特殊处理Color类型
                        elif 'Color' in str(type(value)):
                            return [float(v) for v in value[:]] + [1.0]  # 强制扩展为RGBA四元组
                        # 其他bpy类型使用to_tuple
                        return [float(v) for v in value.to_tuple()]
                    except (TypeError, ValueError, AttributeError):
                        return str(value)
                
                # 处理布尔值
                if isinstance(value, bool):
                    return int(value)
                
                # 处理字符串类型
                if isinstance(value, str):
                    return value
                
                # 处理普通数值
                try:
                    return float(value)
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

                # 修改节点属性设置部分
                for i, input_info in enumerate(node_info.get('inputs', [])):
                    if i < len(node.inputs):
                        input_socket = node.inputs[i]
                        val = input_info['default_value']
                        
                        # 特殊处理不同类型的socket
                        try:
                            if 'NodeSocketVector' in str(type(input_socket)):
                                # 强制转换为Vector类型
                                if isinstance(val, list) and len(val) >= 3:
                                    input_socket.default_value = (val[0], val[1], val[2])
                                else:
                                    f_val = float(val) if not isinstance(val, str) else 0.0
                                    input_socket.default_value = (f_val, f_val, f_val)
                            elif 'NodeSocketColor' in str(type(input_socket)):
                                # 强制转换为Color类型（四元组）
                                if isinstance(val, list):
                                    if len(val) >= 4:
                                        input_socket.default_value = (val[0], val[1], val[2], val[3])
                                    elif len(val) >= 3:
                                        input_socket.default_value = (val[0], val[1], val[2], 1.0)
                                    elif len(val) >= 1:
                                        f_val = float(val[0]) if not isinstance(val[0], str) else 0.0
                                        input_socket.default_value = (f_val, f_val, f_val, 1.0)
                                else:
                                    f_val = float(val) if not isinstance(val, str) else 0.0
                                    input_socket.default_value = (f_val, f_val, f_val, 1.0)
                            elif 'ShaderNodeGroup' in input_socket.node.bl_idname:
                                # 特殊处理节点组socket
                                if isinstance(val, list) and len(val) >= 1:
                                    # 尝试匹配节点组的socket标识符
                                    group_node = input_socket.node
                                    for group_input in group_node.inputs:
                                        if group_input.identifier == input_socket.identifier:
                                            group_input.default_value = float(val[0]) if not isinstance(val[0], str) else 0.0
                                            break
                            else:
                                # 特殊处理节点组输入
                                if 'ShaderNodeGroup' in input_socket.node.bl_idname:
                                    group_node = input_socket.node
                                    for group_input in group_node.inputs:
                                        if group_input.identifier == input_socket.identifier:
                                            if hasattr(group_input, 'default_value'):
                                                if isinstance(val, list) and len(val) >= 1:
                                                    try:
                                                        group_input.default_value = [float(v) if not isinstance(v, str) else 0.0 for v in val[:len(group_input.default_value)]]
                                                    except:
                                                        group_input.default_value = float(val[0]) if not isinstance(val[0], str) else 0.0
                                                break
                                else:
                                    # 默认处理数值类型
                                    if not isinstance(val, str):
                                        input_socket.default_value = float(val)
                        except Exception as e:
                            print(f"输入值设置失败：{node.name}.{i} - {str(e)}")
                
                # 修改输出属性设置部分
                for o, output_info in enumerate(node_info.get('outputs', [])):
                    if o < len(node.outputs):
                        output_socket = node.outputs[o]
                        val = output_info.get('default_value', [])
                        
                        try:
                            if 'NodeSocketColor' in str(type(output_socket)):
                                if isinstance(val, list):
                                    if len(val) >= 4:
                                        output_socket.default_value = (val[0], val[1], val[2], val[3])
                                    elif len(val) >= 3:
                                        output_socket.default_value = (val[0], val[1], val[2], 1.0)
                            elif 'NodeSocketShader' in str(type(output_socket)):
                                continue
                            else:
                                if output_socket.node.bl_idname == 'ShaderNodeGroup':
                                    # 特殊处理节点组输出
                                    group_node = output_socket.node
                                    if group_node.node_tree and group_node.node_tree.nodes:
                                        for sock in group_node.inputs:
                                            if sock.identifier == output_socket.identifier and sock.node_tree:
                                                # 找到节点组内部对应的输入节点
                                                group_input_node = sock.node_tree.nodes.get('Group Input')
                                                if group_input_node:
                                                    for internal_sock in group_input_node.outputs:
                                                        if internal_sock.identifier == sock.identifier:
                                                            if hasattr(internal_sock, 'default_value'):
                                                                if isinstance(val, list) and len(val) >= 1:
                                                                    try:
                                                                        internal_sock.default_value = [float(v) if not isinstance(v, str) else 0.0 for v in val[:len(internal_sock.default_value)]]
                                                                    except:
                                                                        internal_sock.default_value = float(val[0]) if not isinstance(val[0], str) else 0.0
                                                                break
                                else:
                                    if hasattr(output_socket, 'default_value'):
                                        if isinstance(val, list):
                                            if len(val) >= 1:
                                                # 强制转换列表值为合适格式
                                                if 'NodeSocketVector' in str(type(output_socket)):
                                                    if len(val) >= 3:
                                                        output_socket.default_value = (val[0], val[1], val[2])
                                                    else:
                                                        output_socket.default_value = (val[0], val[0], val[0])
                                                elif 'NodeSocketColor' in str(type(output_socket)):
                                                    if len(val) >= 4:
                                                        output_socket.default_value = (val[0], val[1], val[2], val[3])
                                                    else:
                                                        output_socket.default_value = (val[0], val[0], val[0], 1.0)
                                                elif output_socket.node.bl_idname == 'ShaderNodeGroup':
                                                    group_node = output_socket.node
                                                    if group_node.node_tree and group_node.node_tree.nodes:
                                                        # 查找节点组内部对应的输出节点
                                                        group_output_node = group_node.node_tree.nodes.get('Group Output')
                                                        if group_output_node:
                                                            for internal_sock in group_output_node.inputs:
                                                                if internal_sock.identifier == output_socket.identifier:
                                                                    # 强制转换为内部socket类型匹配的格式
                                                                    if 'NodeSocketVector' in str(type(internal_sock)):
                                                                        if isinstance(val, list) and len(val) >= 3:
                                                                            internal_sock.default_value = (val[0], val[1], val[2])
                                                                        else:
                                                                            f_val = float(val) if not isinstance(val, str) else 0.0
                                                                            internal_sock.default_value = (f_val, f_val, f_val)
                                                                    elif 'NodeSocketColor' in str(type(internal_sock)):
                                                                        if isinstance(val, list) and len(val) >= 4:
                                                                            internal_sock.default_value = (val[0], val[1], val[2], val[3])
                                                                        else:
                                                                            f_val = float(val) if not isinstance(val, str) else 0.0
                                                                            internal_sock.default_value = (f_val, f_val, f_val, 1.0)
                                                                    break
                                                else:
                                                    output_socket.default_value = float(val[0]) if not isinstance(val[0], str) else 0.0
                                        else:
                                            output_socket.default_value = float(val) if not isinstance(val, str) else 0.0
                        except Exception as e:
                            print(f"输出值设置失败：{node.name}.{o} - {str(e)}")

            # 修改连接重建部分
            for link_info in nodes_data.get('links', []):
                from_index = link_info.get('from_index', -1)
                to_index = link_info.get('to_index', -1)
                
                if from_index < len(node_instances) and to_index < len(node_instances):
                    from_node = node_instances[from_index]
                    to_node = node_instances[to_index]

                    # 增强socket查找逻辑
                    try:
                        # 处理转接点的特殊socket结构
                        if from_node.bl_idname == 'NodeReroute':
                            # 转接点只有一个输出socket
                            from_socket = next(iter(from_node.outputs))
                        else:
                            from_socket = next(s for s in from_node.outputs if s.identifier == link_info['from_socket'] or s.name == link_info['from_socket'])

                        if to_node.bl_idname == 'NodeReroute':
                            # 转接点只有一个输入socket
                            to_socket = next(iter(to_node.inputs))
                        else:
                            to_socket = next(s for s in to_node.inputs if s.identifier == link_info['to_socket'] or s.name == link_info['to_socket'])

                        # 特殊处理节点组连接
                        if from_node.bl_idname == 'ShaderNodeGroup' or to_node.bl_idname == 'ShaderNodeGroup':
                            from_socket = None
                            to_socket = None
                            
                            # 查找节点组内部socket
                            if from_node.bl_idname == 'ShaderNodeGroup':
                                for sock in from_node.outputs:
                                    if sock.identifier == link_info['from_socket'] and sock.node_tree:
                                        # 找到节点组内部对应的输出节点
                                        group_output_node = sock.node_tree.nodes.get('Group Output')
                                        if group_output_node:
                                            for internal_sock in group_output_node.inputs:
                                                if internal_sock.identifier == sock.identifier:
                                                    from_socket = internal_sock
                                                    break
                            if to_node.bl_idname == 'ShaderNodeGroup':
                                for sock in to_node.inputs:
                                    if sock.identifier == link_info['to_socket'] and sock.node_tree:
                                        # 找到节点组内部对应的输入节点
                                        group_input_node = sock.node_tree.nodes.get('Group Input')
                                        if group_input_node:
                                            for internal_sock in group_input_node.outputs:
                                                if internal_sock.identifier == sock.identifier:
                                                    to_socket = internal_sock
                                                    break
                            
                            if from_socket and to_socket:
                                node_tree.links.new(to_socket, from_socket)
                            elif from_node.bl_idname != 'NodeReroute' and to_node.bl_idname != 'NodeReroute':
                                print(f"无法找到匹配的socket: {link_info['from_socket']} -> {link_info['to_socket']}")
                        else:
                            node_tree.links.new(to_socket, from_socket)
                    except StopIteration as e:
                        print(f"找不到对应socket: {from_node.name}({from_node.bl_idname}) -> {to_node.name}({to_node.bl_idname})")
                        print(f"查找标识符: {link_info['from_socket']} -> {link_info['to_socket']}")
                        raise e
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
