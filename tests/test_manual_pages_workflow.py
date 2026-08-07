from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"


class ManualPagesWorkflowTests(unittest.TestCase):
    def test_pages_deployment_is_manual_only_and_pins_actions(self) -> None:
        self.assertTrue(WORKFLOW.is_file(), "manual Pages workflow is missing")
        text = WORKFLOW.read_text(encoding="utf-8")
        header, jobs = text.split("jobs:", 1)

        self.assertIn("workflow_dispatch:", header)
        self.assertNotRegex(header, r"(?m)^\s+(push|pull_request|schedule):")
        self.assertIn("pages: write", text)
        self.assertIn("id-token: write", text)
        self.assertIn("environment:\n      name: github-pages", jobs)

        actions = re.findall(r"uses:\s*([^\s#]+)", text)
        self.assertGreaterEqual(len(actions), 4)
        for action in actions:
            self.assertRegex(action.rsplit("@", 1)[-1], r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
