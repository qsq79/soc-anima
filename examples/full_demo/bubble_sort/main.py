from algorithms.sorting.bubble.basic.basic_bubble import BubbleSort
# examples/full_demo/bubble_sort/main.py

if __name__ == "__main__":
    # 初始化配置
    config.quality = "high_quality"
    config.frame_rate = 60
    
    # 运行示例
    sample_array = [5, 3, 8, 4, 2]
    scene = BubbleSort(sample_array)
    scene.render()