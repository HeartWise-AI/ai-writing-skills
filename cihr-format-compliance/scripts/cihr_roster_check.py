#!/usr/bin/env python3
"""Cross-check the ResearchNet roster against the attestation forms in the same export.

Two mistakes recur in CIHR applications and both are invisible until a reader
trips over them:

1. Surname and given-name fields get reversed or merged. This is common for
   hyphenated and non-anglophone names, and ResearchNet prints the result into
   generated headings such as "Most Significant Contributions - <mangled name>".

2. Collaborators file a STRAC attestation. CIHR requires one from the Nominated
   Principal Applicant, Principal Applicants, Co-Applicants and Knowledge Users,
   and returns applications that include one from a Collaborator.

Both are checkable inside a single export, because the attestation forms carry
each person's own last-name and first-name fields, written by that person. That
is the authority; the roster is what gets typed into the portal and drifts.

Usage:
    python cihr_roster_check.py EXPORT.pdf
    python cihr_roster_check.py EXPORT.pdf --attestation-pages 4-23

Requires PyMuPDF (`pip install pymupdf`).

Exit status is 1 when any BLOCKER is reported, otherwise 0.
"""

import argparse
import re
import sys
import unicodedata

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

# Roles that owe CIHR a STRAC attestation. Anything else - in practice
# "Collaborator" - must not file one.
ATTESTATION_ROLES = {
    "nominated principal applicant",
    "nominated principal investigator",
    "principal applicant",
    "principal investigator",
    "co-applicant",
    "coapplicant",
    "knowledge user",
    "principal knowledge user",
}


def fold(text):
    """Casefold and strip accents so 'Thériault' and 'Theriault' compare equal."""
    stripped = "".join(
        c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c)
    )
    return re.sub(r"[^a-z0-9 ]+", " ", stripped.casefold()).split()


# Form labels that can follow a "Surname / Given Names" header when the entry is
# blank, which would otherwise be read as somebody's name.
FORM_LABELS = {
    "surname", "given names", "role", "participant type", "institution",
    "department", "faculty", "telephone", "fax", "e-mail", "email",
}


def read_roster(doc):
    """Yield (page, surname, given, role) for every roster entry in the export.

    Roster entries render as a fixed label/value sequence:
        Surname | Given Names | <surname> | <given> | Role | Participant Type | <role> | <type>
    """
    entries = []
    for index in range(doc.page_count):
        lines = [l.strip() for l in doc[index].get_text().split("\n") if l.strip()]
        for i, line in enumerate(lines):
            if line != "Surname" or i + 1 >= len(lines) or lines[i + 1] != "Given Names":
                continue
            if i + 3 >= len(lines):
                continue
            surname, given = lines[i + 2], lines[i + 3]
            if surname.casefold() in FORM_LABELS or given.casefold() in FORM_LABELS:
                continue
            role = ""
            # "Role" and "Participant Type" are labels; the role value is the
            # first line after them.
            for j in range(i + 4, min(i + 8, len(lines))):
                if lines[j] == "Role" and j + 2 < len(lines):
                    role = lines[j + 2]
                    break
            entries.append((index + 1, surname, given, role))
    return entries


def prose_order(doc, skip_pages):
    """Return the export's running text, minus the structured-form pages.

    Letters of support, biosketches and contribution statements all write names
    the way people write them, given name first. That gives a second opinion on
    field order for anyone whose attestation is absent - Collaborators, who by
    rule do not file one.

    Roster and attestation pages must be excluded. Both are forms that print the
    surname before the given name by design, so leaving them in would make every
    correctly entered name look reversed.
    """
    parts = [
        doc[i].get_text() for i in range(doc.page_count) if (i + 1) not in skip_pages
    ]
    return " ".join(" ".join(fold(p)) for p in parts)


def read_attestations(doc, pages):
    """Yield (page, last, first, email) for each STRAC attestation form.

    The filled values sit directly beneath their labels, so the labels' own
    rectangles locate them without relying on hard-coded coordinates.
    """
    forms = []
    for index in pages:
        page = doc[index]
        last_label = page.search_for("Last name of researcher")
        first_label = page.search_for("First name of researcher")
        if not last_label or not first_label:
            continue
        band_top = last_label[0].y1
        values = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    # Filled values are set noticeably larger than the labels.
                    if text and span["size"] > 12 and band_top < span["bbox"][1] < band_top + 30:
                        values.append((span["bbox"][0], text))
        values.sort()
        if len(values) < 2:
            continue
        email = re.findall(r"[\w.\-]+@[\w.\-]+", page.get_text())
        forms.append((index + 1, values[0][1], values[1][1], email[0] if email else ""))
    return forms


def parse_pages(spec, page_count):
    if not spec:
        return range(page_count)
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            pages.update(range(int(lo) - 1, int(hi)))
        else:
            pages.add(int(part) - 1)
    return sorted(p for p in pages if 0 <= p < page_count)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--attestation-pages",
                    help="1-based page range holding the STRAC forms, e.g. 4-23. "
                         "Defaults to scanning the whole document.")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    roster = read_roster(doc)
    attestations = read_attestations(doc, parse_pages(args.attestation_pages, doc.page_count))

    print(f"{args.pdf}: {len(roster)} roster entries, {len(attestations)} attestation forms\n")
    blockers = notes = 0

    # Index the attestations by the person's own spelling of their name.
    by_pair, by_last = {}, {}
    for page, last, first, email in attestations:
        by_pair[(tuple(fold(last)), tuple(fold(first)))] = (page, last, first)
        by_last.setdefault(tuple(fold(last)), []).append((page, last, first))

    form_pages = {page for page, *_ in roster} | {page for page, *_ in attestations}
    prose = prose_order(doc, form_pages)

    for page, surname, given, role in roster:
        s_tokens, g_tokens = tuple(fold(surname)), tuple(fold(given))
        needs_form = role.strip().casefold() in ATTESTATION_ROLES
        issues = []

        # A token in both fields means the name was split or merged wrongly.
        overlap = set(s_tokens) & set(g_tokens)
        if overlap:
            issues.append(
                f"BLOCKER  '{' '.join(sorted(overlap))}' appears in BOTH the surname and "
                f"given-name field - the name is split wrongly"
            )

        if (g_tokens, s_tokens) in by_pair and (s_tokens, g_tokens) not in by_pair:
            # Their own form carries the same two names the other way round.
            form_page, last, first = by_pair[(g_tokens, s_tokens)]
            issues.append(
                f"BLOCKER  fields are reversed - their own attestation (p{form_page}) "
                f"says last name '{last}', first name '{first}'"
            )
        elif (s_tokens, g_tokens) not in by_pair and s_tokens in by_last:
            # Surname agrees with their form but the given name does not.
            form_page, last, first = by_last[s_tokens][0]
            issues.append(
                f"BLOCKER  given name should be '{first}' - that is what they wrote on "
                f"their own attestation (p{form_page})"
            )
        elif (s_tokens, g_tokens) not in by_pair and needs_form:
            issues.append(
                f"BLOCKER  role '{role}' requires a STRAC attestation, "
                f"but no form in this export carries this name"
            )
        elif (
            (s_tokens, g_tokens) not in by_pair
            and len(s_tokens) == 1
            and len(g_tokens) == 1
            and not needs_form
        ):
            # No form to compare against, so ask the rest of the document. Prose
            # writes given name first; if it only ever writes these two names in
            # the opposite order, the portal fields are swapped.
            natural = f"{g_tokens[0]} {s_tokens[0]}"
            swapped = f"{s_tokens[0]} {g_tokens[0]}"
            if swapped in prose and natural not in prose:
                issues.append(
                    f"BLOCKER  fields look reversed - this export writes "
                    f"'{surname} {given}' in prose, never '{given} {surname}'"
                )

        # The RTSAP rule, in reverse: a Collaborator must not have filed one.
        if (s_tokens, g_tokens) in by_pair and role and not needs_form:
            form_page, *_ = by_pair[(s_tokens, g_tokens)]
            issues.append(
                f"BLOCKER  role '{role}' must NOT file a STRAC attestation, "
                f"but one is attached at p{form_page} - remove it"
            )

        if issues:
            print(f"p{page}  surname '{surname}' / given '{given}'  [{role or 'no role'}]")
            for issue in issues:
                print(f"    {issue}")
                blockers += issue.startswith("BLOCKER")
                notes += issue.startswith("NOTE")

    print(f"\n{blockers} blocker(s), {notes} note(s)")
    if blockers:
        print("Fix the roster fields in ResearchNet, or re-merge the attestation bundle.")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
