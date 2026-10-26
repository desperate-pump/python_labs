"""Компактная проверка трёх конвертаций и обязательных граничных случаев."""

import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from openpyxl import load_workbook

from src.lab05.csv_xlsx import csv_to_xlsx
from src.lab05.json_csv import csv_to_json, json_to_csv


class TestLab05(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.json = self.folder / "people.json"
        self.csv = self.folder / "people.csv"
        self.xlsx = self.folder / "people.xlsx"

    def test_json_to_csv_sorted_columns(self) -> None:
        data = [{"name": "Анна", "age": 18, "score": 4.5, "active": True}]
        self.json.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        json_to_csv(str(self.json), str(self.csv))
        with self.csv.open(encoding="utf-8", newline="") as file:
            self.assertEqual(list(csv.reader(file)), [
                ["active", "age", "name", "score"], ["True", "18", "Анна", "4.5"],
            ])

    def test_json_to_csv_missing_fields(self) -> None:
        self.json.write_text('[{"name": "Анна"}, {"age": 19}, {}]', encoding="utf-8")
        json_to_csv(str(self.json), str(self.csv))
        with self.csv.open(encoding="utf-8", newline="") as file:
            self.assertEqual(list(csv.reader(file)), [
                ["age", "name"], ["", "Анна"], ["19", ""], ["", ""],
            ])

    def test_csv_to_json_keeps_strings_and_format(self) -> None:
        self.csv.write_text("name,code,active,empty\nАнна,001,true,\n", encoding="utf-8")
        csv_to_json(str(self.csv), str(self.json))
        text = self.json.read_text(encoding="utf-8")
        self.assertEqual(json.loads(text), [
            {"name": "Анна", "code": "001", "active": "true", "empty": ""},
        ])
        self.assertIn('  {\n    "name": "Анна"', text)
        self.assertNotIn("\\u", text)

    def test_round_trip_cyrillic_commas_quotes_and_newlines(self) -> None:
        data = [{"name": 'Мария, "Маша"', "note": "Привет\nмир"},
                {"name": "Тимур", "note": ""}]
        self.json.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        json_to_csv(str(self.json), str(self.csv))
        csv_to_json(str(self.csv), str(self.json))
        self.assertEqual(json.loads(self.json.read_text(encoding="utf-8")), data)

    def test_empty_and_unsupported_json(self) -> None:
        for text in ("", "  \n", "{", "{}", "[]", "[1]", "[{}]"):
            with self.subTest(text=text):
                self.json.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    json_to_csv(str(self.json), str(self.csv))
                self.assertFalse(self.csv.exists())

    def test_json_rejects_lossy_values_and_bad_keys(self) -> None:
        texts = [json.dumps([{"value": value}])
                 for value in (None, [], {}, float("nan"), float("inf"))]
        texts += ['[{"": 1}]', '[{"name": "Анна", "name": "Тимур"}]']
        self.csv.write_text("старые данные", encoding="utf-8")
        for text in texts:
            with self.subTest(text=text):
                self.json.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    json_to_csv(str(self.json), str(self.csv))
                self.assertEqual(self.csv.read_text(encoding="utf-8"), "старые данные")

    def test_invalid_csv_for_both_converters(self) -> None:
        for text in ("", "\n", "name,\n", "name,name\n", "  \n",
                     "name,age\nАнна\n", "name,age\nАнна,18,Москва\n",
                     'name,age\n"Анна,18\n'):
            for converter, target in ((csv_to_json, self.json), (csv_to_xlsx, self.xlsx)):
                with self.subTest(text=text, converter=converter.__name__):
                    self.csv.write_text(text, encoding="utf-8")
                    target.write_bytes(b"old output")
                    with self.assertRaises(ValueError):
                        converter(str(self.csv), str(target))
                    self.assertEqual(target.read_bytes(), b"old output")

    def test_missing_wrong_type_and_invalid_utf8(self) -> None:
        cases = ((json_to_csv, self.json, self.csv, '[{"name": "Анна"}]'),
                 (csv_to_json, self.csv, self.json, "name\nАнна\n"),
                 (csv_to_xlsx, self.csv, self.xlsx, "name\nАнна\n"))
        for converter, source, target, valid in cases:
            with self.subTest(converter=converter.__name__):
                with self.assertRaises(FileNotFoundError):
                    converter(str(self.folder / ("missing" + source.suffix)), str(target))
                wrong = self.folder / "wrong.txt"
                wrong.write_text(valid, encoding="utf-8")
                with self.assertRaises(ValueError):
                    converter(str(wrong), str(target))
                source.write_text(valid, encoding="utf-8")
                with self.assertRaises(ValueError):
                    converter(str(source), str(self.folder / "output.txt"))
                with self.assertRaises(ValueError):
                    converter(str(self.folder), str(target))
                source.write_bytes(b"\xff\xfe")
                with self.assertRaises(UnicodeDecodeError):
                    converter(str(source), str(target))

    def test_header_only_csv_is_valid(self) -> None:
        for text in ("name", "name\n", "name\n\n"):
            with self.subTest(text=text):
                self.csv.write_text(text, encoding="utf-8")
                csv_to_json(str(self.csv), str(self.json))
                self.assertEqual(json.loads(self.json.read_text(encoding="utf-8")), [])
                csv_to_xlsx(str(self.csv), str(self.xlsx))
                wb = load_workbook(self.xlsx)
                try:
                    self.assertEqual(wb.sheetnames, ["Sheet1"])
                    self.assertEqual(list(wb.active.values), [("name",)])
                    self.assertEqual(wb.active.column_dimensions["A"].width, 8)
                finally:
                    wb.close()

    def test_xlsx_opens_preserves_text_and_sets_widths(self) -> None:
        rows = [["code", "name", "note"],
                ["001", 'Мария, "Маша"', "=1+1"],
                ["002", "Тимур", "#N/A"], ["003", "Анна", ""],
                ["004", "Иван", "a" * 300]]
        with self.csv.open("w", encoding="utf-8", newline="") as file:
            csv.writer(file).writerows(rows)
        csv_to_xlsx(str(self.csv), str(self.xlsx))
        wb = load_workbook(self.xlsx, data_only=False)
        try:
            ws = wb["Sheet1"]
            actual = [[value if value is not None else "" for value in row]
                      for row in ws.iter_rows(values_only=True)]
            self.assertEqual(wb.sheetnames, ["Sheet1"])
            self.assertEqual((ws.max_row, ws.max_column), (5, 3))
            self.assertEqual(actual, rows)
            self.assertEqual(ws["C2"].data_type, "s")
            self.assertEqual(ws["C3"].data_type, "s")
            for index, column in enumerate(ws.columns):
                expected = min(255, max(8, max(len(row[index]) for row in rows) + 2))
                self.assertEqual(ws.column_dimensions[column[0].column_letter].width, expected)
        finally:
            wb.close()

    def test_xlsx_rejects_truncation_and_illegal_content(self) -> None:
        for value in ("a" * 32768, "нельзя\x00в Excel"):
            with self.subTest(length=len(value)):
                with self.csv.open("w", encoding="utf-8", newline="") as file:
                    csv.writer(file).writerows([["value"], [value]])
                with self.assertRaises(ValueError):
                    csv_to_xlsx(str(self.csv), str(self.xlsx))
                self.assertFalse(self.xlsx.exists())
        self.csv.write_text(",".join(f"c{i}" for i in range(16385)), encoding="utf-8")
        with self.assertRaises(ValueError):
            csv_to_xlsx(str(self.csv), str(self.xlsx))

    def test_converters_are_silent_return_none_and_create_parents(self) -> None:
        self.json.write_text('[{"name": "Анна"}]', encoding="utf-8")
        self.csv.write_text("name\nАнна\n", encoding="utf-8")
        cases = ((json_to_csv, self.json, "a/out.csv"),
                 (csv_to_json, self.csv, "b/out.json"),
                 (csv_to_xlsx, self.csv, "c/out.xlsx"))
        for converter, source, name in cases:
            with self.subTest(converter=converter.__name__):
                output = io.StringIO()
                target = self.folder / name
                with redirect_stdout(output):
                    result = converter(str(source), str(target))
                self.assertIsNone(result)
                self.assertEqual(output.getvalue(), "")
                self.assertTrue(target.is_file())


if __name__ == "__main__":
    unittest.main()
