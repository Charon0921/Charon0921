"""main.py 的单元测试。"""

import tempfile
import unittest
from pathlib import Path

import main


class SimilarityTests(unittest.TestCase):
    """覆盖文本相似度计算和命令行入口的测试集合。"""

    def test_identical_texts_have_full_similarity(self):
        """相同文本的相似度应为一。"""
        self.assertEqual(main.calculate_similarity("今天是星期天", "今天是星期天"), 1.0)

    def test_completely_different_texts_have_zero_similarity(self):
        """完全不同文本的相似度应为零。"""
        self.assertEqual(main.calculate_similarity("甲乙丙丁", "戊己庚辛"), 0.0)

    def test_both_empty_texts_are_identical(self):
        """两个空文本视作相同。"""
        self.assertEqual(main.calculate_similarity("", ""), 1.0)

    def test_empty_original_has_zero_similarity(self):
        """空原文与非空文本的相似度应为零。"""
        self.assertEqual(main.calculate_similarity("", "论文内容"), 0.0)

    def test_empty_copied_text_has_zero_similarity(self):
        """非空原文与空抄袭文的相似度应为零。"""
        self.assertEqual(main.calculate_similarity("论文内容", ""), 0.0)

    def test_punctuation_and_spaces_do_not_change_similarity(self):
        """标点和空格不应影响相似度。"""
        original = "今天，天气很好！"
        copied = "今天 天气很好"
        self.assertEqual(main.calculate_similarity(original, copied), 1.0)

    def test_newlines_do_not_change_similarity(self):
        """换行不应影响相似度。"""
        self.assertEqual(main.calculate_similarity("第一行\n第二行", "第一行第二行"), 1.0)

    def test_same_single_character_is_similar(self):
        """相同单字符文本的相似度应为一。"""
        self.assertEqual(main.calculate_similarity("好", "好"), 1.0)

    def test_different_single_characters_are_not_similar(self):
        """不同单字符文本的相似度应为零。"""
        self.assertEqual(main.calculate_similarity("好", "坏"), 0.0)

    def test_small_edit_keeps_partial_similarity(self):
        """少量改动后的文本应保留部分相似度。"""
        similarity = main.calculate_similarity("今天晚上去看电影", "今天晚上要看电影")
        self.assertGreater(similarity, 0.0)
        self.assertLess(similarity, 1.0)

    def test_english_and_numbers_are_compared(self):
        """英文和数字应参与比较。"""
        self.assertEqual(main.calculate_similarity("Python 3.13", "Python313"), 1.0)

    def test_main_writes_a_two_decimal_answer_file(self):
        """命令行入口应写入保留两位小数的答案。"""
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            original = folder / "original.txt"
            copied = folder / "copied.txt"
            answer = folder / "answer.txt"
            original.write_text("相同的论文内容", encoding="utf-8")
            copied.write_text("相同的论文内容", encoding="utf-8")

            status = main.main([str(original), str(copied), str(answer)])

            self.assertEqual(status, 0)
            self.assertEqual(answer.read_text(encoding="utf-8"), "1.00\n")

    def test_main_rejects_wrong_argument_count(self):
        """命令行参数数量错误时应返回错误状态。"""
        self.assertEqual(main.main([]), 2)


if __name__ == "__main__":
    unittest.main()
