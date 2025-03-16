# algorithms/sorting/bubble/basic/basic_bubble.py
from core.base.sorting_base import SortingBase

class BubbleSort(SortingBase):
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