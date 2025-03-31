import sys
# 使用原始字符串设置路径
sys.path.append(r"D:\\algorithm-animation\soc-anima")

# core/base/sorting_base.py
from manim import *

# core/base/sorting_base.py
class SortingBase(Scene):
    """排序算法基类（修复版）"""
    
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
        self.array_group = None  # 初始化数组容器

    def create_element(self, num, color=BLUE):
        return VGroup(
            Rectangle(height=0.8, width=0.8, 
                     fill_color=color, fill_opacity=0.5,
                     stroke_color=WHITE),
            Text(str(num), font_size=24))
    
    def create_array_row(self, arr, color=BLUE):
        self.array_group = VGroup(*[self.create_element(num, color) for num in arr])
        self.array_group.arrange(RIGHT, buff=0.3)
        return self.array_group
    
    def move_pointer(self, index):
        """移动指针动画（基于实例变量）"""
        if not hasattr(self, "pointer"):
            self.pointer = Arrow(start=UP, end=DOWN, color=YELLOW).scale(0.5)
            self.add(self.pointer)
        
        target_pos = self.array_group[index].get_top() + UP*0.5
        self.play(self.pointer.animate.next_to(target_pos, UP))

    def mark_sorted(self, element):
        """标记已排序元素"""
        self.play(
            element.animate.set_fill(self.COLOR_MAP["sorted"]),
            run_time=0.5
        )