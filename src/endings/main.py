import argparse
from youtube_endings import YouTubeEndScene
from bilibili_endings import BilibiliEndScene
from douyin_endings import DouyinEndScene
from education_endings import EducationEndScene

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--platform",
        choices=["youtube", "bilibili", "douyin", "edu"],
        default="youtube",
        help="选择平台类型: youtube, bilibili, douyin, edu"
    )
    args = parser.parse_args()

    if args.platform == "youtube":
        scene = YouTubeEndScene()
    elif args.platform == "bilibili":
        scene = BilibiliEndScene()
    elif args.platform == "douyin":
        scene = DouyinEndScene()
    elif args.platform == "edu":
        scene = EducationEndScene()

    scene.render()
    