---
name: cihr-format-compliance
description: Verify that CIHR application PDFs and attachments meet the agency's mechanical format rules - Times New Roman, black, 12 pt minimum, 2 cm margins - that the right documents are attached, and that roster surname/given-name fields and STRAC attestation roles are correct. Use before submitting a CIHR Project Grant, after any document is re-exported, or when a grants officer returns an application for formatting. Also use when asked whether an application is ready to submit, or to check a ResearchNet export.
---

# CIHR Format Compliance

## Overview

CIHR screens applications on mechanical properties before anyone reads the science. A grants officer will return the application for any of these, and each round trip costs days you may not have near a deadline.

The rules that actually get enforced:

| Rule | Requirement |
|------|-------------|
| Body font | Times New Roman |
| Colour | Black |
| Size | At least 12 pt |
| Margins | At least 2 cm on all four sides |
| Attachments | Only the documents the program requires, from the people it requires them from |

Two things make this harder than it looks. First, all of these are properties of the **PDF**, not of the source `.docx` - a document that is correct in Word can fail after a bad conversion. Second, the font check reads the **embedded font name**, so a metric-compatible clone that is visually indistinguishable still fails.

## The conversion trap

**Never produce a CIHR PDF with LibreOffice.** `soffice --convert-to pdf` substitutes Liberation Serif for Times New Roman even when the real font is installed and `fc-match` resolves it correctly. Liberation Serif is metrically identical, so the page looks perfect and nothing warns you. `pdffonts` shows `LiberationSerif`, and CIHR rejects it.

The same applies to Cambria, which LibreOffice replaces with Caladea.

Safe export paths, both of which embed genuine `TimesNewRomanPSMT`:

- **Microsoft Word** - Save as PDF, or print to PDF. Produces a `Quartz PDFContext` producer string on macOS.
- **Chrome headless** - for HTML you generated yourself:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf=out.pdf "file:///path/to/page.html"
  ```

Whichever you use, verify the result. Do not assume.

## Procedure

### 1. Run the checker

```bash
python scripts/cihr_pdf_check.py FILE.pdf
python scripts/cihr_pdf_check.py EXPORT.pdf --pages 35-50   # applicant-authored pages only
```

It reports BLOCKER for real violations and NOTE for things a human should glance at but that CIHR accepts. It exits non-zero when any blocker is found, so it can gate a submission script.

On a full ResearchNet export, restrict `--pages` to the attachments you authored. CIHR's own generated pages - the reviews, the Scientific Officer notes, the roster and budget forms - are set in Arial and Helvetica with roughly 1 cm margins. That is CIHR's typesetting, not yours, and is never a finding.

### 2. Read the output correctly

**Blockers.** A font that is not Times New Roman across a paragraph's worth of text, any non-black body text, or a genuine margin overflow. Fix and re-export.

**Notes worth a look:**
- *Superscript citation numerals around 8 pt.* Standard and accepted. Only investigate if body text is also undersized.
- *Margin shortfall under 1 mm.* Usually a hanging-indent list numeral - a wide numeral such as `viii.` right-aligned to a tab stop reaches further left than the others. Cosmetic; nudge the list indent right by 2 pt if you want it clean.
- *A handful of stray characters in another font.* A page number the template set in Aptos, or one separator comma in Calibri. Not worth a re-export on its own.

**Suppressed by default.** Page numbers touching the bottom margin. Word places headers and footers inside the margin band by design and CIHR accepts it. Pass `--show-footers` if you want to see them.

### 3. Check the margins the right way

If you measure margins yourself rather than using the script, measure **individual glyph boxes**, not line or span boxes. A span box includes the trailing space of a justified line, which reads as a 1-2 mm overflow that is not really there. This produces false alarms on nearly every justified page.

### 4. Verify the attachment set

Beyond formatting, confirm the right documents are present and no extra ones are:

- **Response to Previous Reviews.** On a resubmission, attach the Scientific Officer notes when they exist. If the application was streamlined, no SO notes were generated - but ResearchNet still produces an SO Notes document that says so. **Attach that document.** It satisfies the requirement and shows you did not omit anything.
- **STRAC / sensitive-technology attestations.** Required from the Nominated Principal Applicant, Principal Applicants, Co-Applicants and Knowledge Users. **Collaborators must not provide one.** Including collaborator attestations gets the application returned. Roles come from the ResearchNet roster, not from how the narrative describes someone - a site PI in your text can be a Collaborator in the portal.
- **Institution fields.** Three separate fields, easy to confuse:
  1. Task 1, with your name and contact details: your **university affiliation**.
  2. Task 2, where the research takes place: the **hospital or institute**.
  3. Task 2, which institution administers the funds (Institution Paid): the **hospital or institute**.

Run the roster checker, which cross-references both against the roster:

```bash
python scripts/cihr_roster_check.py EXPORT.pdf --attestation-pages 4-23
```

It reports a Collaborator who filed an attestation, a required role whose attestation is
missing, and surname/given-name fields that are reversed or wrongly split. Pass the page
range holding the STRAC forms; without it the whole document is scanned, which still works
but is slower.

Also confirm every attestation page carries a completed date. A blank one means the bundle
was merged before the form was filled in.

### 5. Check the budget totals agree across documents

The budget module in ResearchNet and the budget narrative PDF are entered separately and drift apart. Compare the category totals and the grand total line by line. ResearchNet enforces $1,000 rounding on each category, so small differences can be legitimate - but they must be explained in the category description, and a category that is already a round thousand cannot be explained that way.

## How the name check decides

Surname and given-name errors are common and self-inflicted, so the check uses sources the
applicant did not type into the portal, in this order:

1. **The person's own attestation form.** They filled in their own last-name and first-name
   fields, so this outranks the roster. If the roster carries the same two names the other
   way round, the fields are reversed. If the surname agrees but the given name does not,
   the form's given name is the right one.
2. **A token appearing in both fields.** `Surname "Theriault Lauzier" / Given "Lauzier"`
   cannot be right whatever the person is called, and usually means the real given name is
   missing entirely.
3. **Prose elsewhere in the export.** Collaborators file no attestation, so there is no form
   to compare against. Letters of support, biosketches and contribution statements write
   names given-name-first. If the export only ever writes the two names in the order
   `<surname field> <given field>`, the portal fields are swapped.

Roster and attestation pages are excluded from the prose corpus. Both print the surname
before the given name by design, and leaving them in makes every correctly entered name look
reversed.

Accents are folded before comparison, so "Thériault" matches "Theriault". Verify anything the
check reports against a source the person wrote themselves before editing the portal - their
signed form, their letter's signature block, the local part of their institutional email, or
their PubMed author record.

## Pre-submission checklist

- [ ] Every applicant-authored attachment passes `cihr_pdf_check.py` with zero blockers
- [ ] `pdffonts` on each attachment shows only `TimesNewRoman*` variants, all `emb yes`
- [ ] No attachment was produced by LibreOffice
- [ ] Page limits respected for each attachment
- [ ] Task 1 institution is the university; both Task 2 institutions are the host hospital or institute
- [ ] `cihr_roster_check.py` reports zero blockers
- [ ] Attestations present for every required role, and for no Collaborator
- [ ] Every attestation carries a completed date
- [ ] SO notes attached to the response, including the "no notes generated" document if the application was streamlined
- [ ] Budget totals reconcile between ResearchNet and the narrative, or every difference is explained in the description
- [ ] Roster surnames and given names verified against a self-authored source (their attestation form, letter signature, institutional email, or PubMed author record)

## Related skills

- `cihr-grant-writing` - drafting the application
- `cihr-project-grant-audit` - scientific and internal-consistency audit of a non-RCT application
- `cihr-protocol-audit` - the same for a clinical trial protocol
