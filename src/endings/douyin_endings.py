from manim import *
import os

# 定义常量，提高代码可维护性
SCALE_UP = 1.3
SCALE_DOWN = 0.8
MOVE_DISTANCE = 0.5
ANIM_DELAY = 0.1

class DouyinEndings:
    @staticmethod
    def douyin_style():
        # 竖版背景框
        background_frame = Rectangle(
            height=7, width=4,
            stroke_color=BLACK, fill_color=BLACK, fill_opacity=1
        )
        assets_dir = os.path.join(os.path.dirname(__file__), "assets/svg")
        # 抖音 logo，使用 SVGMobject 加载 SVG 文件
        douyin_logo = SVGMobject(os.path.join(assets_dir, "dou_ying.svg")).scale(0.5).to_edge(UP).shift(DOWN * 0.5)
        # like = SVGMobject(os.path.join(assets_dir, "like.svg"))
        # 红心图标
        heart = VGroup(
            Circle(radius=0.3, fill_opacity=1, color=RED).shift(LEFT * 0.3),
            Circle(radius=0.3, fill_opacity=1, color=RED).shift(RIGHT * 0.3),
            Polygon(
                [0, -0.5, 0],
                [0.6, 0.3, 0],
                [-0.6, 0.3, 0],
                fill_opacity=1,
                color=RED
            )
        ).scale(0.8).to_edge(LEFT).shift(RIGHT * 0.5)

        # 分享图标
        share_icon = VGroup(
            Circle(radius=0.3, fill_opacity=1, color=YELLOW),
            Text("分", font="思源黑体", font_size=24, color=BLACK)
        ).scale(0.8).next_to(heart, DOWN, buff=0.5)

        # 音乐图标
        music_icon = VGroup(
            Rectangle(height=0.5, width=0.2, fill_opacity=1, color=BLUE),
            Rectangle(height=0.3, width=0.2, fill_opacity=1, color=BLUE).shift(UP * 0.3)
        ).scale(0.8).next_to(share_icon, DOWN, buff=0.5)

        # 引导关注文本
        follow_text = Text("关注我，更多精彩等你", font="思源黑体").scale(0.6).to_edge(DOWN).shift(UP * 0.5)

        # 动画列表
        anims = [
            douyin_logo.animate.scale(SCALE_UP),
            heart.animate.scale(SCALE_UP),
            share_icon.animate.scale(SCALE_UP),
            music_icon.animate.scale(SCALE_UP),
            follow_text.animate.shift(UP * MOVE_DISTANCE),
            LaggedStart(
                heart.animate.scale(SCALE_DOWN),
                share_icon.animate.scale(SCALE_DOWN),
                music_icon.animate.scale(SCALE_DOWN),
                lag_ratio=ANIM_DELAY
            )
        ]

        return VGroup(background_frame, douyin_logo, heart, share_icon, music_icon, follow_text), anims

class DouyinEndScene(Scene):
    def construct(self):
        self.camera.frame_width = 4  # 竖版适配
        self.camera.frame_height = 7
        # 获取动画元素和动画列表
        group, anims = DouyinEndings.douyin_style()
        # 淡入动画元素
        self.play(FadeIn(group))
        # 播放动画列表中的动画
        self.play(*anims)
        # 等待 2 秒
        self.wait(2)

if __name__ == "__main__":
    # 创建抖音结尾动画场景
    scene = DouyinEndScene()
    # 渲染场景
    scene.render()
    