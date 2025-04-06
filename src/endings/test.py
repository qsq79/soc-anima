from manim import *
import numpy as np
import os
import random

class TikTokEnding(Scene):
    def construct(self):
        # === 1. 动态背景 ===
        self.camera.background_color = "#010101"
        gradient = VGroup(*[
            Rectangle(width=14, height=0.5, fill_opacity=1,
                     fill_color=random.choice(["#ff0050", "#00f2ea", "#ffcc00"]))
            .shift(UP*y) for y in np.arange(-5, 5, 0.5)
        ])
        self.play(
            LaggedStart(*[FadeIn(rect) for rect in gradient],
            run_time=2, lag_ratio=0.05)
        )
        
        # === 2. 中心LOGO ===
        logo_text = Text("@科技创意秀", font="SimHei", font_size=60)  # 修改字体为系统支持的
        logo_text.set_color_by_gradient("#ff0050", "#00f2ea")
        
        assets_dir = os.path.join(os.path.dirname(__file__), "assets/svg")
        # 抖音 logo
        music_note = SVGMobject(os.path.join(assets_dir, "dou_ying.svg")).scale(0.5)
        
        # 使用新的圆形排列方法
        notes = VGroup(*[music_note.copy() for _ in range(8)])
        for i, note in enumerate(notes):
            angle = i * 2 * PI / len(notes)
            note.move_to(1.5 * np.array([np.cos(angle), np.sin(angle), 0]))
        notes.set_color_by_gradient("#ff0050", "#00f2ea")
        
        logo_group = VGroup(logo_text, notes).move_to(ORIGIN)
        
        self.play(
            DrawBorderThenFill(logo_text, run_time=1.5),
            LaggedStart(
                *[SpinInFromNothing(note, path_arc=2*PI) 
                  for note in notes],
                lag_ratio=0.2
            ),
            run_time=2
        )
        
        # === 3. 动态音符特效 ===
        def note_updater(mob, dt):
            mob.rotate(dt * 30 * DEGREES)
            for note in mob[1]:
                note.rotate(-dt * 45 * DEGREES)
        logo_group.add_updater(note_updater)
        
        # === 4. 引导关注动效 ===
        # 使用替代的手指图标
        hand = VGroup(
            Circle(radius=0.3, fill_color=WHITE, fill_opacity=1),
            Line(ORIGIN, UP*0.5, stroke_width=8)
        ).scale(0.5).next_to(logo_group, DOWN, buff=0.5)
        
        arrow = Arrow(
            start=hand.get_center(),
            end=hand.get_center() + UP,
            buff=0.2,
            stroke_width=8,
            tip_length=0.3,
            color="#ff0050"
        )
        
        follow_text = Text("点击关注看更多创意", font="SimHei", font_size=36)
        follow_text.next_to(hand, DOWN, buff=0.3)
        
        self.play(
            FadeIn(hand, shift=UP*0.5),
            GrowFromCenter(arrow),
            Write(follow_text),
            run_time=1.5
        )
        
        # === 5. 心跳脉冲效果 ===
        def pulse_animation(mob, alpha):
            mob.scale(1 + 0.1 * np.sin(alpha * 2 * PI))
        self.play(
            UpdateFromAlphaFunc(
                logo_group,
                pulse_animation,
                rate_func=there_and_back,
                run_time=1.5
            )
        )
        
        # === 6. 粒子爆发效果 ===
        def random_bright_color():
            colors = ["#ff0050", "#00f2ea", "#ffcc00", "#25f4ee", "#fe2c55"]
            return random.choice(colors)
            
        particles = VGroup(*[
            Dot(radius=0.05, color=random_bright_color())
            .move_to(logo_group.get_center())
            for _ in range(50)
        ])
        
        self.add(particles)
        self.play(
            LaggedStart(
                *[Succession(
                    UpdateFromAlphaFunc(
                        p,
                        lambda m, a: m.move_to(
                            logo_group.get_center() + 
                            rotate_vector(RIGHT*3, a*2*PI) * a
                        ).set_opacity(1-a)
                    ),
                    FadeOut(p)
                ) for p in particles],
                lag_ratio=0.02
            ),
            run_time=2
        )
        
        # === 7. 最终定格 ===
        self.play(
            Flash(logo_text, color="#ffffff", flash_radius=1.5),
            run_time=1.5
        )
        
        self.wait(3)

if __name__ == "__main__":
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    scene = TikTokEnding()
    scene.render()