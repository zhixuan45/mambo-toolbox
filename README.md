# 材质节点预设管理器插件 / Material Node Preset Manager Addon

## 概述 / Overview
本插件专为 Blender 设计，主要功能是保存和加载材质节点预设。它能帮助用户快速复用常用的材质节点配置，提高工作效率，避免重复创建相同的节点结构。

This addon is designed for Blender, with the main functionality of saving and loading material node presets. It helps users quickly reuse common material node configurations, improving workflow efficiency and avoiding recreating the same node structures.

## 功能特性 / Features
- **保存材质节点**：用户可以将当前的材质节点配置保存为预设，方便后续使用。  
  *Save Material Nodes*: Users can save current material node configurations as presets for future use.
- **加载材质节点**：从保存的预设列表中选择预设，快速应用到当前场景中。  
  *Load Material Nodes*: Select presets from the saved list to quickly apply to the current scene.
- **预设管理**：[WIP]支持对保存的预设进行重命名、删除等操作。  
  *Preset Management*: Supports renaming and deleting saved presets.
![GUI](https://github.com/user-attachments/assets/4bf8e439-3b74-426f-8958-e9ef2c546ed9)

## 安装方法 / Installation
1. 下载插件文件。  
   *Download the addon file.*
2. 打开 Blender，进入 `编辑` -> `偏好设置` -> `插件` 选项卡。  
   *Open Blender, go to `Edit` -> `Preferences` -> `Add-ons` tab.*
3. 点击 `安装` 按钮，选择下载的插件文件。  
   *Click `Install`, then select the downloaded addon file.*
4. 勾选插件旁边的复选框以启用插件。  
   *Check the box next to the addon to enable it.*

## 使用方法 / Usage
### 保存材质节点 / Saving Material Nodes
1. 在 Blender 中创建或调整好所需的材质节点。  *当然你也可以去打开别人的工程文件*
   *Create or adjust the desired material nodes in Blender.*
2. 找到插件面板，点击 `保存预设` 按钮。  
   *Find the addon panel and click the `Save Preset` button.*
3. 输入预设名称，然后点击 `确认`。  
   *Enter a preset name and click `Confirm`.*

### 加载材质节点 / Loading Material Nodes
1. 打开插件面板，在预设列表中选择要加载的预设。  
   *Open the addon panel and select the preset to load from the list.*
2. 点击 `加载预设` 按钮，所选预设将应用到当前场景。  
   *Click the `Load Preset` button to apply the selected preset to the current scene.*

### [WIP]管理预设 / Managing Presets
- **重命名**：在预设列表中右键点击预设名称，选择 `重命名` 选项，输入新名称后确认。  
  *Rename*: Right-click the preset name in the list, select `Rename`, enter a new name and confirm.
- **删除**：在预设列表中右键点击预设名称，选择 `删除` 选项。  
  *Delete*: Right-click the preset name in the list and select `Delete`.

## 注意事项 / Notes
- 保存预设时，请确保材质节点配置已经完成，避免保存不完整的配置。  
  *When saving presets, ensure the material node configuration is complete to avoid saving incomplete setups.*
- 加载预设可能会覆盖当前场景中的材质节点，请提前备份重要数据。  
  *Loading presets may overwrite existing material nodes in the scene, please back up important data beforehand.*

## 反馈与贡献 / Feedback & Contribution
如果您在使用过程中遇到问题或有改进建议，请在 [插件仓库地址] 提交 issue。欢迎大家为插件的发展贡献代码！  
*If you encounter issues or have suggestions for improvement, please submit an issue at [Addon Repository URL]. Contributions to the addon's development are welcome!*
