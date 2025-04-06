from manim import *

class CodeTheoryLogo(Scene):
    def construct(self):
        # 配置
        self.camera.background_color = "#282a36"  # 深色背景
        
        # 1. 创建代码符号元素
        code_bracket = Text("<>", font_size=120, font="Roboto Mono")
        code_icon = VGroup(
            Square(side_length=0.8, fill_opacity=0, stroke_width=8),
            Triangle(fill_opacity=1, fill_color=BLUE).scale(0.3).shift(LEFT*0.2 + UP*0.2),
            Dot(color=RED, radius=0.08).shift(RIGHT*0.2 + UP*0.2),
            Dot(color=YELLOW, radius=0.08).shift(LEFT*0.2 + DOWN*0.2),
            Dot(color=GREEN, radius=0.08).shift(RIGHT*0.2 + DOWN*0.2)
        )
        
        # 2. 创建眼睛元素
        eye_outline = Circle(radius=1, stroke_width=8, stroke_color=WHITE, fill_color="#2962FF", fill_opacity=0.3)
        eye_pupil = VGroup(
            Circle(radius=0.4, fill_color=WHITE, fill_opacity=1),
            Circle(radius=0.15, fill_color=BLACK).shift(UR*0.2)
        )
        eye = VGroup(eye_outline, eye_pupil)
        
        # 3. 文字元素
        name_cn = Text("@码理炼金", font="思源黑体 CN Heavy", font_size=48)
        # name_en = Text("Code Alchemy", font="Roboto Mono", font_size=36)
        text_group = VGroup(name_cn).arrange(DOWN, center=False, aligned_edge=LEFT)
        
        # 4. 组合布局
        logo = VGroup(code_icon, eye, text_group).arrange(RIGHT, buff=0.8)
        logo.move_to(ORIGIN)
        
        # 5. 动画序列
        # 代码图标动画
        self.play(
            GrowFromCenter(code_icon[0]),
            FadeIn(code_icon[1]),
            FadeIn(code_icon[2]),
            FadeIn(code_icon[3]),
            FadeIn(code_icon[4]),
            run_time=1.5
        )
        
        # 眼睛动画
        self.play(
            Create(eye_outline),
            DrawBorderThenFill(eye_pupil),
            run_time=1.2
        )
        
        # 文字动画
        self.play(
            Write(name_cn),
            # Write(name_en),
            run_time=1.5
        )
        
        # 整体发光效果
        glow = logo.copy()
        glow.set_fill(opacity=0.1).set_stroke(width=0)
        glow.scale(1.2)
        self.add(glow)
        self.play(
            glow.animate.scale(1.3).set_opacity(0),
            run_time=2,
            rate_func=there_and_back
        )
        self.remove(glow)
        
        self.wait(2)

if __name__ == "__main__":
    scene = CodeTheoryLogo()
    scene.render()