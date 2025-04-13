import sys
import os

# 自动获取项目根目录（无论从哪里运行）
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../.."))  # 根据实际层级调整
sys.path.append(project_root)

from src.algorithms.data_structures.memory.memory_explanation import MemoryExplanation
from manim import config
# examples/full_demo/bubble_sort/main.py

if __name__ == "__main__":
    # 初始化配置
    config.quality = "high_quality"
    config.frame_rate = 60
    
    # 运行示例
    scene = MemoryExplanation()
    scene.render()