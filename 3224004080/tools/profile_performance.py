"""为论文查重程序生成可重复的性能分析样本。"""

from main import calculate_similarity


def build_sample_documents() -> tuple[str, str]:
    """构造较长的原文和经过局部修改的抄袭文。"""
    paragraph = "软件工程课程要求学生完成需求分析、编码实现、单元测试和性能优化。"
    original = paragraph * 5_000
    middle = len(original) // 2
    copied = original[:middle] + "学生还需要记录开发过程并提交实验报告。" + original[middle + 30 :]
    return original, copied


def profile_target() -> float:
    """重复执行查重计算，便于性能分析器采样。"""
    original, copied = build_sample_documents()
    similarity = 0.0
    for _ in range(10):
        similarity = calculate_similarity(original, copied)
    return similarity


if __name__ == "__main__":
    print(f"模拟文本相似度：{profile_target():.2f}")
