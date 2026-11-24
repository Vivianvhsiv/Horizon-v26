"""Regression tests for evidence-gated subject-to-major links."""
import json
from pathlib import Path

from evidence_rules import has_subject_major_evidence


def ref(**overrides):
    value = {
        "claim_id": "claim-001",
        "institution": "Example University",
        "title": "Programme curriculum",
        "url": "https://example.edu/programme",
    }
    value.update(overrides)
    return value


def test_approved_exploratory_curriculum_status_with_claim_reference_passes():
    record = {
        "evidence_status_en": "Curriculum context identified; EMASI subject mapping remains exploratory",
        "evidence_refs": [ref()],
    }
    assert has_subject_major_evidence(record)


def test_university_curriculum_context_status_with_claim_reference_passes():
    record = {
        "evidence_status_en": "University curriculum context identified; EMASI subject mapping remains exploratory and is not an admission requirement.",
        "evidence_refs": [ref()],
    }
    assert has_subject_major_evidence(record)


def test_unverified_subject_level_link_is_rejected_even_with_a_reference():
    record = {
        "evidence_status_en": "Exploratory mapping — subject-level link not yet independently verified",
        "evidence_refs": [ref()],
    }
    assert not has_subject_major_evidence(record)


def test_general_reference_without_claim_id_is_rejected():
    record = {
        "evidence_status_en": "Curriculum context identified; EMASI subject mapping remains exploratory",
        "evidence_refs": [ref(claim_id="")],
    }
    assert not has_subject_major_evidence(record)


def test_empty_or_malformed_evidence_is_rejected():
    assert not has_subject_major_evidence({})
    assert not has_subject_major_evidence({"evidence_status_en": "Curriculum context identified; EMASI subject mapping remains exploratory", "evidence_refs": []})
    assert not has_subject_major_evidence(None)


def test_major_catalogue_contains_twenty_profiles_and_bilingual_fields():
    data = json.loads((Path(__file__).parent / "majors.json").read_text(encoding="utf-8"))
    assert len(data) == 20
    for profile in data.values():
        assert profile.get("name_vi")
        assert profile.get("overview") or profile.get("overview_vi")
