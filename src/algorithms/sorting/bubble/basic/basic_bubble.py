# import sys
# import os

# # 自动获取项目根目录（无论从哪里运行）
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, "../../.."))  # 根据实际层级调整
# sys.path.append(project_root)

import sys
# 使用原始字符串设置路径
sys.path.append(r"D:\\algorithm-animation\soc-anima")

from src.core.base.sorting_base import SortingBase
from manim import *


class BubbleSort(SortingBase):
    """冒泡排序完整实现（修复版）"""

    def __init__(self, input_array, **kwargs):
        super().__init__(input_array, **kwargs)
        self.total_steps = len(input_array) - 1
        self.array_group = None  # 添加实例变量

    def construct(self):
        # 标题动画
        title = Text(f"冒泡排序完整演示", font_size=48)
        self.play(Write(title))
        self.play(FadeOut(title))
        # 初始化数组展示并保存到实例变量
        self.array_group = self.create_array_row(self.array)
        self.play(self.array_group.animate.center())

        # 完整排序过程
        for i in range(self.total_steps):
            self.bubble_pass(title, i)  # 修改参数

        # 最终效果
        self.play(Flash(self.array_group[-1].get_center()))
        self.wait(2)

    def bubble_pass(self, title, step):
        """单次冒泡过程（使用实例变量）"""
        n = len(self.array)
        step_text = Text(f"第{step+1}次遍历", font_size=32).to_edge(UP)
        self.play(Transform(title, step_text))

        for j in range(n - step - 1):
            self.highlight_elements(j)
            
            if self.array[j] > self.array[j+1]:
                self.swap_elements(j)
                # 同步更新底层数组
                self.array[j], self.array[j+1] = self.array[j+1], self.array[j]

        # 标记已排序元素
        self.mark_sorted(self.array_group[-step-1])

    def highlight_elements(self, index):
        """高亮比较元素（优化参数）"""
        self.play(
            self.array_group[index].animate.set_fill(self.COLOR_MAP["highlight"]),
            self.array_group[index+1].animate.set_fill(self.COLOR_MAP["highlight"]),
            run_time=0.5
        )

    def swap_elements(self, index):
        """交换元素动画（直接使用实例变量）"""
        target_left = self.array_group[index+1].get_center()
        target_right = self.array_group[index].get_center()
        
        self.play(
            self.array_group[index].animate.move_to(target_left),
            self.array_group[index+1].animate.move_to(target_right),
            path_arc=PI/2,
            run_time=1
        )
        # 更新图形元素位置
        self.array_group[index], self.array_group[index+1] = self.array_group[index+1], self.array_group[index]
