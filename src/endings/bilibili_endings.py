from manim import *
import os

class BilibiliEndScene(Scene):
    def construct(self):
        # =============== 第一部分：突出标题和互动按钮 ===============
        # 1. 主标题
        logo = Text("@码理炼金", font="思源黑体", font_size=80, color=WHITE)
        logo.to_edge(UP, buff=0.9).set_color_by_gradient(BLUE_A, BLUE_D)
        
        # 2. 互动图标
        assets_dir = os.path.join(os.path.dirname(__file__), "assets/svg")
        try:
            like = SVGMobject(os.path.join(assets_dir, "like.svg"))
            coin = SVGMobject(os.path.join(assets_dir, "coin.svg"))
            collect = SVGMobject(os.path.join(assets_dir, "collect.svg"))
            share = SVGMobject(os.path.join(assets_dir, "share.svg"))
            
            icons = VGroup(like, coin, collect, share)
            icons.set_color_by_gradient(BLUE, YELLOW, PINK, GREEN)
            icons.scale(0.7).arrange(RIGHT, buff=0.8).next_to(logo, DOWN, buff=1.0)
            
            hands = SVGMobject(os.path.join(assets_dir, "please.svg"))
            hands.set_color_by_gradient(GOLD_A, GOLD_E).scale(0.6)
            
        except Exception as e:
            print(f"SVG加载错误: {e}")
            icons = VGroup(
                Circle(radius=0.5, fill_color=BLUE, fill_opacity=1),
                Square(side_length=0.8, fill_color=YELLOW, fill_opacity=1),
                Star(n=5, fill_color=PINK, fill_opacity=1),
                Triangle(fill_color=GREEN, fill_opacity=1)
            ).arrange(RIGHT, buff=1.0).scale(1.2)
            
            hands = VGroup(
                Polygon([-1,0,0], [-0.5,0.5,0], [-0.5,-0.5,0], fill_color=GOLD_A),
                Polygon([1,0,0], [0.5,0.5,0], [0.5,-0.5,0], fill_color=GOLD_E)
            ).scale(0.5)

        # =============== 第二部分：底部元素 ===============
        # 1. "求求了"文字
        beg_text = Text("求求了", font="思源黑体", font_size=40, color=GOLD_C)
        beg_text.move_to(DOWN*0.6)
        
        # 2. 手掌位置
        hands.next_to(beg_text, DOWN, buff=0.3)
        
        # 3. 关注文字
        follow_text = Text("点关注，不迷路", font="思源黑体", font_size=32, color=BLUE_C)
        follow_text.next_to(hands, DOWN, buff=0.5)
        
        # 将底部元素组合成一个组
        bottom_group = VGroup(beg_text, hands, follow_text)
        
        # =============== 动画序列 ===============
        # 第一阶段：强调标题和图标
        self.play(
            DrawBorderThenFill(logo, run_time=1.5),
            LaggedStart(
                *[GrowFromCenter(icon) for icon in icons],
                lag_ratio=0.2
            ),
            run_time=2.5
        )
        
        # 第二阶段：图标脉冲动画
        for icon in icons:
            self.play(
                icon.animate.scale(1.3).set_opacity(0.8),
                rate_func=there_and_back,
                run_time=0.8
            )
        
        # 第三阶段：同时显示所有底部元素
        self.play(
            FadeIn(bottom_group, shift=UP*0.5),
            run_time=1.5
        )
        
        # 第四阶段：手掌合十动画作为结尾（循环3次）
        for _ in range(3):
            self.play(
                hands.animate.scale(1.1).set_color_by_gradient(GOLD_E, PINK),
                follow_text.animate.set_color(WHITE),  # 同时文字变白
                rate_func=there_and_back,
                run_time=0.8
            )
            self.play(
                hands.animate.set_color_by_gradient(GOLD_A, GOLD_E),
                follow_text.animate.set_color(BLUE_C),
                run_time=0.4
            )
        
        self.wait(2)

if __name__ == "__main__":
    scene = BilibiliEndScene()
    scene.render()