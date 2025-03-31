# import sys
# import os

# # 自动获取项目根目录（无论从哪里运行）
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, "../.."))  # 根据实际层级调整
# sys.path.append(project_root)

import sys
# 使用原始字符串设置路径
sys.path.append(r"D://algorithm-animation/soc-anima")

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
    """冒泡排序完整实现"""

    def __init__(self, input_array, **kwargs):
        super().__init__(input_array, **kwargs)
        self.total_steps = len(input_array) - 1

    def construct(self):
        # 标题动画
        title = Text(f"冒泡排序完整演示", font_size=48)
        self.play(Write(title))

        # 初始化数组展示
        array_row = self.create_array_row(self.array)
        self.play(array_row.animate.center())

        # 完整排序过程
        for i in range(self.total_steps):
            self.bubble_pass(array_row, i)

        # 最终效果
        self.play(Flash(array_row[-1].get_center()))
        self.wait(2)

    def bubble_pass(self, array_group, step):
        """单次冒泡过程"""
        n = len(self.array)

        # 添加步骤说明
        step_text = Text(f"第{step+1}次遍历", font_size=32).to_edge(UP)
        self.play(Transform(title, step_text))

        for j in range(n - step - 1):
            # 高亮比较元素
            self.highlight_elements(array_group[j], array_group[j+1])

            if self.array[j] > self.array[j+1]:
                # 执行交换动画
                self.swap_elements(array_group, j)

            # 更新指针位置
            self.move_pointer(j)

        # 标记已排序元素
        self.mark_sorted(array_group[-step-1])

    def highlight_elements(self, elem1, elem2):
        """高亮比较元素动画"""
        self.play(
            elem1.animate.set_fill(self.COLOR_MAP["highlight"]),
            elem2.animate.set_fill(self.COLOR_MAP["highlight"]),
            run_time=0.5
        )

    def swap_elements(self, array_group, index):
        """交换元素动画"""
        self.play(
            array_group[index].animate.move_to(array_group[index+1]),
            array_group[index+1].animate.move_to(array_group[index]),
            path_arc=PI/2,
            run_time=1
        )
        array_group[index], array_group[index+1] = array_group[index+1], array_group[index]