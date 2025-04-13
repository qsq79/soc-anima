import sys
# 使用原始字符串设置路径
sys.path.append(r"D:\\algorithm-animation\soc-anima")

from manim import *

class MemoryExplanation(Scene): 
    def construct(self):
        # 标题
        title = Text("计算机内存工作原理", font_size=48)
        subtitle = Text("(以超市储物柜为例)", font_size=36).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # 介绍超市储物柜
        locker_title = Text("超市储物柜系统", font_size=40)
        self.play(Write(locker_title))
        self.wait(1)
        self.play(locker_title.animate.to_edge(UP))
        
        # 创建储物柜图示 - 优化编号位置
        locker = VGroup()
        rows, cols = 4, 5
        for i in range(rows):
            for j in range(cols):
                box = Rectangle(height=1, width=1, color=BLUE)
                box.move_to([j*1.2 - (cols-1)*1.2/2, i*1.2 - (rows-1)*1.2/2 + 0.5, 0])
                # 将编号缩小并移动到左上角
                num = Text(str(i*cols + j), font_size=18).move_to(
                    box.get_corner(UL) + DOWN*0.15 + RIGHT*0.15
                )
                locker.add(box, num)
        
        self.play(Create(locker), run_time=2)
        self.wait(1)
        
        # 解释储物柜编号
        address_explanation = Text("每个柜子有唯一编号(内存地址)", font_size=30)
        address_explanation.next_to(locker, DOWN)
        self.play(Write(address_explanation))
        self.wait(2)
        
        # 展示存储物品 - 现在不会与编号重叠
        items = ["包", "外套", "手机", "钱包", "书", "雨伞", "钥匙"]
        stored_items = []
        for i, item in enumerate(items[:5]):
            # 物品文字放在格子中央，字号稍大
            item_text = Text(item, font_size=28).move_to(locker[2*i])
            stored_items.append(item_text)
            self.play(FadeIn(item_text), run_time=0.5)
        
        self.wait(1)
        
        # 解释存储数据
        data_explanation = Text("柜子中可以存放物品(存储数据)", font_size=30)
        data_explanation.next_to(address_explanation, DOWN)
        self.play(Write(data_explanation))
        self.wait(2)
        self.play(FadeOut(data_explanation), FadeOut(address_explanation))
        
        # 展示取物品过程
        pointer = Arrow(ORIGIN, UP*0.5, color=YELLOW).next_to(locker[0], DOWN)
        pointer_label = Text("内存指针", font_size=30).next_to(locker, DOWN)
        self.play(GrowArrow(pointer), Write(pointer_label))
        self.wait(1)
        
        # 指针移动到3号柜子
        self.play(pointer.animate.next_to(locker[6], DOWN))
        self.wait(1)
        
        # 取出物品
        phone = stored_items[1].copy()
        self.play(phone.animate.move_to(UP*2 + LEFT*5))
        access_explanation = Text("通过地址(1)访问对应柜子中的数据", font_size=30)
        access_explanation.next_to(address_explanation, DOWN)
        self.play(Write(access_explanation))
        self.wait(2)
        
        # 清理场景
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # 对比计算机内存 - 同样优化编号位置
        computer_title = Text("计算机内存系统", font_size=40)
        self.play(Write(computer_title))
        self.wait(1)
        self.play(computer_title.animate.to_edge(UP))
        
        # 创建内存单元图示 - 优化编号位置
        memory = VGroup()
        for i in range(rows):
            for j in range(cols):
                box = Rectangle(height=1, width=1, color=GREEN)
                box.move_to([j*1.2 - (cols-1)*1.2/2, i*1.2 - (rows-1)*1.2/2 + 0.5, 0])
                # 将地址缩小并移动到左上角
                addr = Text(f"0x{i*cols + j:02X}", font_size=16).move_to(
                    box.get_corner(UL) + DOWN*0.15 + RIGHT*0.25
                )
                memory.add(box, addr)
        
        self.play(Create(memory), run_time=2)
        self.wait(1)
        
        # 展示内存中的数据 - 现在不会与地址重叠
        data_values = ["0101", "1100", "0011", "1010", "1111", "0000", "1001"]
        stored_data = []
        for i, value in enumerate(data_values[:5]):
            # 数据放在格子中央，字号稍大
            data_text = Text(value, font_size=28).move_to(memory[2*i])
            stored_data.append(data_text)
            self.play(FadeIn(data_text), run_time=0.5)
        
        # 类比解释
        analogy1 = Text("储物柜编号 → 内存地址", font_size=30)
        analogy2 = Text("存放的物品 → 存储的数据", font_size=30)
        analogy3 = Text("取物品 → 内存读写操作", font_size=30)
        
        analogy_group = VGroup(analogy1, analogy2, analogy3).arrange(DOWN, aligned_edge=LEFT)
        analogy_group.next_to(memory, DOWN)
        
        self.play(Write(analogy1))
        self.wait(1)
        self.play(Write(analogy2))
        self.wait(1)
        self.play(Write(analogy3))
        self.wait(3)
        
        # 总结
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        conclusion = Text("内存就像储物柜系统:", font_size=36)
        bullet1 = Text("- 每个位置有唯一地址", font_size=32)
        bullet2 = Text("- 通过地址访问数据", font_size=32)
        bullet3 = Text("- 可以读取或写入数据", font_size=32)
        
        conclusion_group = VGroup(conclusion, bullet1, bullet2, bullet3).arrange(DOWN, aligned_edge=LEFT)
        conclusion_group.move_to(ORIGIN)
        
        self.play(Write(conclusion))
        self.wait(1)
        self.play(Write(bullet1))
        self.wait(0.5)
        self.play(Write(bullet2))
        self.wait(0.5)
        self.play(Write(bullet3))
        self.wait(3)


if __name__ == "__main__":
    # 初始化配置
    config.quality = "high_quality"
    config.frame_rate = 60
    
    # 运行示例
    scene = MemoryExplanation()
    scene.render()