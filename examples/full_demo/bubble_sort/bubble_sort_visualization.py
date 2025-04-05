from manim import *

class ProfessionalBubbleSort(Scene):
    def __init__(self, original_array, **kwargs):
        self.original_array = original_array.copy()
        super().__init__(**kwargs)
    
    def is_sorted(self, arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    
    def create_element(self, value, color=BLUE, width=1.0, height_scale=0.5):
        """创建带数字的矩形元素"""
        height = value * height_scale
        rect = Rectangle(
            width=width, 
            height=height,
            fill_color=color,
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2
        )
        text = Text(str(value), font_size=24, color=WHITE)
        text.move_to(rect.get_center())
        return VGroup(rect, text)
    
    def create_array_group(self, arr, color=BLUE, position=ORIGIN):
        """创建数组的可视化组"""
        elements = VGroup(*[self.create_element(num, color) for num in arr])
        elements.arrange(RIGHT, buff=0.5)
        elements.move_to(position)
        return elements
    
    def highlight_elements(self, elements, indices, color, run_time=0.5):
        """高亮指定元素"""
        anims = [elements[i][0].animate.set_fill(color) for i in indices]
        return self.play(*anims, run_time=run_time)
    
    def swap_elements(self, elements, i, j, run_time=1.0):
        """交换元素位置并更新数字"""
        # 创建临时元素用于动画
        temp_i = elements[i].copy()
        temp_j = elements[j].copy()
        
        # 添加到场景中
        self.add(temp_i, temp_j)
        self.remove(elements[i], elements[j])
        
        # 执行交换动画
        self.play(
            temp_i.animate.move_to(elements[j]),
            temp_j.animate.move_to(elements[i]),
            run_time=run_time,
            rate_func=smooth
        )
        
        # 更新实际元素位置
        elements[i], elements[j] = elements[j], elements[i]
        self.remove(temp_i, temp_j)
        self.add(elements[i], elements[j])
        
        # 添加交换效果
        self.play(
            elements[i][0].animate.set_fill(RED).scale(1.1),
            elements[j][0].animate.set_fill(RED).scale(1.1),
            run_time=0.3
        )
        self.play(
            elements[i][0].animate.scale(1/1.1),
            elements[j][0].animate.scale(1/1.1),
            run_time=0.3
        )
    
    def create_pseudo_code(self):
        """创建伪代码显示"""
        pseudo = VGroup(
            Text("for i = 0 to n-1:", font="Monospace", font_size=24),
            Text("    for j = 0 to n-i-1:", font="Monospace", font_size=24),
            Text("        if arr[j] > arr[j+1]:", font="Monospace", font_size=24),
            Text("            swap(arr[j], arr[j+1])", font="Monospace", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        pseudo.to_corner(UL, buff=1)
        pseudo.set_opacity(0.7)
        return pseudo
    
    def highlight_code_line(self, pseudo, line_num):
        """高亮伪代码行"""
        for i, line in enumerate(pseudo):
            if i == line_num:
                self.play(line.animate.set_color(YELLOW).set_opacity(1))
            else:
                self.play(line.animate.set_color(WHITE).set_opacity(0.7))
    
    def construct(self):
        # 初始设置
        self.camera.background_color = "#1e1e1e"
        current_array = self.original_array.copy()
        n = len(current_array)
        comparisons = 0
        swaps = 0
        
        # 创建标题
        title = Text("冒泡排序算法可视化", font_size=36, gradient=(BLUE, TEAL))
        title.to_edge(UP)
        
        # 创建初始数组显示
        array_group = self.create_array_group(current_array, position=UP*0.5)
        
        # 创建伪代码
        pseudo_code = self.create_pseudo_code()
        
        # 创建统计信息
        stats = VGroup(
            Text(f"比较次数: {comparisons}", font_size=24),
            Text(f"交换次数: {swaps}", font_size=24),
            Text(f"复杂度: O(n²)", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        stats.to_corner(UR, buff=1)
        
        # 开场动画
        self.play(
            Write(title),
            FadeIn(array_group, shift=UP),
            FadeIn(pseudo_code),
            FadeIn(stats),
            run_time=2
        )
        self.wait(1)
        
        # 排序过程
        for i in range(n-1):
            # 高亮外循环代码
            self.highlight_code_line(pseudo_code, 0)
            self.wait(0.5)
            
            # 添加轮次标记
            round_text = Text(f"第 {i+1} 轮", font_size=28, color=YELLOW)
            round_text.next_to(title, DOWN)
            self.play(Write(round_text))
            self.wait(0.5)
            
            for j in range(n-i-1):
                # 高亮内循环代码
                self.highlight_code_line(pseudo_code, 1)
                comparisons += 1
                
                # 更新统计信息
                stats[0].become(Text(f"比较次数: {comparisons}", font_size=24))
                self.play(FadeIn(stats[0], shift=LEFT))
                
                # 高亮比较的元素
                self.highlight_elements(array_group, [j, j+1], RED)
                self.highlight_code_line(pseudo_code, 2)
                self.wait(0.3)
                
                if current_array[j] > current_array[j+1]:
                    swaps += 1
                    # 更新统计信息
                    stats[1].become(Text(f"交换次数: {swaps}", font_size=24))
                    self.play(FadeIn(stats[1], shift=LEFT))
                    
                    # 高亮交换代码
                    self.highlight_code_line(pseudo_code, 3)
                    
                    # 执行交换
                    current_array[j], current_array[j+1] = current_array[j+1], current_array[j]
                    self.swap_elements(array_group, j, j+1)
                    
                    # 添加交换音效标记（后期配音用）
                    sound_marker = Dot(radius=0.1, color=RED, fill_opacity=0)
                    sound_marker.move_to(array_group[j])
                    self.add(sound_marker)
                    self.wait(0.1)
                    self.remove(sound_marker)
                
                # 恢复元素颜色
                self.highlight_elements(array_group, [j, j+1], BLUE)
                self.wait(0.2)
            
            # 标记已排序的元素
            sorted_index = n-i-1
            self.play(
                array_group[sorted_index][0].animate.set_fill(GREEN),
                run_time=0.5
            )
            
            # 移除轮次标记
            self.play(FadeOut(round_text))
        
        # 全部排序完成
        self.play(
            *[elem[0].animate.set_fill(GREEN) for elem in array_group],
            run_time=1.5
        )
        
        # 显示完成信息
        complete_text = Text("排序完成!", font_size=48, color=GOLD)
        complete_text.move_to(DOWN*1.5)
        
        # 复杂度分析
        analysis = VGroup(
            Text("时间复杂度分析:", font_size=32, color=WHITE),
            Text(f"• 最好情况: O(n) (已排序数组)", font_size=24, color=GREEN),
            Text(f"• 最坏情况: O(n²) (逆序数组)", font_size=24, color=RED),
            Text(f"• 本次排序: {comparisons}次比较, {swaps}次交换", font_size=24, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT)
        analysis.next_to(complete_text, DOWN, buff=1)
        
        # 显示结果
        self.play(
            Write(complete_text),
            run_time=1.5
        )
        self.wait(1)
        self.play(
            LaggedStart(*[Write(line) for line in analysis], lag_ratio=0.3),
            run_time=2
        )
        self.wait(3)
        
        # 结束动画
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

if __name__ == "__main__":
    original_array = [5, 3, 8, 4, 2, 7, 1, 6]  # 增加数组长度演示更多效果
    scene = ProfessionalBubbleSort(original_array)
    scene.render()