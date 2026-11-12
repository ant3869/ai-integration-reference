"""Check local Markdown links without internet or third-party dependencies."""

import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\]\(([^\s)]+)")


class DocumentationTests(unittest.TestCase):
    def test_local_markdown_links_exist(self):
        missing = []
        for page in ROOT.rglob("*.md"):
            if page.name == "AI_INTEGRATION_MASTER_REFERENCE.md":
                continue  # Embedded relative links are resolved from their source files.
            for raw_target in LINK_RE.findall(page.read_text(encoding="utf-8")):
                target = unquote(raw_target.split("#", 1)[0])
                if not target or re.match(r"^(?:https?:|mailto:|data:)", target):
                    continue
                if not (page.parent / target).exists():
                    missing.append(f"{page.relative_to(ROOT)} -> {raw_target}")
        self.assertFalse(missing, "Broken relative links:\n" + "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
