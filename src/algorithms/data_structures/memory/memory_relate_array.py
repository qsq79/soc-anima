import sys
# 使用原始字符串设置路径
sys.path.append(r"D:\\algorithm-animation\soc-anima")

from manim import *

class ArrayInMemory(Scene):
    def construct(self):
        # 标题
        title = Text("数组在内存中的工作原理", font_size=48)
        subtitle = Text("连续存储的奥秘", font_size=36).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # 内存布局图示
        memory_title = Text("计算机内存布局", font_size=40)
        self.play(Write(memory_title))
        self.wait(1)
        self.play(memory_title.animate.to_edge(UP))

        # 创建内存网格
        rows, cols = 1, 10  # 单行多列表示连续内存
        memory_grid = self.create_memory_grid(rows, cols)
        self.play(Create(memory_grid), run_time=1.5)
        self.wait(1)

        # 标记数组区域
        array_length = 5
        array_rect = SurroundingRectangle(
            VGroup(*memory_grid[0:array_length*2:2]),  # 每两个元素是一个内存单元(框+地址)
            color=YELLOW,
            buff=0.1
        )
        array_label = Text("数组分配的内存区域", font_size=28).next_to(array_rect, UP)
        self.play(Create(array_rect), Write(array_label))
        self.wait(2)

        # 数组元素定义
        array_elements = ["数据1", "数据2", "数据3", "数据4", "数据5"]
        element_size = 4  # 假设每个元素占4字节

        # 显示数组声明
        code = Code(
            code="int numbers[5] = {10, 20, 30, 40, 50};",  # 将text改为code
            language="cpp",
            font="Monospace",
            font_size=24,
            line_spacing=0.8,
            margin=0.2
        ).to_edge(DOWN)
        self.play(Write(code))
        self.wait(2)

        # 在内存中填充数组元素
        element_objects = []
        for i in range(array_length):
            # 内存地址计算
            address = Text(f"0x{i*element_size:04X}", font_size=16).move_to(
                memory_grid[2*i].get_corner(UL) + DOWN*0.15 + RIGHT*0.15
            )

            # 数组元素值
            value = Text(str((i+1)*10), font_size=28).move_to(memory_grid[2*i])

            # 索引标签
            index = Text(f"[{i}]", font_size=20, color=BLUE).next_to(memory_grid[2*i], DOWN)

            self.play(
                Transform(memory_grid[2*i+1], address),  # 替换为实际地址
                FadeIn(value),
                FadeIn(index),
                run_time=0.5
            )
            element_objects.extend([address, value, index])

        # 展示数组特性
        properties = VGroup(
            Text("数组特性:", font_size=32, color=YELLOW),
            Text("1. 连续的内存空间", font_size=28),
            Text("2. 相同类型的数据元素", font_size=28),
            Text("3. 固定长度(声明时确定)", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(memory_grid, RIGHT)

        self.play(Write(properties[0]))
        self.wait(0.5)
        self.play(Write(properties[1]))
        self.wait(0.5)
        self.play(Write(properties[2]))
        self.wait(0.5)
        self.play(Write(properties[3]))
        self.wait(2)

        # 地址计算演示
        calc_title = Text("数组地址计算公式:", font_size=32).to_edge(DOWN)
        calc_formula = Tex(
            r"\text{元素地址} = \text{首地址} + \text{索引} \times \text{元素大小}",
            font_size=36
        ).next_to(calc_title, DOWN)

        self.play(Write(calc_title))
        self.play(Write(calc_formula))
        self.wait(2)

        # 示例计算第三个元素
        example = VGroup(
            Text("例如访问numbers[2]:", font_size=28),
            Tex(
                r"0x0000 + 2 \times 4 = 0x0008",
                font_size=32
            ).next_to(calc_formula, DOWN)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)

        # 高亮第三个元素
        highlight = SurroundingRectangle(element_objects[4], color=RED, buff=0.1)

        self.play(
            FadeOut(calc_title),
            FadeOut(calc_formula),
            FadeIn(example),
            Create(highlight)
        )
        self.wait(3)

        # 随机访问演示
        pointer = Arrow(ORIGIN, UP*0.5, color=RED).next_to(memory_grid[4], DOWN)
        pointer_label = Text("直接访问numbers[2]", font_size=24).next_to(pointer, DOWN)
        self.play(GrowArrow(pointer), Write(pointer_label))
        self.wait(2)

        # 总结优势
        advantages = VGroup(
            Text("数组优势:", font_size=32, color=GREEN),
            Text("• O(1)时间复杂度的随机访问", font_size=28),
            Text("• 内存连续，缓存友好", font_size=28),
            Text("• 简单高效", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(memory_grid, LEFT)

        self.play(Write(advantages[0]))
        self.wait(0.5)
        self.play(Write(advantages[1]))
        self.wait(0.5)
        self.play(Write(advantages[2]))
        self.wait(0.5)
        self.play(Write(advantages[3]))
        self.wait(3)

        # 清理场景
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 结束语
        conclusion = Text("数组通过连续内存分配实现高效随机访问", font_size=36)
        next_step = Text("接下来我们将探讨链表的存储方式...", font_size=32).next_to(conclusion, DOWN)
        self.play(Write(conclusion))
        self.wait(2)
        self.play(Write(next_step))
        self.wait(3)

    def create_memory_grid(self, rows, cols):
        """创建内存网格，每个单元包含框和默认地址文本"""
        grid = VGroup()
        for i in range(rows):
            for j in range(cols):
                box = Rectangle(height=1, width=1, color=WHITE)
                box.move_to([j*1.2 - (cols-1)*1.2/2, i*1.2 - (rows-1)*1.2/2, 0])
                # 默认地址文本(会被实际地址替换)
                addr = Text(f"cell_{i*cols+j}", font_size=16).move_to(box)
                grid.add(box, addr)
        return grid

if __name__ == "__main__":
    # 初始化配置
    config.quality = "high_quality"
    config.frame_rate = 60

    # 运行示例
    scene = ArrayInMemory()
    scene.render()