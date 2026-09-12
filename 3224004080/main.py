"""论文查重程序：比较两个文本文件并把相似度写入指定文件。"""

from __future__ import annotations

import sys
from pathlib import Path


NGRAM_SIZE = 2


def read_text(path: str) -> str:
    """读取常见编码的文本文件。"""
    file_path = Path(path)
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return file_path.read_text(encoding="utf-8")


def normalize_text(text: str) -> str:
    """去除空白和标点，只保留中英文字符及数字。"""
    return "".join(character for character in text if character.isalnum())


def build_ngrams(text: str, size: int = NGRAM_SIZE) -> set[str]:
    """将文本切分为连续字符片段；极短文本本身视作一个片段。"""
    if not text:
        return set()
    if len(text) < size:
        return {text}
    return {text[index : index + size] for index in range(len(text) - size + 1)}


def calculate_similarity(original: str, copied: str) -> float:
    """使用字符二元片段集合的 Jaccard 相似度计算重复率。"""
    original_ngrams = build_ngrams(normalize_text(original))
    copied_ngrams = build_ngrams(normalize_text(copied))

    if not original_ngrams and not copied_ngrams:
        return 1.0
    if not original_ngrams or not copied_ngrams:
        return 0.0

    return len(original_ngrams & copied_ngrams) / len(original_ngrams | copied_ngrams)


def main(arguments: list[str]) -> int:
    if len(arguments) != 3:
        print("用法: python main.py 原文路径 抄袭文路径 答案路径", file=sys.stderr)
        return 2

    original_path, copied_path, answer_path = arguments
    similarity = calculate_similarity(read_text(original_path), read_text(copied_path))
    Path(answer_path).write_text(f"{similarity:.2f}\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
