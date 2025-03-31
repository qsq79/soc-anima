from manim import *


class ShellSortVisualization(Scene):
    def __init__(self, original_array, **kwargs):
        self.original_array = original_array
        super().__init__(**kwargs)

    def is_sorted(self, arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def construct(self):
        num_steps = 1
        current_array = self.original_array
        n = len(current_array)
        gap = n // 2

        while True:
            if self.is_sorted(current_array):
                sorted_text = Text("数组已排序完成！", font_size=48, color=YELLOW)
                sorted_text.move_to(ORIGIN)
                self.play(Write(sorted_text))
                self.wait(3)
                break

            self.camera.background_color = "#1e1e1e"
            title = Text(f"希尔排序第{num_steps}次排序演示，间隔为 {gap}", font_size=48, color=WHITE)
            title.to_edge(UP)
            self.play(Write(title))
            self.wait(1)

            def create_row(arr, color=BLUE):
                row = VGroup()
                for num in arr:
                    rect = Rectangle(height=0.8, width=0.8, fill_color=color, fill_opacity=0.5, stroke_color=WHITE)
                    text = Text(str(num), font_size=20, color=WHITE)
                    group = VGroup(rect, text)
                    row.add(group)
                row.arrange(RIGHT, buff=0.3)
                return row

            original_row = create_row(current_array, color=GRAY)
            original_row.to_edge(LEFT).shift(UP * 2)
            original_label = Text(f"第{num_steps - 1}次排序后的数组", font_size=24, color=GRAY).next_to(original_row, UP)
            self.play(FadeIn(original_row), Write(original_label))
            self.wait(0.5)

            current_row = create_row(current_array)
            current_row.next_to(original_row, DOWN, buff=1)
            current_label = Text("当前数组", font_size=24, color=WHITE).next_to(current_row, UP)
            self.play(FadeIn(current_row), Write(current_label))
            self.wait(0.5)

            sort_row = create_row(current_array).to_edge(RIGHT).shift(UP * 2)
            self.play(FadeIn(sort_row))
            self.wait(0.5)

            sort_rows = [sort_row]

            while gap > 0:
                for i in range(gap, n):
                    temp = current_array[i]
                    j = i
                    compare_text = Text(f"比较 {current_array[i]} 和 {current_array[j - gap]}", font_size=24, color=BLUE)
                    compare_text.move_to(ORIGIN)
                    self.play(Write(compare_text))
                    self.wait(0.5)

                    self.play(
                        sort_row[i].animate.set_fill(RED, opacity=0.8),
                        sort_row[j - gap].animate.set_fill(RED, opacity=0.8),
                        run_time=0.5
                    )

                    while j >= gap and current_array[j - gap] > temp:
                        swap_text = Text(f"交换 {current_array[j - gap]} 和 {current_array[j]}", font_size=24, color=RED)
                        swap_text.move_to(ORIGIN)
                        self.play(Write(swap_text))
                        self.wait(0.5)

                        current_array[j] = current_array[j - gap]
                        self.play(
                            sort_row[j].animate.move_to(sort_row[j - gap].get_center()),
                            run_time=1
                        )
                        self.play(FadeOut(swap_text))
                        j -= gap

                    current_array[j] = temp
                    new_sort_row = create_row(current_array)
                    new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
                    sort_rows.append(new_sort_row)
                    self.play(FadeIn(new_sort_row))
                    sort_row = new_sort_row

                    self.play(
                        sort_row[i].animate.set_fill(BLUE, opacity=0.5),
                        sort_row[j - gap].animate.set_fill(BLUE, opacity=0.5),
                        run_time=0.5
                    )
                    self.play(FadeOut(compare_text))

                gap //= 2

            self.play(
                sort_rows[-1].animate.set_fill(GREEN, opacity=0.8),
                run_time=0.5
            )
            self.wait(1)

            new_current_row = create_row(current_array)
            new_current_row.move_to(current_row.get_center())
            self.play(Transform(current_row, new_current_row))
            self.wait(1)

            self.clear()
            num_steps += 1


if __name__ == "__main__":
    original_array = [5, 3, 8, 4, 2]
    scene = ShellSortVisualization(original_array)
    scene.render()
    