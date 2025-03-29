from manim import *

class BubbleSortSinglePass(Scene):
    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1e1e1e"

        # 待排序的数组
        array = [5, 3, 8, 4, 2]
        n = len(array)

        # 创建标题
        title = Text("冒泡排序单次过程演示", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建数组的可视化表示
        def create_row(arr, color=BLUE):
            row = VGroup()
            for num in arr:
                # 缩小格子大小
                rect = Rectangle(height=0.8, width=0.8, fill_color=color, fill_opacity=0.5, stroke_color=WHITE)
                text = Text(str(num), font_size=20, color=WHITE)  # 缩小字体大小
                group = VGroup(rect, text)
                row.add(group)
            row.arrange(RIGHT, buff=0.3)  # 缩小格子间距
            return row

        # 初始行（当前冒泡排序开始时的数组状态）
        initial_row = create_row(array)
        initial_row.next_to(title, DOWN, buff=1)  # 将初始行上移，靠近标题
        self.play(FadeIn(initial_row))
        self.wait(1)

        # 冒泡排序单次过程
        current_array = array.copy()
        all_rows = [initial_row]  # 保存每一行的状态
        for j in range(n - 1):
            # 高亮当前比较的两个元素
            self.play(
                all_rows[-1][j].animate.set_fill(RED, opacity=0.8),
                all_rows[-1][j + 1].animate.set_fill(RED, opacity=0.8),
                run_time=0.5
            )

            # 如果顺序错误，交换元素
            if current_array[j] > current_array[j + 1]:
                # 交换数组中的值
                current_array[j], current_array[j + 1] = current_array[j + 1], current_array[j]

                # 创建新的一行并下移展示
                new_row = create_row(current_array)
                new_row.next_to(all_rows[-1], DOWN, buff=0.3)  # 缩小行间距
                all_rows.append(new_row)

                # 交换格子
                self.play(
                    all_rows[-2][j].animate.move_to(all_rows[-2][j + 1].get_center()),
                    all_rows[-2][j + 1].animate.move_to(all_rows[-2][j].get_center()),
                    FadeIn(new_row),
                    run_time=1
                )
                # 更新格子的位置
                all_rows[-2][j], all_rows[-2][j + 1] = all_rows[-2][j + 1], all_rows[-2][j]
            else:
                # 如果顺序正确，恢复颜色
                self.play(
                    all_rows[-1][j].animate.set_fill(BLUE, opacity=0.5),
                    all_rows[-1][j + 1].animate.set_fill(BLUE, opacity=0.5),
                    run_time=0.5
                )

        # 标记已排序的元素
        self.play(
            all_rows[-1][-1].animate.set_fill(GREEN, opacity=0.8),
            run_time=0.5
        )
        self.wait(2)