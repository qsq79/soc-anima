from manim import *

class OptimizedLockerAnimation(Scene):
    def construct(self):
        # 全局布局参数
        self.locker_rows = 4
        self.locker_cols = 5
        self.locker_spacing = 1.3
        self.locker_size = 1.0
        self.font_scale = 0.85
        self.animation_speed = 1.0
        
        # 场景1：优化的储物柜系统介绍
        self.show_optimized_locker_system()
        
        # 场景2：物品存储演示
        self.demonstrate_item_storage()
        
        # 场景3：内存对比
        self.show_memory_comparison()

    def show_optimized_locker_system(self):
        """展示优化布局的储物柜系统"""
        # 标题（上方留更多空间）
        title = Text("超市储物柜内存模型", font_size=42*self.font_scale)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=1*self.animation_speed)
        self.wait(0.5)
        
        # 创建储物柜网格
        lockers = self.create_optimized_lockers()
        self.play(Create(lockers), run_time=2*self.animation_speed)
        self.wait(0.5)
        
        # 分步解释说明（自动清理）
        explanations = VGroup(
            Text("1. 每个柜子有唯一编号（内存地址）", font_size=30*self.font_scale),
            Text("2. 柜子大小相同（数据类型一致）", font_size=30*self.font_scale),
            Text("3. 连续排列（内存连续性）", font_size=30*self.font_scale)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        # 定位解释文本（屏幕下方）
        explanations.next_to(lockers, DOWN, buff=1.2)
        
        # 逐个显示解释并上移淡出
        for i, explanation in enumerate(explanations):
            self.play(FadeIn(explanation), run_time=0.8*self.animation_speed)
            self.wait(0.8)
            
            if i < len(explanations)-1:  # 不是最后一条则上移淡出
                self.play(
                    explanation.animate.shift(UP*0.8).set_opacity(0.2),
                    run_time=0.7*self.animation_speed
                )
        
        # 移除所有解释
        self.play(FadeOut(explanations), run_time=0.5*self.animation_speed)
        self.wait(0.5)
        
        # 保存标题和储物柜供后续使用
        self.title = title
        self.lockers = lockers

    def create_optimized_lockers(self):
        lockers = VGroup()
        
        for i in range(self.locker_rows):
            for j in range(self.locker_cols):
                # 创建柜子方块
                box = Rectangle(
                    height=self.locker_size,
                    width=self.locker_size,
                    color=BLUE,
                    fill_opacity=0.15,
                    stroke_width=2.5
                )
                
                # 计算位置（增加间距）
                x_pos = j*self.locker_spacing - (self.locker_cols-1)*self.locker_spacing/2
                y_pos = i*self.locker_spacing - (self.locker_rows-1)*self.locker_spacing/2 + 0.3
                box.move_to([x_pos, y_pos, 0])
                
                # 创建编号（小字体，左上角偏内）- 修正括号问题
                locker_id = i*self.locker_cols + j
                num_pos = box.get_corner(UL) + np.array([0.18, -0.18, 0])
                num = Text(
                    str(locker_id), 
                    font_size=20*self.font_scale,
                    color=YELLOW
                ).move_to(num_pos)
                
                # 添加柜子和编号
                lockers.add(box, num)
    
        return lockers

    def demonstrate_item_storage(self):
        """演示物品存储过程"""
        # 更新标题
        new_title = Text("物品存储演示", font_size=40*self.font_scale, color=GREEN)
        new_title.move_to(self.title)
        self.play(Transform(self.title, new_title))
        self.wait(0.5)
        
        # 要存储的物品
        items = ["书包", "笔记本电脑", "水杯", "外套", "充电器"]
        item_count = len(items)
        
        # 显示物品列表（左侧排列）
        items_group = VGroup()
        for i, item in enumerate(items):
            text = Text(item, font_size=26*self.font_scale)
            text.move_to([-4, 2-i*0.7, 0])
            items_group.add(text)
        
        self.play(FadeIn(items_group), run_time=1*self.animation_speed)
        self.wait(0.8)
        
        # 寻找连续空间（从第2个柜子开始）
        start_idx = 2
        highlight_boxes = VGroup()
        for i in range(item_count):
            highlight = SurroundingRectangle(
                self.lockers[2*(start_idx+i)],  # 每个柜子占2个元素（box+num）
                color=YELLOW,
                buff=0.1,
                fill_opacity=0.3,
                stroke_width=3
            )
            highlight_boxes.add(highlight)
        
        # 显示高亮动画
        self.play(
            items_group.animate.shift(RIGHT*0.5).set_opacity(0.8),
            Create(highlight_boxes),
            run_time=1.5*self.animation_speed
        )
        self.wait(0.5)
        
        # 存储物品动画
        stored_items = VGroup()
        for i in range(item_count):
            item_copy = items_group[i].copy()
            locker = self.lockers[2*(start_idx+i)]  # 获取柜子方块
            self.play(
                item_copy.animate.move_to(locker).scale(0.9),
                run_time=0.7*self.animation_speed
            )
            stored_items.add(item_copy)
        
        # 显示存储信息（下方居中）
        storage_info = VGroup(
            Text(f"起始柜号: {start_idx}", font_size=28*self.font_scale),
            Text(f"存储数量: {item_count}", font_size=28*self.font_scale)
        ).arrange(RIGHT, buff=1.0).next_to(self.lockers, DOWN, buff=1.0)
        
        self.play(Write(storage_info), run_time=1*self.animation_speed)
        self.wait(1.5)
        
        # 清理临时元素
        self.play(
            FadeOut(items_group),
            FadeOut(highlight_boxes),
            run_time=0.7*self.animation_speed
        )
        self.stored_items = stored_items
        self.storage_info = storage_info

    def show_memory_comparison(self):
        """展示内存对比"""
        # 更新标题
        new_title = Text("内存存储对比", font_size=40*self.font_scale, color=ORANGE)
        new_title.move_to(self.title)
        self.play(Transform(self.title, new_title))
        self.wait(0.5)
        
        # 创建内存单元对比
        memory_cells = VGroup()
        cell_count = 8
        for i in range(cell_count):
            cell = Rectangle(
                height=0.8,
                width=1.5,
                color=GREEN,
                fill_opacity=0.2,
                stroke_width=2
            )
            cell.move_to([i*1.8 - (cell_count-1)*1.8/2, -1.5, 0])
            
            # 内存地址标签
            address = Text(f"0x{i*4:04X}", font_size=18*self.font_scale)
            address.move_to(cell.get_top() + DOWN*0.2)
            
            # 内存数据（从储物柜复制）
            if i < len(self.stored_items):
                data = self.stored_items[i].copy()
                data.scale(0.8).move_to(cell)
            else:
                data = Text("NULL", font_size=22*self.font_scale, color=GRAY).move_to(cell)
            
            memory_cells.add(cell, address, data)
        
        # 显示内存单元
        self.play(
            FadeOut(self.storage_info),
            self.stored_items.animate.set_opacity(0.3),
            run_time=0.7*self.animation_speed
        )
        self.play(Create(memory_cells), run_time=1.5*self.animation_speed)
        self.wait(1)
        
        # 对比说明
        comparison = VGroup(
            Text("储物柜系统  →  计算机内存", font_size=32*self.font_scale),
            Text("柜子编号  →  内存地址", font_size=28*self.font_scale),
            Text("存放物品  →  存储数据", font_size=28*self.font_scale),
            Text("连续柜子  →  连续内存空间", font_size=28*self.font_scale)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        comparison.next_to(memory_cells, DOWN, buff=1.0)
        
        # 逐个显示对比项
        for item in comparison:
            self.play(Write(item), run_time=0.8*self.animation_speed)
            self.wait(0.5)
        
        # 地址计算演示
        calc_text = Text(
            "地址计算: 首地址 + 索引 × 元素大小", 
            font_size=30*self.font_scale
        ).next_to(comparison, DOWN, buff=0.8)
        
        example = Text(
            "例如: 首地址0x0000 + 2 × 4 = 0x0008",
            font_size=26*self.font_scale,
            color=YELLOW
        ).next_to(calc_text, DOWN, buff=0.4)
        
        self.play(Write(calc_text), run_time=1*self.animation_speed)
        self.wait(0.8)
        self.play(Write(example), run_time=0.8*self.animation_speed)
        self.wait(2)
        
        # 最终总结
        conclusion = Text(
            "关键点: 连续存储实现高效随机访问",
            font_size=36*self.font_scale,
            color=GOLD
        ).next_to(example, DOWN, buff=1.0)
        
        self.play(Write(conclusion), run_time=1.2*self.animation_speed)
        self.wait(3)

if __name__ == "__main__":
    scene = OptimizedLockerAnimation()
    scene.render()

