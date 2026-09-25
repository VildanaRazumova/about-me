#!/usr/bin/env python3
"""Build agent/knowledge.md from public/ files: the ONLY text the agent sees besides rules.md.

Cleaning rules (so drafts never reach visitors):
- HTML comments are removed
- trailing YAML comments that start with "# ⚠" are removed, the fact itself is kept
- "⚠ <question>?" fragments are removed; anything after a remaining "⚠" on a line is cut
- lines that end up empty ("- **Result:**", "period:") are dropped
- in the "Missing stories" section, "- ⚠ X" becomes "- X" (the agent must know there is no story yet)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ORDER = ["facts.yaml", "now.md", "stories.md", "recommendations.md"] + sorted(
    f"projects/{p.name}" for p in (PUBLIC / "projects").glob("*.md"))


def clean(text: str, is_yaml: bool) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out, in_missing = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            in_missing = "Missing stories" in line
        if re.match(r"^\s*visibility:", line):
            continue
        line = re.sub(r"\s+#\s*⚠.*$", "", line)                 # trailing draft comments: keep the fact
        if "⚠" not in line:
            out.append(line.rstrip())
            continue
        # the line itself is (partly) a draft
        if is_yaml or line.lstrip().startswith("#"):
            continue                                              # YAML value or comment with ⚠: drop line
        if in_missing and line.startswith("- ⚠ "):
            out.append("- " + line[4:].strip())                   # agent must know there is no story yet
            continue
        line = line[: line.index("⚠")].rstrip()                # cut the draft part (always at line end)
        if re.fullmatch(r"\s*(-\s*)?(\*\*[^*]+:\*\*)?\s*", line) or re.fullmatch(r"\s*[\w-]+:\s*[\"']?\s*", line):
            continue                                              # only a label left
        out.append(line.rstrip())
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def main() -> None:
    parts = []
    for rel in ORDER:
        body = clean((PUBLIC / rel).read_text(encoding="utf-8"), rel.endswith(".yaml"))
        parts.append(f"<file name=\"{rel}\">\n{body}\n</file>")
    knowledge = "\n\n".join(parts) + "\n"
    dest = ROOT / "agent" / "knowledge.md"
    dest.write_text(knowledge, encoding="utf-8")
    print(f"{dest}: {len(knowledge):,} chars ≈ {len(knowledge)//4:,} tokens", file=sys.stderr)


if __name__ == "__main__":
    main()
