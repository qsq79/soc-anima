from manim import *


class QuickSortVisualization(Scene):
    def __init__(self, original_array, **kwargs):
        self.original_array = original_array
        super().__init__(**kwargs)

    def is_sorted(self, arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def partition(self, arr, low, high, sort_row, sort_rows, create_row):
        pivot = arr[high]
        pivot_text = Text(f"基准值: {pivot}", font_size=24, color=BLUE)
        pivot_text.move_to(ORIGIN)
        self.play(Write(pivot_text))
        self.wait(0.5)

        self.play(sort_row[high].animate.set_fill(YELLOW, opacity=0.8))
        i = low - 1

        for j in range(low, high):
            compare_text = Text(f"比较 {arr[j]} 和 {pivot}", font_size=24, color=BLUE)
            compare_text.move_to(ORIGIN)
            self.play(Write(compare_text))
            self.wait(0.5)

            self.play(
                sort_row[j].animate.set_fill(RED, opacity=0.8),
                run_time=0.5
            )

            if arr[j] <= pivot:
                i = i + 1
                swap_text = Text(f"交换 {arr[i]} 和 {arr[j]}", font_size=24, color=RED)
                swap_text.move_to(ORIGIN)
                self.play(Write(swap_text))
                self.wait(0.5)

                arr[i], arr[j] = arr[j], arr[i]
                self.play(
                    sort_row[i].animate.move_to(sort_row[j].get_center()),
                    sort_row[j].animate.move_to(sort_row[i].get_center()),
                    run_time=1
                )
                self.play(FadeOut(swap_text))

            self.play(
                sort_row[j].animate.set_fill(BLUE, opacity=0.5),
                run_time=0.5
            )
            self.play(FadeOut(compare_text))

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.play(
            sort_row[i + 1].animate.move_to(sort_row[high].get_center()),
            sort_row[high].animate.move_to(sort_row[i + 1].get_center()),
            run_time=1
        )

        new_sort_row = create_row(arr)
        new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
        sort_rows.append(new_sort_row)
        self.play(FadeIn(new_sort_row))
        sort_row = new_sort_row

        self.play(FadeOut(pivot_text))
        return i + 1

    def quick_sort(self, arr, low, high, sort_row, sort_rows, create_row):
        if low < high:
            pi = self.partition(arr, low, high, sort_row, sort_rows, create_row)

            self.quick_sort(arr, low, pi - 1, sort_row, sort_rows, create_row)
            self.quick_sort(arr, pi + 1, high, sort_row, sort_rows, create_row)

    def construct(self):
        num_steps = 1
        current_array = self.original_array
        n = len(current_array)

        while True:
            if self.is_sorted(current_array):
                sorted_text = Text("数组已排序完成！", font_size=48, color=YELLOW)
                sorted_text.move_to(ORIGIN)
                self.play(Write(sorted_text))
                self.wait(3)
                break

            self.camera.background_color = "#1e1e1e"
            title = Text(f"快速排序第{num_steps}次排序演示", font_size=48, color=WHITE)
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

            self.quick_sort(current_array, 0, n - 1, sort_row, sort_rows, create_row)

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
    scene = QuickSortVisualization(original_array)
    scene.render()
    