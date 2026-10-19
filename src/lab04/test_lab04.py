"""Автоматические тесты лабораторной работы 4 (стандартная библиотека)."""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.lab04.io_txt_csv import ensure_parent_dir, read_text, write_csv
from src.lab04.text_report import create_report

ROOT = Path(__file__).resolve().parents[2]


class TestReadText(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def test_utf8(self) -> None:
        path = self.folder / "russian.txt"
        path.write_text("Привет, мир!", encoding="utf-8")
        self.assertEqual(read_text(path), "Привет, мир!")

    def test_empty_file(self) -> None:
        path = self.folder / "empty.txt"
        path.write_text("", encoding="utf-8")
        self.assertEqual(read_text(path), "")

    def test_cp1251(self) -> None:
        path = self.folder / "cp1251.txt"
        path.write_bytes("Привет".encode("cp1251"))
        self.assertEqual(read_text(path, encoding="cp1251"), "Привет")

    def test_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_text(self.folder / "missing.txt")

    def test_bad_encoding(self) -> None:
        path = self.folder / "cp1251.txt"
        path.write_bytes("Привет".encode("cp1251"))
        with self.assertRaises(UnicodeDecodeError):
            read_text(path, encoding="utf-8")


class TestWriteCsv(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.file = self.folder / "report.csv"

    def rows(self) -> list[list[str]]:
        with self.file.open(newline="", encoding="utf-8") as stream:
            return list(csv.reader(stream))

    def test_header_and_data(self) -> None:
        write_csv([("привет", 2), ("мир", 1)], self.file, ("word", "count"))
        self.assertEqual(self.rows(), [["word", "count"], ["привет", "2"], ["мир", "1"]])

    def test_without_header(self) -> None:
        write_csv([("слово", 5)], self.file)
        self.assertEqual(self.rows(), [["слово", "5"]])

    def test_empty_without_header(self) -> None:
        write_csv([], self.file)
        self.assertEqual(self.file.stat().st_size, 0)

    def test_empty_with_header(self) -> None:
        write_csv([], self.file, ("word", "count"))
        self.assertEqual(self.rows(), [["word", "count"]])

    def test_mixed_row_lengths(self) -> None:
        with self.assertRaises(ValueError):
            write_csv([("a", 2), ("b", 3, 4)], self.file)

    def test_row_vs_header_mismatch(self) -> None:
        with self.assertRaises(ValueError):
            write_csv([("one", 2, "extra")], self.file, ("word", "count"))

    def test_does_not_overwrite_on_validation_error(self) -> None:
        self.file.write_text("old content", encoding="utf-8")
        with self.assertRaises(ValueError):
            write_csv([("a", 1), ("b",)], self.file)
        self.assertEqual(self.file.read_text(encoding="utf-8"), "old content")

    def test_commas_and_quotation_marks(self) -> None:
        write_csv([('a,"b"', 1)], self.file)
        self.assertEqual(self.rows(), [['a,"b"', '1']])

    def test_creates_parent_directory(self) -> None:
        path = self.folder / "nested" / "dir" / "result.csv"
        write_csv([("a", 1)], path)
        self.assertTrue(path.is_file())

    def test_ensure_parent_dir_idempotent(self) -> None:
        path = self.folder / "one" / "two" / "file.txt"
        ensure_parent_dir(path)
        ensure_parent_dir(path)
        self.assertTrue(path.parent.is_dir())


class TestTextReport(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.input = self.folder / "input.txt"
        self.output = self.folder / "reports" / "report.csv"

    def csv_rows(self) -> list[list[str]]:
        with self.output.open(newline="", encoding="utf-8") as stream:
            return list(csv.reader(stream))

    def test_example(self) -> None:
        self.input.write_text("Привет, мир! Привет!!!", encoding="utf-8")
        result = create_report(self.input, self.output)
        self.assertEqual(result, (3, 2, [("привет", 2), ("мир", 1)]))
        self.assertEqual(self.csv_rows(), [["word", "count"], ["привет", "2"], ["мир", "1"]])

    def test_empty_text(self) -> None:
        self.input.write_text("", encoding="utf-8")
        self.assertEqual(create_report(self.input, self.output), (0, 0, []))
        self.assertEqual(self.csv_rows(), [["word", "count"]])

    def test_sort_ties_alphabetically(self) -> None:
        self.input.write_text("банан арбуз банан арбуз кот", encoding="utf-8")
        create_report(self.input, self.output)
        self.assertEqual(self.csv_rows(), [["word", "count"], ["арбуз", "2"], ["банан", "2"], ["кот", "1"]])

    def test_yo_and_hyphens(self) -> None:
        self.input.write_text("Ёжик ёжик кто-то!", encoding="utf-8")
        self.assertEqual(create_report(self.input, self.output),
                         (3, 2, [("ежик", 2), ("кто-то", 1)]))

    def test_cp1251_input(self) -> None:
        self.input.write_bytes("Привет".encode("cp1251"))
        self.assertEqual(create_report(self.input, self.output, encoding="cp1251"),
                         (1, 1, [("привет", 1)]))

    def test_cli_module(self) -> None:
        self.input.write_text("Мир, мир!", encoding="utf-8")
        completed = subprocess.run([sys.executable, "-m", "src.lab04.text_report",
                                   "--in", str(self.input), "--out", str(self.output)],
                                  cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "Всего слов: 2\nУникальных слов: 1\nТоп-5:\nмир:2\n")
        self.assertEqual(self.csv_rows(), [["word", "count"], ["мир", "2"]])

    def test_cli_direct_script(self) -> None:
        self.input.write_text("Кот кот", encoding="utf-8")
        completed = subprocess.run([sys.executable, "src/lab04/text_report.py",
                                   "--in", str(self.input), "--out", str(self.output)],
                                  cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(self.csv_rows(), [["word", "count"], ["кот", "2"]])

    def test_cli_missing_file(self) -> None:
        completed = subprocess.run([sys.executable, "-m", "src.lab04.text_report",
                                   "--in", str(self.input), "--out", str(self.output)],
                                  cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("Ошибка", completed.stderr)
        self.assertFalse(self.output.exists())

    def test_cli_cp1251(self) -> None:
        self.input.write_bytes("Привет".encode("cp1251"))
        completed = subprocess.run([sys.executable, "-m", "src.lab04.text_report",
                                   "--in", str(self.input), "--out", str(self.output),
                                   "--encoding", "cp1251"],
                                  cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(self.csv_rows(), [["word", "count"], ["привет", "1"]])


if __name__ == "__main__":
    unittest.main()
