#!/usr/bin/env python3
"""Lightweight validation for GAIA decision-grade world signal ontology files.

This intentionally avoids third-party dependencies. It checks that required TTL
modules, SHACL stubs, and examples exist and contain the core vocabulary terms
needed by downstream GAIA, contracts, ledger, and MLOps integrations.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "world-signals" / "world-signals.ttl"
SHAPES = ROOT / "shapes" / "world-signals" / "world-signals.shacl.ttl"
EXAMPLE = ROOT / "examples" / "world-signals" / "feature-registry-entry.ttl"

REQUIRED_CLASSES = [
    "gaia:WorldSignal",
    "gaia:FeatureRegistryEntry",
    "gaia:FootTrafficIndex",
    "gaia:WeatherFeature",
    "gaia:CanonicalEntity",
    "gaia:ConcordanceLink",
    "gaia:EnergyLedgerEntry",
    "gaia:DecisionLedgerEntry",
    "gaia:ProofArtifact",
    "gaia:PromotionDecision",
    "gaia:PromotionState",
]

REQUIRED_PROMOTION_STATES = [
    "gaia:EvidenceOnly",
    "gaia:ReviewRequired",
    "gaia:Rejected",
    "gaia:Promoted",
]

REQUIRED_PROPERTIES = [
    "gaia:hasFeatureId",
    "gaia:hasPolicyId",
    "gaia:hasConfidence",
    "gaia:hasMarginDelta",
    "gaia:hasPerturbationFlipRate",
    "gaia:hasPromotionState",
    "gaia:promotesSignal",
    "gaia:mapsSourceRecordToEntity",
    "gaia:hasDecisionLedgerEntry",
]

REQUIRED_SHAPES = [
    "gaia:FeatureRegistryEntryShape",
    "gaia:EnergyLedgerEntryShape",
    "gaia:PromotionDecisionShape",
]


def read(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"missing required file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def require_terms(label: str, text: str, terms: list[str], errors: list[str]) -> None:
    for term in terms:
        if term not in text:
            errors.append(f"{label}: missing required term {term}")


def main() -> int:
    errors: list[str] = []
    ontology = read(ONTOLOGY, errors)
    shapes = read(SHAPES, errors)
    example = read(EXAMPLE, errors)

    require_terms("ontology", ontology, REQUIRED_CLASSES, errors)
    require_terms("ontology", ontology, REQUIRED_PROMOTION_STATES, errors)
    require_terms("ontology", ontology, REQUIRED_PROPERTIES, errors)
    require_terms("shapes", shapes, REQUIRED_SHAPES, errors)
    require_terms("example", example, ["gaia:WeatherFeature", "gaia:EnergyLedgerEntry", "gaia:PromotionDecision"], errors)

    if errors:
        print("GAIA world signal ontology validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Validated GAIA decision-grade world signal ontology module, shapes, and example fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
