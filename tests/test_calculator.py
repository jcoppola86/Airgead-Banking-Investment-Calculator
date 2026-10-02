"""Build the calculator and check its console output. Requires Python 3 and g++."""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CalculatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build_dir = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.build_dir.cleanup)
        cls.program = Path(cls.build_dir.name) / "investment_calculator"
        subprocess.run(
            [os.environ.get("CXX", "g++"), "-std=c++11", "-Wall", "-Wextra",
             "-pedantic", str(ROOT / "src/main.cpp"),
             str(ROOT / "src/InvestmentCalculator.cpp"), "-o", str(cls.program)],
            check=True,
        )

    def run_program(self, text):
        result = subprocess.run(
            [str(self.program)], input=text, text=True, capture_output=True,
            timeout=5, check=True,
        )
        return result.stdout

    def rows(self, output):
        return re.findall(r"^(\d+)\s+\$([\d.]+)\s+\$([\d.]+)$", output, re.MULTILINE)

    def test_example(self):
        output = self.run_program("1000\n100\n6\n2\n\n")
        self.assertEqual(self.rows(output), [
            ("1", "1061.68", "61.68"), ("2", "1127.16", "65.48"),
            ("1", "2295.23", "95.23"), ("2", "3670.36", "175.12"),
        ])

    def test_zero_values(self):
        cases = [
            ("1000\n100\n0\n1\n\n", [("1", "1000.00", "0.00"), ("1", "2200.00", "0.00")]),
            ("1000\n0\n6\n1\n\n", [("1", "1061.68", "61.68")] * 2),
            ("0\n0\n0\n1\n\n", [("1", "0.00", "0.00")] * 2),
        ]
        for text, expected in cases:
            with self.subTest(input=text):
                self.assertEqual(self.rows(self.run_program(text)), expected)

    def test_invalid_numbers_allow_retry(self):
        valid = ["1000", "100", "6", "1"]
        errors = ["Enter an initial investment", "Enter a monthly deposit", "Enter an annual interest rate"]
        for field in range(3):
            for bad in ["abc", "", "-1", "2abc", "nan", "inf", "1e309", "1,000"]:
                with self.subTest(field=field, value=bad):
                    entries = valid.copy()
                    entries.insert(field, bad)
                    output = self.run_program("\n".join(entries) + "\n\n")
                    self.assertIn(errors[field], output)
                    self.assertEqual(self.rows(output), [
                        ("1", "1061.68", "61.68"), ("1", "2295.23", "95.23"),
                    ])

    def test_invalid_years_allow_retry(self):
        for bad in ["0", "-1", "1.5", "abc", "", "2147483648", "2abc", "101"]:
            with self.subTest(value=bad):
                output = self.run_program("1000\n100\n6\n" + bad + "\n1\n\n")
                self.assertIn("Enter a whole number of years from 1 to 100.", output)
                self.assertEqual(len(self.rows(output)), 2)

    def test_values_above_limits_allow_retry(self):
        valid = ["1000", "100", "6", "1"]
        for field, bad in [(0, "1000000000.01"), (1, "1000000000.01"), (2, "100.01")]:
            with self.subTest(field=field):
                entries = valid.copy()
                entries.insert(field, bad)
                output = self.run_program("\n".join(entries) + "\n\n")
                self.assertIn("Enter a", output)
                self.assertEqual(len(self.rows(output)), 2)

    def test_upper_limits(self):
        output = self.run_program("1000000000\n1000000000\n100\n100\n\n")
        self.assertNotIn("Enter a", output)
        self.assertEqual(len(self.rows(output)), 200)
        self.assertNotRegex(output.lower(), r"\b(?:inf|nan)\b")

    def test_surrounding_whitespace(self):
        output = self.run_program(" 1000 \n 100 \n 6 \n 1 \n\n")
        self.assertEqual(self.rows(output), [
            ("1", "1061.68", "61.68"), ("1", "2295.23", "95.23"),
        ])

    def test_end_of_input(self):
        for text in ["", "1000\n", "1000\n100\n", "1000\n100\n6\n", "1000\n100\n6\n1\n", "abc\n"]:
            with self.subTest(input=text):
                output = self.run_program(text)
                self.assertIn("Input ended. No calculation was performed.", output)
                self.assertEqual(self.rows(output), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
