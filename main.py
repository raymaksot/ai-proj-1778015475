import sys
import csv
from io import StringIO
from math import floor

SAMPLE_CSV = """\
Category,Value
Apples,10
Oranges,7
Bananas,5
Grapes,12
Kiwis,3
Pears,8
Cherries,15
Mangos,6
Pineapples,4
Watermelons,9"""

def parse_csv(reader):
    """Read rows from csv.reader, return (labels, values) or ([], []) on failure."""
    labels = []
    values = []
    first_row = True
    for row in reader:
        if not row:
            continue
        if first_row:
            # Try to interpret as header; if second column is numeric, treat as data
            try:
                float(row[1])
                # It's data, so add it
                labels.append(row[0])
                values.append(float(row[1]))
                first_row = False
            except (ValueError, IndexError):
                # Likely header row, skip
                first_row = False
                continue
        else:
            try:
                val = float(row[1])
                labels.append(row[0])
                values.append(val)
            except (ValueError, IndexError):
                continue
    return labels, values

def draw_bar_chart(labels, values, bar_char='█', max_bar_width=50):
    """Prints a horizontal bar chart to stdout."""
    if not labels:
        print("No data to display.")
        return

    max_val = max(values) if values else 0
    if max_val == 0:
        # All values zero, just print empty bars
        label_width = max((len(l) for l in labels), default=0)
        for label, val in zip(labels, values):
            print(f"{label:{label_width}} | {val:.1f}")
        return

    label_width = max((len(l) for l in labels), default=0)
    fmt = f"{{label:<{label_width}}} | {{bar:<{max_bar_width}}} {{val:6.1f}}"
    for label, val in zip(labels, values):
        bar_len = floor(val / max_val * max_bar_width)
        bar = bar_char * bar_len
        print(fmt.format(label=label, bar=bar, val=val))

def main():
    with StringIO(SAMPLE_CSV) as f:
        reader = csv.reader(f)
        labels, values = parse_csv(reader)

    draw_bar_chart(labels, values)

if __name__ == '__main__':
    main()