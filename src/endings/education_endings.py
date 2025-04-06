from manim import *

class EducationEndings:
    @staticmethod
    def education_style():
        title = Text("系列课程推荐", font="思源黑体").to_edge(UP)
        courses = BulletedList(
            "数据结构基础",
            "算法精讲",
            "面试专题",
            height=3, width=5
        )
        contact = Text("讲师: 码理可视\n联系: contact@malike.com", font_size=24)

        anims = [
            title.animate.set_color(BLUE),
            courses.animate.shift(LEFT * 3),
            contact.animate.shift(RIGHT * 3)
        ]
        return VGroup(title, courses, contact), anims

class EducationEndScene(Scene):
    def construct(self):
        group, anims = EducationEndings.education_style()
        self.play(FadeIn(group))
        self.play(*anims)
        self.wait(2)
    