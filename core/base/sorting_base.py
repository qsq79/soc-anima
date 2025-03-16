# core/base/sorting_base.py
from manim import *

class SortingBase(Scene):
    """排序算法基类"""
    
    # 颜色配置（后续可迁移到color_schemes.yaml）
    COLOR_MAP = {
        "default": BLUE,
        "highlight": RED,
        "sorted": GREEN,
        "background": "#1e1e1e"
    }
    
    def __init__(self, input_array, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = self.COLOR_MAP["background"]
        self.original_array = input_array.copy()
        self.array = input_array.copy()
        
    def create_element(self, num, color=BLUE):
        """创建带数字的方块元素"""
        return VGroup(
            Rectangle(height=0.8, width=0.8, 
                     fill_color=color, fill_opacity=0.5,
                     stroke_color=WHITE),
            Text(str(num), font_size=24)
        )
    
    def create_array_row(self, arr, color=BLUE):
        """创建水平排列的数组"""
        row = VGroup(*[self.create_element(num, color) for num in arr])
        row.arrange(RIGHT, buff=0.3)
        return row