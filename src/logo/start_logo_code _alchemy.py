from manim import *
import numpy as np


class Gear(VMobject):
    def __init__(self, radius=1.0, inner_radius=0.5, n_teeth=12, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.inner_radius = inner_radius
        self.n_teeth = n_teeth

        # 创建齿轮齿
        angle_step = 2 * PI / n_teeth
        teeth_width = angle_step * 0.4

        points = []
        for i in range(n_teeth):
            # 齿根
            angle = i * angle_step
            points.append(inner_radius * np.array([np.cos(angle), np.sin(angle), 0]))

            # 齿顶外点1
            points.append(radius * np.array([np.cos(angle - teeth_width / 2), np.sin(angle - teeth_width / 2), 0]))

            # 齿顶外点2
            points.append(radius * np.array([np.cos(angle + teeth_width / 2), np.sin(angle + teeth_width / 2), 0]))

        # 闭合路径
        points.append(points[0])

        self.set_points_as_corners(points)
        self.set_fill(opacity=1)


class DataNode(Circle):
    def __init__(self, radius=0.2, color=YELLOW, **kwargs):
        super().__init__(radius=radius, color=color, **kwargs)
        self.set_fill(color, opacity=1)


class NewVideoLogo(Scene):
    def construct(self):
        # === 配置 ===
        self.camera.background_color = "#1a1b26"
        gear_color = "#4cc9f0"  # 科技蓝
        node_color = YELLOW  # 数据节点颜色
        code_color = "#9ece6a"  # 代码颜色

        # === 1. 创建主齿轮 ===
        main_gear = Gear(radius=1.5, inner_radius=0.75, n_teeth=20,
                         fill_color=gear_color, stroke_color=WHITE, stroke_width=2)

        # === 2. 创建小齿轮组 ===
        small_gears = VGroup(*[
            Gear(radius=0.4, inner_radius=0.2, n_teeth=10,
                 fill_color=gear_color, stroke_color=WHITE, stroke_width=1.5).shift(pos)
            for pos in [UP * 2, DOWN * 2, LEFT * 2, RIGHT * 2]
        ])

        # === 3. 创建连接轴 ===
        axles = VGroup(*[
            Line(ORIGIN, dir * 1.6, stroke_width=4, color=WHITE)
            for dir in [UP, DOWN, LEFT, RIGHT]
        ]).move_to(main_gear.get_center())

        # === 4. 数据结构元素 ===
        data_nodes = VGroup(*[
            DataNode(color=node_color).move_to(gear.get_center())
            for gear in small_gears
        ])

        data_lines = VGroup(*[
            Line(main_gear.get_center(), node.get_center(), color=node_color, stroke_width=2)
            for node in data_nodes
        ])

        # === 5. 文字标识 ===
        name_cn = Text("@码理炼金", font="思源黑体 CN Bold", font_size=40)
        # name_en = Text("@Code Alchemy", font="Roboto Mono", font_size=30)
        text_group = VGroup(name_cn).arrange(DOWN, aligned_edge=LEFT)
        text_group.next_to(main_gear, DOWN, buff=1)

        # === 6. 代码片段元素 ===
        code_text = Text("def alchemy():\n    result = transform(code)\n    return result", font="Courier New", font_size=20, color=code_color)
        code_text.shift(UP * 3)

        # === 7. 二进制数字流元素 ===
        binary_digits = [Text(str(np.random.randint(0, 2)), font="Courier New", font_size=16, color=code_color) for _ in range(20)]
        binary_stream = VGroup(*binary_digits)
        for i, digit in enumerate(binary_digits):
            digit.shift(LEFT * 5 + UP * (i / 2 - 5))

        # === 8. 炼金炉图标元素 ===
        def create_alchemy_furnace():
            # 炼金炉主体
            alchemy_furnace = RoundedRectangle(corner_radius=0.2, width=2, height=2, stroke_color=WHITE, fill_color="#8B4513", fill_opacity=1)
            # 炼金炉顶部开口
            furnace_opening = Ellipse(width=1.5, height=0.5, color=WHITE, fill_color="#FF8C00", fill_opacity=1).move_to(alchemy_furnace.get_top())
            # 组合炼金炉
            return VGroup(alchemy_furnace, furnace_opening).scale(0.5)

        # 创建四个炼金炉并放置到四个角落
        alchemy_furnaces = VGroup(
            create_alchemy_furnace().to_corner(UL),
            create_alchemy_furnace().to_corner(UR),
            create_alchemy_furnace().to_corner(DL),
            create_alchemy_furnace().to_corner(DR)
        )

        # 炼金炉动画效果
        def update_furnaces(mob, dt):
            for furnace in mob:
                furnace_opening = furnace[1]
                new_opacity = 0.5 + 0.5 * np.sin(self.time * 2)
                furnace_opening.set_opacity(new_opacity)

        alchemy_furnaces.add_updater(update_furnaces)

        # === 9. 动画序列 ===
        # 第一阶段：背景闪烁
        background_flash = Rectangle(width=config.frame_width, height=config.frame_height, color=WHITE, fill_opacity=0.2)
        self.add(background_flash)
        self.play(
            FadeOut(background_flash, run_time=0.5)
        )

        # 第二阶段：主齿轮浮现
        self.play(
            DrawBorderThenFill(main_gear),
            run_time=1.5,
            rate_func=smooth
        )

        # 第三阶段：小齿轮和连接轴出现
        self.play(
            *[FadeIn(gear, shift=dir * 0.3) for gear, dir in zip(small_gears, [UP, DOWN, LEFT, RIGHT])],
            Create(axles),
            run_time=1.5
        )

        # 齿轮旋转动画
        def update_gears(mob, dt):
            mob[0].rotate(-dt)  # 主齿轮逆时针
            for i in range(4):
                mob[1][i].rotate(2 * dt)  # 小齿轮顺时针

        gear_system = VGroup(main_gear, small_gears)
        gear_system.add_updater(update_gears)
        self.add(gear_system)

        # 第四阶段：数据结构元素出现
        self.play(
            FadeIn(data_nodes),
            Create(data_lines),
            run_time=1.5
        )

        # 数据节点闪烁动画
        def update_nodes(mob, dt):
            for node in mob:
                node.set_opacity(0.5 + 0.5 * np.sin(self.time * 2))

        data_nodes.add_updater(update_nodes)
        self.add(data_nodes)

        # 第五阶段：代码片段出现
        self.play(Write(code_text), run_time=1.5)

        # 第六阶段：二进制数字流滚动
        def update_binary_stream(mob, dt):
            for digit in mob:
                digit.shift(RIGHT * 0.1)
                if digit.get_center()[0] > 5:
                    digit.move_to(LEFT * 5 + digit.get_center()[1] * UP)

        binary_stream.add_updater(update_binary_stream)
        self.add(binary_stream)

        # 第七阶段：炼金炉图标出现
        self.play(FadeIn(alchemy_furnaces), run_time=1.5)

        # 第八阶段：文字显现
        self.play(
            LaggedStart(
                Write(name_cn),
                # Write(name_en),
                lag_ratio=0.3
            ),
            run_time=1.8
        )

        # 最终光效
        light = VGroup(main_gear, small_gears, axles, data_nodes, data_lines, text_group, code_text, binary_stream, alchemy_furnaces).copy()
        light.set_fill(opacity=0.1).set_stroke(width=0)
        self.add(light)
        self.play(
            light.animate.scale(1.3).set_opacity(0),
            run_time=3,
            rate_func=there_and_back
        )
        self.remove(light)

        self.wait(3)


if __name__ == "__main__":
    scene = NewVideoLogo()
    scene.render()
    