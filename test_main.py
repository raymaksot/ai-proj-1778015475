import pytest
from io import StringIO
import csv
from main import parse_csv, draw_bar_chart


class TestParseCsv:
    def test_standard_header(self):
        """Should skip header row when second column is non-numeric."""
        data = "Category,Value\nApples,10\nOranges,7"
        reader = csv.reader(StringIO(data))
        labels, values = parse_csv(reader)
        assert labels == ["Apples", "Oranges"]
        assert values == [10.0, 7.0]

    def test_no_header_numeric_first(self):
        """If first row's second column is numeric, treat it as data."""
        data = "Apples,10\nOranges,7"
        reader = csv.reader(StringIO(data))
        labels, values = parse_csv(reader)
        assert labels == ["Apples", "Oranges"]
        assert values == [10.0, 7.0]

    def test_skip_empty_lines(self):
        """Blank rows should be ignored."""
        data = "Name,Value\n\nApples,10\n\nOranges,7"
        reader = csv.reader(StringIO(data))
        labels, values = parse_csv(reader)
        assert labels == ["Apples", "Oranges"]
        assert values == [10.0, 7.0]

    def test_skip_invalid_values(self):
        """Rows where the second column is not a float should be skipped."""
        data = "Name,Value\nApples,10\nOranges,notanumber\nBananas,5"
        reader = csv.reader(StringIO(data))
        labels, values = parse_csv(reader)
        assert labels == ["Apples", "Bananas"]
        assert values == [10.0, 5.0]

    def test_empty_input(self):
        """Empty CSV should yield empty lists."""
        reader = csv.reader(StringIO(""))
        labels, values = parse_csv(reader)
        assert labels == []
        assert values == []


class TestDrawBarChart:
    def test_normal_output(self, capsys):
        labels = ["Apples", "Bananas"]
        values = [3.0, 10.0]
        draw_bar_chart(labels, values, max_bar_width=8)
        captured = capsys.readouterr().out
        assert "Apples" in captured
        assert "Bananas" in captured
        assert "3.0" in captured
        assert "10.0" in captured
        # Bar characters present for both (first bar = floor(3/10*8)=2, second =8)
        assert captured.count("█") == 2 + 8

    def test_all_zero_values(self, capsys):
        labels = ["X", "Y"]
        values = [0.0, 0.0]
        draw_bar_chart(labels, values, max_bar_width=10)
        captured = capsys.readouterr().out
        assert "0.0" in captured
        assert "X" in captured and "Y" in captured
        # No bar characters should be printed
        assert "█" not in captured

    def test_no_data(self, capsys):
        draw_bar_chart([], [])
        captured = capsys.readouterr().out
        assert captured.strip() == "No data to display."
        assert "No data" in captured