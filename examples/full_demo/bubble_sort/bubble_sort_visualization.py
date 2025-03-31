from manim import *


class BubbleSortVisualization(Scene):
    def __init__(self, original_array, **kwargs):
        self.original_array = original_array
        super().__init__(**kwargs)

    def is_sorted(self, arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def construct(self):
        num_steps = 1
        current_array = self.original_array
        n = len(current_array)
        comparisons = 0
        swaps = 0

        while True:
            if self.is_sorted(current_array):
                sorted_text = Text("数组已排序完成！", font_size=48, color=YELLOW)
                sorted_text.move_to(ORIGIN)
                self.play(Write(sorted_text))
                self.wait(3)
                self.clear()

                # 复杂度分析
                complexity_text = Text("冒泡排序复杂度分析", font_size=48, color=WHITE)
                complexity_text.to_edge(UP)
                self.play(Write(complexity_text))
                self.wait(1)

                best_case_text = Text(f"最好情况: O(n)，当数组已经有序时，仅需比较 {n - 1} 次", font_size=24, color=WHITE)
                best_case_text.next_to(complexity_text, DOWN, buff=0.5)
                self.play(Write(best_case_text))
                self.wait(1)

                worst_case_text = Text(f"最坏情况: O(n^2)，当数组完全逆序时，需要比较 {n * (n - 1) // 2} 次", font_size=24, color=WHITE)
                worst_case_text.next_to(best_case_text, DOWN, buff=0.5)
                self.play(Write(worst_case_text))
                self.wait(1)

                actual_case_text = Text(f"本次排序比较次数: {comparisons}，交换次数: {swaps}", font_size=24, color=WHITE)
                actual_case_text.next_to(worst_case_text, DOWN, buff=0.5)
                self.play(Write(actual_case_text))
                self.wait(3)
                break

            self.camera.background_color = "#1e1e1e"
            title = Text(f"冒泡排序第{num_steps}次排序演示", font_size=48, color=WHITE)
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

            swapped = False
            for j in range(n - num_steps):
                comparisons += 1
                compare_text = Text(f"比较 {current_array[j]} 和 {current_array[j + 1]}", font_size=24, color=BLUE)
                compare_text.move_to(ORIGIN)
                self.play(Write(compare_text))
                self.wait(0.5)

                self.play(
                    sort_row[j].animate.set_fill(RED, opacity=0.8),
                    sort_row[j + 1].animate.set_fill(RED, opacity=0.8),
                    run_time=0.5
                )

                if current_array[j] > current_array[j + 1]:
                    swaps += 1
                    swapped = True
                    swap_text = Text(f"交换 {current_array[j]} 和 {current_array[j + 1]}", font_size=24, color=RED)
                    swap_text.move_to(ORIGIN)
                    self.play(Write(swap_text))
                    self.wait(0.5)

                    current_array[j], current_array[j + 1] = current_array[j + 1], current_array[j]
                    self.play(
                        sort_row[j].animate.move_to(sort_row[j + 1].get_center()),
                        sort_row[j + 1].animate.move_to(sort_row[j].get_center()),
                        run_time=1
                    )
                    self.play(FadeOut(swap_text))

                    new_sort_row = create_row(current_array)
                    new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
                    sort_rows.append(new_sort_row)
                    self.play(FadeIn(new_sort_row))
                    sort_row = new_sort_row

                self.play(
                    sort_row[j].animate.set_fill(BLUE, opacity=0.5),
                    sort_row[j + 1].animate.set_fill(BLUE, opacity=0.5),
                    run_time=0.5
                )
                self.play(FadeOut(compare_text))

            self.play(
                sort_rows[-1][-num_steps].animate.set_fill(GREEN, opacity=0.8),
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
    scene = BubbleSortVisualization(original_array)
    scene.render()
    