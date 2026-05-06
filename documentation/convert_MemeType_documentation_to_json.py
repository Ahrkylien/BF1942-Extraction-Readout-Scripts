import json
import re
from pathlib import Path

INPUT_FILE = Path("MemeType.md")
OUTPUT_FILE = Path("../meme_types.json")


def parse_markdown(md_text):
    result = {}
    current_node = None
    start_of_types_found = False
    in_nodes_section = False

    for line in md_text.splitlines():
        line = line.strip()

        if line.startswith("# Nodes"):
            start_of_types_found = True
            in_nodes_section = True
            continue
        elif line.startswith("# "):
            in_nodes_section = False

        if not start_of_types_found:
            continue

        header_match = re.match(r"^##\s+(\w+)", line)
        if header_match:
            current_node = header_match.group(1)
            result[current_node] = [["NextNode", "Next node"]] if in_nodes_section else []
            continue

        if line.startswith("- ") and current_node:
            content = line.lstrip("-* ").strip()
            parts = content.split(":", 1)
            if len(parts) == 2:
                result[current_node].append([parts[0].strip(), parts[1].strip()])

    return result


def format_json_inline_lists(data):
    lines = ["{"]

    items = list(data.items())
    for i, (key, value) in enumerate(items):
        inner = ", ".join(f'["{t}", "{n}"]' for t, n in value)
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'  "{key}": [{inner}]{comma}')

    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main():
    md_text = INPUT_FILE.read_text(encoding="utf-8")
    parsed = parse_markdown(md_text)

    formatted = format_json_inline_lists(parsed)

    OUTPUT_FILE.write_text(formatted, encoding="utf-8")

    print(f"JSON written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
