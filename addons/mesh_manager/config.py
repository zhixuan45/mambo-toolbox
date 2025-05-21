# config.py
from ..common.types.framework import is_extension

# 动态获取插件标识符
__addon_name__ = (
    ".".join(__package__.split(".")[:3]) 
    if is_extension() 
    else __package__.split(".")[0]
)
