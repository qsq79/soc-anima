from manim import *

class YouTubeEndings:
    @staticmethod
    def youtube_style():
        logo = Text("码理可视", font="思源黑体").scale(0.8)

        sub_button = RoundedRectangle(
            corner_radius=0.2,
            height=0.8, width=2.5,
            fill_color=RED, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2
        )
        sub_text = Text("订阅", font="思源黑体").scale(0.7)
        sub_group = VGroup(sub_button, sub_text)

        bell_body = Circle(radius=0.4, fill_color=WHITE, fill_opacity=1)
        bell_top = ArcBetweenPoints(
            start=[-0.3, 0.4, 0],
            end=[0.3, 0.4, 0],
            angle=PI / 3
        ).set_stroke(WHITE, width=8)
        bell_clapper = Line(
            start=[0, -0.3, 0],
            end=[0, -0.5, 0],
            stroke_width=4
        )
        bell = VGroup(bell_body, bell_top, bell_clapper).next_to(sub_group, RIGHT, buff=0.5)

        anims = [
            logo.animate.scale(1.1).set_color([BLUE, WHITE]),
            sub_group.animate.shift(DOWN),
            Rotate(bell, angle=PI / 4, rate_func=there_and_back)
        ]
        return VGroup(logo, sub_group, bell), anims

class YouTubeEndScene(Scene):
    def construct(self):
        group, anims = YouTubeEndings.youtube_style()
        self.play(FadeIn(group))
        self.play(*anims)
        self.wait(2)
    
