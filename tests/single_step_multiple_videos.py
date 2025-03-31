from manim import *

class BubbleSortFirstStep(Scene):
    def __init__(self, **kwargs):
        self.original_array = [5, 3, 8, 4, 2]
        self.array = [5, 3, 8, 4, 2]
        self.step_num = 0
        super().__init__(**kwargs)

    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1e1e1e"

        # 创建标题
        title = Text(f"冒泡排序第1次排序演示", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建数组的可视化表示
        def create_row(arr, color=BLUE):
            row = VGroup()
            for num in arr:
                rect = Rectangle(height=0.8, width=0.8, fill_color=color, fill_opacity=0.5, stroke_color=WHITE)
                text = Text(str(num), font_size=20, color=WHITE)
                group = VGroup(rect, text)
                row.add(group)
            row.arrange(RIGHT, buff=0.3)
            return row

        # 初始行（原始数组）
        original_row = create_row(self.original_array, color=GRAY)
        original_row.to_edge(LEFT).shift(UP * 2)
        original_label = Text("原始数组", font_size=24, color=GRAY).next_to(original_row, UP)
        self.play(FadeIn(original_row), Write(original_label))
        self.wait(0.5)

        # 当前数组的可视化表示
        current_row = create_row(self.array)
        current_row.next_to(original_row, DOWN, buff=1)
        current_label = Text("当前数组", font_size=24, color=WHITE).next_to(current_row, UP)
        self.play(FadeIn(current_row), Write(current_label))
        self.wait(0.5)

        n = len(self.array)
        # 右侧展示本次排序的过程
        sort_row = create_row(self.array).to_edge(RIGHT).shift(UP * 2)
        self.play(FadeIn(sort_row))
        self.wait(0.5)

        # 用于存储所有排序过程的行
        sort_rows = [sort_row]

        for j in range(n - self.step_num - 1):
            # 字幕：描述当前比较的元素
            compare_text = Text(f"比较 {self.array[j]} 和 {self.array[j + 1]}", font_size=24, color=BLUE)
            compare_text.move_to(ORIGIN)
            self.play(Write(compare_text))
            self.wait(0.5)

            # 高亮当前比较的两个元素
            self.play(
                sort_row[j].animate.set_fill(RED, opacity=0.8),
                sort_row[j + 1].animate.set_fill(RED, opacity=0.8),
                run_time=0.5
            )
            # 移除比较字幕
            self.play(FadeOut(compare_text))
            # 如果顺序错误，交换元素
            if self.array[j] > self.array[j + 1]:
                # 字幕：描述交换操作
                swap_text = Text(f"交换 {self.array[j]} 和 {self.array[j + 1]}", font_size=24, color=RED)
                swap_text.move_to(ORIGIN)
                self.play(Write(swap_text))
                self.wait(0.5)

                # 交换数组中的值
                self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]

                # 交换格子
                self.play(
                    sort_row[j].animate.move_to(sort_row[j + 1].get_center()),
                    sort_row[j + 1].animate.move_to(sort_row[j].get_center()),
                    run_time=1
                )
                # 更新格子的位置
                sort_row[j], sort_row[j + 1] = sort_row[j + 1], sort_row[j]
                # 移除交换字幕
                self.play(FadeOut(swap_text))

                # 创建新的一行并下移展示
                new_sort_row = create_row(self.array)
                new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
                sort_rows.append(new_sort_row)
                self.play(FadeIn(new_sort_row))

                # 更新 sort_row 为新的行
                sort_row = new_sort_row
            else:
                # 如果顺序正确，恢复颜色
                self.play(
                    sort_row[j].animate.set_fill(BLUE, opacity=0.5),
                    sort_row[j + 1].animate.set_fill(BLUE, opacity=0.5),
                    run_time=0.5
                )

        # 标记已排序的元素
        self.play(
            sort_rows[-1][-self.step_num - 1].animate.set_fill(GREEN, opacity=0.8),
            run_time=0.5
        )
        self.wait(1)

        # 更新当前数组的状态
        new_current_row = create_row(self.array)
        new_current_row.move_to(current_row.get_center())
        self.play(Transform(current_row, new_current_row))
        self.wait(1)

        # 保存第一次排序的结果
        self.sorted_array_after_first_step = self.array.copy()


class BubbleSortSecondStep(Scene):
    def __init__(self, sorted_array_after_first_step, **kwargs):
        self.original_array = sorted_array_after_first_step
        self.array = sorted_array_after_first_step.copy()
        self.step_num = 1  # 第二次排序
        super().__init__(**kwargs)

    def construct(self):
        # 设置背景颜色
        self.camera.background_color = "#1e1e1e"

        # 创建标题
        title = Text(f"冒泡排序第2次排序演示", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建数组的可视化表示
        def create_row(arr, color=BLUE):
            row = VGroup()
            for num in arr:
                rect = Rectangle(height=0.8, width=0.8, fill_color=color, fill_opacity=0.5, stroke_color=WHITE)
                text = Text(str(num), font_size=20, color=WHITE)
                group = VGroup(rect, text)
                row.add(group)
            row.arrange(RIGHT, buff=0.3)
            return row

        # 初始行（第一次排序后的数组）
        original_row = create_row(self.original_array, color=GRAY)
        original_row.to_edge(LEFT).shift(UP * 2)
        original_label = Text("第一次排序后的数组", font_size=24, color=GRAY).next_to(original_row, UP)
        self.play(FadeIn(original_row), Write(original_label))
        self.wait(0.5)

        # 当前数组的可视化表示
        current_row = create_row(self.array)
        current_row.next_to(original_row, DOWN, buff=1)
        current_label = Text("当前数组", font_size=24, color=WHITE).next_to(current_row, UP)
        self.play(FadeIn(current_row), Write(current_label))
        self.wait(0.5)

        n = len(self.array)
        # 右侧展示本次排序的过程
        sort_row = create_row(self.array).to_edge(RIGHT).shift(UP * 2)
        self.play(FadeIn(sort_row))
        self.wait(0.5)

        # 用于存储所有排序过程的行
        sort_rows = [sort_row]

        for j in range(n - self.step_num - 1):
            # 字幕：描述当前比较的元素
            compare_text = Text(f"比较 {self.array[j]} 和 {self.array[j + 1]}", font_size=24, color=BLUE)
            compare_text.move_to(ORIGIN)
            self.play(Write(compare_text))
            self.wait(0.5)

            # 高亮当前比较的两个元素
            self.play(
                sort_row[j].animate.set_fill(RED, opacity=0.8),
                sort_row[j + 1].animate.set_fill(RED, opacity=0.8),
                run_time=0.5
            )
            # 移除比较字幕
            self.play(FadeOut(compare_text))
            # 如果顺序错误，交换元素
            if self.array[j] > self.array[j + 1]:
                # 字幕：描述交换操作
                swap_text = Text(f"交换 {self.array[j]} 和 {self.array[j + 1]}", font_size=24, color=RED)
                swap_text.move_to(ORIGIN)
                self.play(Write(swap_text))
                self.wait(0.5)

                # 交换数组中的值
                self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]

                # 交换格子
                self.play(
                    sort_row[j].animate.move_to(sort_row[j + 1].get_center()),
                    sort_row[j + 1].animate.move_to(sort_row[j].get_center()),
                    run_time=1
                )
                # 更新格子的位置
                sort_row[j], sort_row[j + 1] = sort_row[j + 1], sort_row[j]
                # 移除交换字幕
                self.play(FadeOut(swap_text))

                # 创建新的一行并下移展示
                new_sort_row = create_row(self.array)
                new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
                sort_rows.append(new_sort_row)
                self.play(FadeIn(new_sort_row))

                # 更新 sort_row 为新的行
                sort_row = new_sort_row
            else:
                # 如果顺序正确，恢复颜色
                self.play(
                    sort_row[j].animate.set_fill(BLUE, opacity=0.5),
                    sort_row[j + 1].animate.set_fill(BLUE, opacity=0.5),
                    run_time=0.5
                )

        # 标记已排序的元素
        self.play(
            sort_rows[-1][-self.step_num - 1].animate.set_fill(GREEN, opacity=0.8),
            run_time=0.5
        )
        self.wait(1)

        # 更新当前数组的状态
        new_current_row = create_row(self.array)
        new_current_row.move_to(current_row.get_center())
        self.play(Transform(current_row, new_current_row))
        self.wait(1)


if __name__ == "__main__":
    # 运行第一个排序动画
    # first_step_scene = BubbleSortFirstStep()
    # first_step_scene.render()

    # # 获取第一次排序的结果
    sorted_array_after_first_step = first_step_scene.sorted_array_after_first_step

    # 运行第二个排序动画
    second_step_scene = BubbleSortSecondStep(sorted_array_after_first_step)
    second_step_scene.render()
    