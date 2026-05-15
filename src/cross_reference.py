"""
Compare extension sets from ``instr_dict.json`` (after canonicalization)
with names scraped from the ISA manual. ``json_only`` usually means the
landscape lists an extension the manual scan did not pick up yet—often
newer or vendor-specific packs, or limits of regex on AsciiDoc.

Matching strategy:
  1. Exact set intersection (canonical names must match exactly).
  2. Fuzzy fallback via Levenshtein distance for near-misses — catches
     cases like ``Svinval_h`` vs ``Svinval`` that survive normalization
     with a trailing component the manual does not repeat verbatim.
"""

from src.normalizer import (
    normalize_extension_name,
)


def normalize_json_extensions(
    extension_groups: dict,
) -> set:
    """
    Build the set of canonical extension names implied by Tier 1 grouping.

    ``extension_groups`` keys are raw tags (e.g. ``rv_zba``). Tags that
    normalize to ``""`` are skipped so bad keys do not enter the set.
    """

    normalized_extensions = set()

    for extension in extension_groups:

        normalized = (
            normalize_extension_name(
                extension
            )
        )

        if not normalized:
            continue

        normalized_extensions.add(
            normalized
        )

    return normalized_extensions


def levenshtein_distance(a: str, b: str) -> int:
    """
    Compute the Levenshtein edit distance between two strings.

    Args:
        a: First string.
        b: Second string.

    Returns:
        Minimum number of single-character edits (insert, delete,
        substitute) needed to transform ``a`` into ``b``.
    """

    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    prev = list(range(len(b) + 1))

    for i, char_a in enumerate(a, start=1):
        curr = [i]
        for j, char_b in enumerate(b, start=1):
            cost = 0 if char_a == char_b else 1
            curr.append(
                min(
                    curr[j - 1] + 1,
                    prev[j] + 1,
                    prev[j - 1] + cost,
                )
            )
        prev = curr

    return prev[-1]


def fuzzy_match(
    source: str,
    candidates: set,
    threshold: float = 0.75,
) -> str | None:
    """
    Find the closest candidate to ``source`` using Levenshtein similarity.

    Similarity is defined as:
        1.0 - (edit_distance / max(len(source), len(candidate)))

    Only candidates with similarity >= ``threshold`` are considered.
    Returns the best candidate or ``None`` if nothing meets the threshold.

    Args:
        source:     Canonical JSON extension name to match.
        candidates: Set of canonical manual extension names.
        threshold:  Minimum similarity score (0.0 to 1.0). Default 0.75
                    is tight enough to avoid false positives while catching
                    real near-misses like ``Svinval_h`` vs ``Svinval``.

    Returns:
        Best-matching candidate string, or ``None``.
    """

    best_match = None
    best_score = 0.0

    source_lower = source.lower()

    for candidate in candidates:
        candidate_lower = candidate.lower()
        distance = levenshtein_distance(
            source_lower,
            candidate_lower,
        )
        max_len = max(
            len(source_lower),
            len(candidate_lower),
            1,
        )
        score = 1.0 - (distance / max_len)

        if score >= threshold and score > best_score:
            best_score = score
            best_match = candidate

    return best_match


def cross_reference_extensions(
    json_extensions: set,
    manual_extensions: set,
    fuzzy: bool = True,
    fuzzy_threshold: float = 0.75,
) -> dict:
    """
    Split two canonical-name sets into matched, JSON-only, and manual-only.

    Matching runs in two passes:
      1. Exact intersection — canonical names must be identical.
      2. Fuzzy pass (when ``fuzzy=True``) — Levenshtein similarity on the
         remaining JSON-only set. Near-misses above ``fuzzy_threshold``
         are moved to matched and annotated with ``(fuzzy)``.

    Args:
        json_extensions:  Canonical names from ``instr_dict.json``.
        manual_extensions: Canonical names from ISA manual scan.
        fuzzy:            Enable fuzzy fallback. Default ``True``.
        fuzzy_threshold:  Minimum similarity score for fuzzy match.

    Returns:
        Dict with keys ``matched``, ``json_only``, ``manual_only``.
        ``matched`` is a set of strings; fuzzy-matched entries are
        suffixed with ``" (fuzzy)"``.
    """

    # Pass 1 — exact match
    exact_matched = (
        json_extensions &
        manual_extensions
    )

    json_only_remainder = (
        json_extensions -
        manual_extensions
    )

    manual_only_remainder = (
        manual_extensions -
        json_extensions
    )

    matched = set(exact_matched)

    # Pass 2 — fuzzy fallback on remaining json_only
    if fuzzy and json_only_remainder:

        still_json_only = set()

        for source in json_only_remainder:

            candidate = fuzzy_match(
                source,
                manual_only_remainder,
                threshold=fuzzy_threshold,
            )

            if candidate is not None:
                # Move from unmatched to matched with fuzzy annotation
                matched.add(f"{source} (fuzzy)")
                manual_only_remainder.discard(candidate)
            else:
                still_json_only.add(source)

        json_only_remainder = still_json_only

    return {
        "matched": matched,
        "json_only": json_only_remainder,
        "manual_only": manual_only_remainder,
    }


def generate_cross_reference_report(
    cross_reference_results: dict,
) -> str:
    """
    Format ``cross_reference_results`` as a stable, sorted text report.

    Expects keys ``matched``, ``json_only``, ``manual_only``. Includes the
    assignment-style count line plus three labeled sections. Fuzzy-matched
    entries (suffixed with ``" (fuzzy)"``) appear in the matched section.
    """

    matched = sorted(
        cross_reference_results["matched"]
    )

    json_only = sorted(
        cross_reference_results["json_only"]
    )

    manual_only = sorted(
        cross_reference_results["manual_only"]
    )

    lines = []

    lines.append(
        "Cross Reference Summary"
    )

    lines.append("-" * 55)

    lines.append(
        f"Matched Extensions: {len(matched)}"
    )

    lines.append(
        f"JSON Only Extensions: {len(json_only)}"
    )

    lines.append(
        f"Manual Only Extensions: {len(manual_only)}"
    )

    lines.append("")

    lines.append(
        f"{len(matched)} matched, {len(json_only)} in JSON only, "
        f"{len(manual_only)} in manual only"
    )

    lines.append("")

    lines.append(
        "Matched Extensions"
    )

    lines.append("-" * 55)

    for extension in matched:
        lines.append(extension)

    lines.append("")

    lines.append(
        "JSON Only Extensions"
    )

    lines.append("-" * 55)

    for extension in json_only:
        lines.append(extension)

    lines.append("")

    lines.append(
        "Manual Only Extensions"
    )

    lines.append("-" * 55)

    for extension in manual_only:
        lines.append(extension)

    return "\n".join(lines)