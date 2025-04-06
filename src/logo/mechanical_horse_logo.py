from manim import *
import numpy as np

class Gear(VMobject):
    def __init__(self, radius=1.0, inner_radius=0.5, n_teeth=12, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.inner_radius = inner_radius
        self.n_teeth = n_teeth
        
        angle_step = 2 * PI / n_teeth
        teeth_width = angle_step * 0.4
        
        points = []
        for i in range(n_teeth):
            angle = i * angle_step
            points.append(inner_radius * np.array([np.cos(angle), np.sin(angle), 0]))
            points.append(radius * np.array([np.cos(angle - teeth_width/2), np.sin(angle - teeth_width/2), 0]))
            points.append(radius * np.array([np.cos(angle + teeth_width/2), np.sin(angle + teeth_width/2), 0]))
        
        points.append(points[0])
        self.set_points_as_corners(points)
        self.set_fill(opacity=1)

class ComplexityGraph(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 创建坐标系（调整范围）
        self.axes = Axes(
            x_range=[0, 5, 1],  # x轴最大为5
            y_range=[0, 6, 1],  # y轴调整为6
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={"numbers_to_include": np.arange(0, 6, 1)},
            y_axis_config={"numbers_to_include": np.arange(0, 7, 1)},
        ).scale(0.4)
        
        # 四条复杂度曲线（调整函数使在0-5范围内显示和谐）
        self.graphs = VGroup(
            self.axes.plot(lambda x: 0.5*np.log2(5*x+1), color=PURPLE, stroke_width=3),  # O(log n)
            self.axes.plot(lambda x: x, color=GREEN, stroke_width=3),                    # O(n)
            self.axes.plot(lambda x: 0.5*x*np.log2(5*x+1), color=YELLOW, stroke_width=3),# O(n log n)
            self.axes.plot(lambda x: 0.3*x**2, color=RED, stroke_width=3)               # O(n²)
        )
        
        # 四个动态点（颜色与曲线对应）
        self.dots = VGroup(
            Dot(color=PURPLE, radius=0.07),  # O(log n)点
            Dot(color=GREEN, radius=0.07),   # O(n)点
            Dot(color=YELLOW, radius=0.07),  # O(n log n)点
            Dot(color=RED, radius=0.07)      # O(n²)点
        )
        
        # 在曲线上直接添加标注
        self.labels = VGroup(
            MathTex(r"O(\log n)", color=PURPLE).scale(0.5)
                .next_to(self.graphs[0].get_end(), UP, buff=0.1),
            MathTex(r"O(n)", color=GREEN).scale(0.5)
                .next_to(self.graphs[1].point_from_proportion(0.7), UP, buff=0.1),
            MathTex(r"O(n\log n)", color=YELLOW).scale(0.5)
                .next_to(self.graphs[2].point_from_proportion(0.6), UP, buff=0.1),
            MathTex(r"O(n^2)", color=RED).scale(0.5)
                .next_to(self.graphs[3].point_from_proportion(0.5), UR, buff=0.1)
        )
        
        self.add(self.axes, self.graphs, self.dots, self.labels)

class MechanicalHorseLogo(Scene):
    def construct(self):
        # === 配置 ===
        self.camera.background_color = "#1a1b26"
        horse_color = "#ff9e64"
        gear_color = "#4cc9f0"
        
        # === 左侧复杂度曲线图 ===
        complexity = ComplexityGraph().to_edge(LEFT, buff=0.3)
        self.add(complexity)
        
        def update_dots(mob, dt):
            # 每个点以不同速度移动，x范围0-5
            t = self.time % 5  # 5秒循环
            mob[0].move_to(complexity.axes.c2p(t+0.5, 0.5*np.log2(5*(t+0.5)+1)))  # O(log n)
            mob[1].move_to(complexity.axes.c2p(t+0.5, t+0.5))                    # O(n)
            mob[2].move_to(complexity.axes.c2p(t+0.5, 0.5*(t+0.5)*np.log2(5*(t+0.5)+1)))  # O(n log n)
            mob[3].move_to(complexity.axes.c2p(t+0.5, 0.3*(t+0.5)**2))           # O(n²)
        
        complexity.dots.add_updater(update_dots)
        
        # === 机械马和齿轮 ===
        horse_body = VGroup(
            Polygon([-1,0,0], [1,0,0], [0.5,1.5,0], [-0.5,1.5,0], color=horse_color),
            Polygon([0.8,1.5,0], [1.5,2.2,0], [1,2.5,0], color=horse_color),
            Ellipse(width=0.6, height=0.8).move_to([1.7,2.7,0])
        ).set_fill(horse_color).set_stroke(WHITE, width=2)
        
        main_gear = Gear(radius=0.8, inner_radius=0.4, n_teeth=16,
                        fill_color=gear_color, stroke_color=WHITE, stroke_width=2)
        
        small_gears = VGroup(*[
            Gear(radius=0.3, inner_radius=0.15, n_teeth=10,
                 fill_color=gear_color, stroke_color=WHITE, stroke_width=1.5).shift(pos)
            for pos in [UL*0.6, UR*0.6, DL*0.6, DR*0.6]
        ])
        
        axles = VGroup(*[
            Line(ORIGIN, dir*0.5, stroke_width=4, color=WHITE)
            for dir in [UL, UR, DL, DR]
        ]).move_to(main_gear.get_center())
        
        bearing_system = VGroup(main_gear, small_gears, axles).move_to(horse_body.get_center())
        
        # === 观察眼 ===
        eye = VGroup(
            Circle(radius=1.2, stroke_width=4, stroke_color=WHITE, fill_color="#1a1b26"),
            VGroup(
                Annulus(inner_radius=0.3, outer_radius=0.8, fill_color=BLUE_D, fill_opacity=0.7),
                Circle(radius=0.25, fill_color=BLACK)
            )
        ).next_to(horse_body, RIGHT, buff=0.5)
        
        # === 标题 ===
        title = VGroup(
            Text("@码理炼金", font="思源黑体 CN Bold", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT)
        title.move_to([0.5, -1.5, 0])  # 移动到右下方
        
        # === 动画序列 ===
        self.play(DrawBorderThenFill(horse_body), run_time=2)
        self.play(FadeIn(main_gear, scale=0.5),
                 *[FadeIn(gear, shift=dir*0.3) for gear, dir in zip(small_gears, [UL, UR, DL, DR])],
                 run_time=1.5)
        
        def update_gears(mob, dt):
            mob[0].rotate(-dt)
            for i in range(4): mob[1][i].rotate(2*dt)
        bearing_system.add_updater(update_gears)
        self.add(bearing_system)
        
        self.play(Create(eye[0]), FadeIn(eye[1], shift=DOWN), run_time=1.2)
        
        def update_eye(mob, dt):
            mob[1][1].move_to(mob[0].get_center() + np.array([0.3*np.sin(self.time), 0.2*np.cos(self.time), 0]))
        eye.add_updater(update_eye)
        
        self.play(LaggedStart(Write(title[0]), lag_ratio=0.3), run_time=1.8)
        
        # 最终光效
        light = VGroup(horse_body, bearing_system, eye).copy()
        light.set_fill(opacity=0.1).set_stroke(width=0)
        self.add(light)
        self.play(light.animate.scale(1.3).set_opacity(0), run_time=3, rate_func=there_and_back)
        self.remove(light)
        
        self.wait(3)

if __name__ == "__main__":
    scene = MechanicalHorseLogo()
    scene.render()