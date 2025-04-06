from manim import *
import argparse

class PlatformEndings:
    """不同平台的结尾动画组件库"""
    @staticmethod
    def youtube_style():
        # YouTube专业风格
        logo = SVGMobject("logo.svg").scale(0.8)
        sub_button = RoundedRectangle(
            corner_radius=0.2,
            height=0.8, width=2.5,
            fill_color=RED, fill_opacity=1,
            stroke_color=WHITE, stroke_width=2
        )
        sub_text = Text("订阅", font="思源黑体").scale(0.7)
        sub_group = VGroup(sub_button, sub_text)
        
        bell = SVGMobject("bell.svg").next_to(sub_group, RIGHT, buff=0.5)
        
        anims = [
            logo.animate.scale(1.1).set_color([BLUE, WHITE]),
            sub_group.animate.shift(DOWN),
            bell.animate.rotate(PI/4, rate_func=there_and_back)
        ]
        return VGroup(logo, sub_group, bell), anims

    @staticmethod
    def bilibili_style():
        # B站活泼风格
        logo = Text("码理可视", font="思源黑体").scale(1.2)
        sanlian = VGroup(
            SVGMobject("like.svg").set_color(BLUE),
            SVGMobject("coin.svg").set_color(YELLOW),
            SVGMobject("collect.svg").set_color(PINK)
        ).arrange(RIGHT, buff=1)
        
        # 弹幕元素
        danmu = VGroup(
            Text("讲得真好！", color=GREEN),
            Text("三连了", color=YELLOW),
            Text("下次讲红黑树吗？", color=PINK)
        ).arrange(DOWN, buff=0.3).to_edge(UP)
        
        anims = [
            logo.animate.shift(UP),
            LaggedStart(
                *[obj.animate.scale(1.5) for obj in sanlian],
                lag_ratio=0.2
            ),
            danmu.animate.shift(LEFT*5)
        ]
        return VGroup(logo, sanlian, danmu), anims

    @staticmethod
    def douyin_style():
        # 抖音竖版风格
        phone_frame = Rectangle(
            height=6, width=3.5,
            stroke_color=WHITE, stroke_width=3
        )
        qr_code = Square(side_length=1.5).set_fill(WHITE, opacity=1)
        follow_text = Text("关注我", font="思源黑体").scale(0.8)
        heart = SVGMobject("heart.svg").set_color(RED)
        
        anims = [
            qr_code.animate.shift(UP*0.5),
            follow_text.animate.shift(DOWN*0.5),
            heart.animate.scale(1.5).set_opacity(0)
        ]
        return VGroup(phone_frame, qr_code, follow_text, heart), anims

class CustomEndScene(Scene):
    def __init__(self, platform="bilibili", **kwargs):
        self.platform = platform
        super().__init__(**kwargs)

    def construct(self):
        if self.platform == "youtube":
            group, anims = PlatformEndings.youtube_style()
        elif self.platform == "bilibili":
            group, anims = PlatformEndings.bilibili_style()
        elif self.platform == "douyin":
            self.camera.frame_width = 4  # 竖版适配
            self.camera.frame_height = 7
            group, anims = PlatformEndings.douyin_style()
        else:  # 教育平台
            group, anims = self.education_style()
        
        self.play(FadeIn(group))
        self.play(*anims)
        self.wait(2)
    
    def education_style(self):
        # 教育平台风格
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
            courses.animate.shift(LEFT*3),
            contact.animate.shift(RIGHT*3)
        ]
        return VGroup(title, courses, contact), anims

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--platform",
        choices=["youtube", "bilibili", "douyin", "edu"],
        default="youtube",
        help="选择平台类型: youtube, bilibili, douyin, edu"
    )
    args = parser.parse_args()
    
    # 渲染对应平台动画
    scene = CustomEndScene(platform=args.platform)
    scene.render()
