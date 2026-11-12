"""Keep the optional single-file export synchronized with the source pages."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_master import render


class MasterExportTests(unittest.TestCase):
    def test_export_is_up_to_date(self):
        self.assertEqual(
            render(),
            (ROOT / "AI_INTEGRATION_MASTER_REFERENCE.md").read_text(encoding="utf-8"),
            "Run: python scripts/build_master.py",
        )


if __name__ == "__main__":
    unittest.main()
