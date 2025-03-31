from manim import *


class MergeSortVisualization(Scene):
    def __init__(self, original_array, **kwargs):
        self.original_array = original_array
        super().__init__(**kwargs)

    def is_sorted(self, arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def merge(self, arr, l, m, r, sort_row, sort_rows, create_row):
        n1 = m - l + 1
        n2 = r - m

        L = [0] * n1
        R = [0] * n2

        for i in range(0, n1):
            L[i] = arr[l + i]

        for j in range(0, n2):
            R[j] = arr[m + 1 + j]

        i = 0
        j = 0
        k = l

        while i < n1 and j < n2:
            compare_text = Text(f"比较 {L[i]} 和 {R[j]}", font_size=24, color=BLUE)
            compare_text.move_to(ORIGIN)
            self.play(Write(compare_text))
            self.wait(0.5)

            self.play(
                sort_row[l + i].animate.set_fill(RED, opacity=0.8),
                sort_row[m + 1 + j].animate.set_fill(RED, opacity=0.8),
                run_time=0.5
            )

            if L[i] <= R[j]:
                arr[k] = L[i]
                i = i + 1
            else:
                arr[k] = R[j]
                j = j + 1

            new_sort_row = create_row(arr)
            new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
            sort_rows.append(new_sort_row)
            self.play(FadeIn(new_sort_row))
            sort_row = new_sort_row

            self.play(
                sort_row[l + i - 1].animate.set_fill(BLUE, opacity=0.5),
                sort_row[m + 1 + j - 1].animate.set_fill(BLUE, opacity=0.5),
                run_time=0.5
            )
            self.play(FadeOut(compare_text))
            k = k + 1

        while i < n1:
            arr[k] = L[i]
            new_sort_row = create_row(arr)
            new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
            sort_rows.append(new_sort_row)
            self.play(FadeIn(new_sort_row))
            sort_row = new_sort_row
            i = i + 1
            k = k + 1

        while j < n2:
            arr[k] = R[j]
            new_sort_row = create_row(arr)
            new_sort_row.next_to(sort_rows[-1], DOWN, buff=0.5)
            sort_rows.append(new_sort_row)
            self.play(FadeIn(new_sort_row))
            sort_row = new_sort_row
            j = j + 1
            k = k + 1

        return sort_row

    def merge_sort(self, arr, l, r, sort_row, sort_rows, create_row):
        if l < r:
            m = (l + r) // 2

            self.merge_sort(arr, l, m, sort_row, sort_rows, create_row)
            self.merge_sort(arr, m + 1, r, sort_row, sort_rows, create_row)

            sort_row = self.merge(arr, l, m, r, sort_row, sort_rows, create_row)

        return sort_row

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
            title = Text(f"归并排序第{num_steps}次排序演示", font_size=48, color=WHITE)
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

            self.merge_sort(current_array, 0, n - 1, sort_row, sort_rows, create_row)

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
    scene = MergeSortVisualization(original_array)
    scene.render()
    