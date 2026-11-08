#!/usr/bin/env python3
"""Maintain shared references without runtime dependencies between skills.

Edit references/ beside this script, then run this script to update installed
copies. --check reports missing or stale copies without writing. Each skill's
local references are complete; this authoring directory is not needed to use it.
--skills-root targets a separate installation for packaging or verification.
"""

import argparse
from pathlib import Path


SOURCE = Path(__file__).resolve().parent
TARGETS = {
    "evidence.md": ("diagnosing-bugs", "finding-bugs", "investigating-regressions"),
    "review-history.md": ("diagnosing-bugs", "finding-bugs", "investigating-regressions"),
    "regression-history.md": ("diagnosing-bugs", "investigating-regressions"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--skills-root", type=Path, default=SOURCE.parent)
    args = parser.parse_args()

    # Read every source and check the destinations before changing any copy.
    updates = []
    for filename, skills in TARGETS.items():
        source = SOURCE / "references" / filename
        header = (
            f"<!-- Generated from .bug-workflows/references/{filename}. "
            "Edit that source and run .bug-workflows/sync.py. "
            "This local copy is self-contained at runtime. -->\n\n"
        )
        content = header + source.read_text()
        for skill in skills:
            directory = args.skills_root / skill
            if not (directory / "SKILL.md").is_file():
                parser.error(f"Missing skill: {directory}")
            target = directory / "references" / filename
            if not target.exists() or target.read_text() != content:
                updates.append((target, content))

    for target, content in updates:
        if args.check:
            print(f"STALE {target}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            print(f"UPDATED {target}")
    if not updates:
        print("Shared reference copies are current.")
    return int(args.check and bool(updates))


if __name__ == "__main__":
    raise SystemExit(main())
