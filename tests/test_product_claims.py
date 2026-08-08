from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PAGES = (
    "index.html",
    "product.html",
    "integrations.html",
    "trust.html",
    "about.html",
    "docs.html",
    "privacy.html",
)
CANONICAL_STATUS = "Signet7 is not released, deployed, or production-qualified."


class _PublicPage(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.visible_parts: list[str] = []
        self.title_parts: list[str] = []
        self.metadata: dict[str, str] = {}
        self._ignored_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"script", "style", "template"}:
            self._ignored_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and values.get("content"):
            key = values.get("name") or values.get("property")
            if key:
                self.metadata[str(key).casefold()] = str(values["content"])

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "template"} and self._ignored_depth:
            self._ignored_depth -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        if self._in_title:
            self.title_parts.append(data)
        else:
            self.visible_parts.append(data)

    @staticmethod
    def _normalized(parts: list[str]) -> str:
        return " ".join(" ".join(parts).split())

    @property
    def visible_text(self) -> str:
        return self._normalized(self.visible_parts)

    @property
    def searchable_text(self) -> str:
        return self._normalized(
            [self.visible_text, *self.title_parts, *self.metadata.values()]
        )


def _load_page(name: str) -> _PublicPage:
    parser = _PublicPage()
    parser.feed((ROOT / name).read_text(encoding="utf-8"))
    return parser


class PublicProductTruthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = {name: _load_page(name) for name in PUBLIC_PAGES}

    def test_every_public_page_is_under_the_claim_guardrail(self) -> None:
        self.assertEqual(
            {path.name for path in ROOT.glob("*.html")},
            set(PUBLIC_PAGES),
        )

    def test_approved_ai_inbox_tagline_is_visible_and_immediately_scoped(self) -> None:
        home = self.pages["index.html"].visible_text.casefold()
        self.assertIn("gatekeeper for the ai inbox.", home)
        self.assertIn(
            "not a deployed inbound mailbox gateway or agent inbox service",
            home,
        )
        self.assertIn(
            "operators and integrators still supply the receive path and enforce the result",
            home,
        )

    def test_every_page_keeps_the_candidate_out_of_production(self) -> None:
        for name, page in self.pages.items():
            with self.subTest(page=name):
                self.assertIn(CANONICAL_STATUS.casefold(), page.visible_text.casefold())

    def test_homepage_metadata_keeps_positioning_and_status_together(self) -> None:
        home = self.pages["index.html"]
        description = home.metadata.get("description", "")
        social_description = home.metadata.get("og:description", "")
        for label, value in (
            ("description", description),
            ("og:description", social_description),
        ):
            with self.subTest(metadata=label):
                normalized = value.casefold()
                self.assertIn("gatekeeper for the ai inbox.", normalized)
                self.assertIn("source-built candidate", normalized)
                self.assertIn("not released or deployed", normalized)

    def test_retired_and_unsupported_claim_classes_cannot_return(self) -> None:
        retired_patterns = {
            "universal inbound protection": r"\bprotects? every inbound email\b",
            "automatic action guarding": r"\bguards? every action\b",
            "whole-email overclaim": r"\bprotects? the whole email\b",
            "unsubstantiated category monopoly": r"\bno other platform\b",
            "built-in connector overclaim": r"\bbuilt[- ]in (?:gmail|ses|provider|mailbox|inbox|sdk|api|connector)",
            "availability overclaim": r"\b(?:production[- ]ready|generally available|now available)\b",
            "live integration overclaim": r"(?<!not )(?<!no )\blive (?:gmail|ses|provider|mailbox|inbound|agent inbox|integration)\b",
            "standardization overclaim": r"\bindustry standard\b|(?<!not an )\bindependently established (?:production )?standard\b",
            "released-status drift": r"\brelease[- ]candidate\b",
            "retired narrow email model": r"\bpartial input/signature foundation\b",
            "retired connector status": r"\bprovider connectors are roadmap work\b",
        }
        failures: list[str] = []
        for name, page in self.pages.items():
            text = page.searchable_text.casefold()
            for claim_class, pattern in retired_patterns.items():
                if re.search(pattern, text):
                    failures.append(f"{name}: {claim_class}: /{pattern}/")
        self.assertEqual(failures, [])

    def test_current_candidate_capabilities_are_not_erased_or_promoted(self) -> None:
        product = self.pages["product.html"].visible_text.casefold()
        required_product_facts = (
            "s7-email-1 signed-email signing and verification",
            "transactional and webhook flows",
            "signed, hash-chained evidence ledger",
            "authenticated physical epochs",
            "disabled by default and not activated",
            "recovery tooling",
            "nine-command windows packaging",
            "manual release and deployment workflows",
        )
        for fact in required_product_facts:
            with self.subTest(fact=fact):
                self.assertIn(fact, product)

        integrations = self.pages["integrations.html"].visible_text.casefold()
        required_integration_boundaries = (
            "gmail pilot tooling and ses operator tooling exist in source",
            "no live gmail or ses qualification",
            "not a deployed webhook receiver",
            "no deployed inbound mailbox gateway",
            "no universal receive pipeline",
        )
        for boundary in required_integration_boundaries:
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, integrations)

        docs = self.pages["docs.html"].visible_text.casefold()
        for absent_gate in (
            "no live github controls",
            "no approved production aws deployment",
            "no public sdk, api, or connector program",
        ):
            with self.subTest(absent_gate=absent_gate):
                self.assertIn(absent_gate, docs)

    def test_targets_and_vsn_artifacts_keep_their_non_live_boundary(self) -> None:
        integrations = self.pages["integrations.html"].visible_text.casefold()
        self.assertIn(
            "intended consumers and integration targets—not live integrations",
            integrations,
        )

        docs = self.pages["docs.html"].visible_text.casefold()
        self.assertIn("draft/archived transport profile", docs)
        self.assertIn("not an independently established production standard", docs)


if __name__ == "__main__":
    unittest.main()
