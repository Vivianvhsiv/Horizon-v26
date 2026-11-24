"""Evidence threshold for EMASI subject-to-major exploration links.

Only claim-level references attached to an explicitly approved exploratory
curriculum status can create a network edge. General programme URLs alone
are not enough to support a specific subject-to-major relationship.
"""

APPROVED_SUBJECT_MAP_STATUSES = {
    "Curriculum context identified; EMASI subject mapping remains exploratory",
    "University curriculum context identified; EMASI subject mapping remains exploratory and is not an admission requirement.",
}


def has_subject_major_evidence(guidance):
    """Return True only when status and every required claim reference field pass."""
    if not isinstance(guidance, dict):
        return False
    if (guidance.get("evidence_status_en") or "").strip() not in APPROVED_SUBJECT_MAP_STATUSES:
        return False
    refs = guidance.get("evidence_refs", [])
    if not isinstance(refs, list) or not refs:
        return False
    return any(
        isinstance(ref, dict)
        and all(str(ref.get(field, "")).strip() for field in ("claim_id", "institution", "title", "url"))
        for ref in refs
    )
