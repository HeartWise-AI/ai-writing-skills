#!/usr/bin/env python3
"""
CIHR Protocol Audit -- Automated Checks (Parts B, E, F)

Parts A, C, D require semantic judgment and should be done by Claude
reading the document. This script handles the mechanical checks that
benefit from regex and string matching.

Usage:
    python run_audit.py <plain_text_file> [--output audit_results.md]
"""

import re
import sys
import argparse
from collections import defaultdict


def extract_sections(text):
    """Extract section headings and their content."""
    sections = {}
    pattern = re.compile(r'^(\d+(?:\.\d+)*)\s+(.+)$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        sec_num = m.group(1)
        sec_title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[sec_num] = {
            'title': sec_title,
            'content': text[start:end].strip(),
            'pos': m.start()
        }
    return sections


def find_cross_references(text):
    """Find all cross-references to other sections."""
    patterns = [
        r'[Ss]ection\s+(\d+(?:\.\d+)*)',
        r'[Ss]ec\.?\s+(\d+(?:\.\d+)*)',
        r'\((\d+\.\d+(?:\.\d+)*)\)',
    ]
    refs = []
    for p in patterns:
        for m in re.finditer(p, text):
            line_start = text.rfind('\n', 0, m.start()) + 1
            line_end = text.find('\n', m.end())
            if line_end == -1:
                line_end = len(text)
            context = text[line_start:line_end].strip()
            refs.append({
                'target': m.group(1),
                'context': context[:120],
                'pos': m.start()
            })
    return refs


def find_garbled_text(text):
    """Detect potential garbled text from tracked-change splice errors."""
    issues = []

    # Period followed by lowercase with no space (excluding decimals, abbreviations)
    for m in re.finditer(r'\.([a-z])', text):
        pos = m.start()
        before = text[max(0, pos - 20):pos + 5]
        # Skip decimal numbers
        if pos > 0 and text[pos - 1].isdigit():
            continue
        # Skip common abbreviations and domain-specific terms
        abbrev_check = text[max(0, pos - 10):pos + 5]
        if any(a in abbrev_check.lower() for a in ['e.g', 'i.e', 'vs.', 'al.', 'dr.', 'mr.', 'ms.', 'doi:', '.ai', '.com', '.org', '.ca']):
            continue
        # Skip URLs and filenames
        if re.search(r'www\.|http|\.pdf|\.docx|\.xlsx', text[max(0, pos - 15):pos + 10]):
            continue
        issues.append({
            'type': 'period_no_space',
            'context': before,
            'pos': pos
        })

    # Lowercase-uppercase junction (missing space)
    for m in re.finditer(r'([a-z])([A-Z])', text):
        pos = m.start()
        before = text[max(0, pos - 15):pos + 10]
        # Skip camelCase-like patterns in known terms
        word_start = text.rfind(' ', max(0, pos - 30), pos)
        word = text[word_start + 1:pos + 2] if word_start >= 0 else text[:pos + 2]
        # Skip known proper nouns, abbreviations, and camelCase terms
        context_window = text[max(0, pos - 20):pos + 20]
        known_terms = [
            'EchoNext', 'DeepECG', 'InForm', 'HeartWise', 'HeartLife',
            'HFrEF', 'HFpEF', 'CoA', 'DiCiccio', 'McG',
            'NT-pro', 'proBNP', 'OxVALVE',
        ]
        if any(t in context_window for t in known_terms):
            continue
        # Skip superscript notation patterns
        if re.search(r'[⁰¹²³⁴⁵⁶⁷⁸⁹\^]\s*[A-Z]', context_window):
            continue
        issues.append({
            'type': 'missing_space',
            'context': before,
            'pos': pos
        })

    # Orphan possessive ('s without clear antecedent)
    for m in re.finditer(r"\.\s*'s\s", text):
        pos = m.start()
        context = text[max(0, pos - 30):pos + 30]
        issues.append({
            'type': 'orphan_possessive',
            'context': context,
            'pos': pos
        })

    return issues


def find_duplicate_fragments(text):
    """Detect near-duplicate phrases within proximity."""
    issues = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for i in range(len(sentences) - 1):
        s1 = sentences[i].strip().lower()
        s2 = sentences[i + 1].strip().lower()
        if len(s1) < 15 or len(s2) < 15:
            continue
        # Check for significant word overlap
        words1 = set(s1.split())
        words2 = set(s2.split())
        if len(words1) < 3 or len(words2) < 3:
            continue
        overlap = words1 & words2
        ratio = len(overlap) / min(len(words1), len(words2))
        if ratio > 0.7:
            issues.append({
                'type': 'duplicate_fragment',
                'sentence1': sentences[i][:80],
                'sentence2': sentences[i + 1][:80],
                'overlap_ratio': f'{ratio:.0%}'
            })
    return issues


def check_abbreviation_consistency(text):
    """Check that abbreviations are defined at first use and used consistently."""
    # Common clinical trial abbreviations
    abbrevs = {
        'TTE': r'\btransthoracic echocardiograph',
        'SHD': r'\bstructural heart disease\b',
        'ECG': r'\belectrocardiogra',
        'MACE': r'\bmajor adverse cardiovascular event',
        'ICC': r'\bintraclass correlation',
        'DSMB': r'\b[Dd]ata [Ss]afety [Mm]onitoring [Bb]oard',
        'SUS': r'\b[Ss]ystem [Uu]sability [Ss]cale',
        'CAHPS': r'\bConsumer Assessment of Healthcare',
        'FTE': r'\bfull.time equivalent',
        'SAP': r'\bstatistical analysis plan',
        'CRF': r'\bcase report form',
        'OR': r'\bodds ratio',
        'CI': r'\bconfidence interval',
        'RCT': r'\brandomized controlled trial',
    }

    results = {}
    for abbr, full_pattern in abbrevs.items():
        abbr_count = len(re.findall(r'\b' + abbr + r'\b', text))
        full_matches = re.findall(full_pattern, text, re.IGNORECASE)
        # Check if defined at first use
        first_abbr = re.search(r'\b' + abbr + r'\b', text)
        first_full = re.search(full_pattern, text, re.IGNORECASE)

        if abbr_count > 0:
            defined = first_full is not None and (first_abbr is None or first_full.start() <= first_abbr.start())
            results[abbr] = {
                'count': abbr_count,
                'full_form_count': len(full_matches),
                'defined_before_use': defined
            }

    return results


def check_arm_naming(text):
    """Check consistency of study arm/group naming."""
    arm_patterns = {
        'intervention': [
            r'\bintervention\s+arm\b',
            r'\bAI\s+arm\b',
            r'\bexperimental\s+arm\b',
            r'\bEchoNext\s+arm\b',
            r'\bintervention\s+group\b',
            r'\bAI\s+group\b',
            r'\bAI-guided\s+arm\b',
        ],
        'control': [
            r'\bcontrol\s+arm\b',
            r'\busual\s+care\b',
            r'\bstandard\s+care\b',
            r'\bcomparator\b',
            r'\bcontrol\s+group\b',
            r'\bnon-AI\s+arm\b',
        ]
    }

    results = {}
    for arm_type, patterns in arm_patterns.items():
        variants = {}
        for p in patterns:
            matches = re.findall(p, text, re.IGNORECASE)
            if matches:
                canonical = matches[0].strip()
                variants[canonical] = len(matches)
        results[arm_type] = variants

    return results


def check_statistical_method_naming(text):
    """Check consistency of statistical method names."""
    method_groups = {
        'logistic_regression': [
            r'mixed.effect\s+logistic\s+regression',
            r'mixed.effects\s+logistic\s+regression',
            r'multilevel\s+logistic\s+(?:regression|model)',
            r'hierarchical\s+logistic\s+(?:regression|model)',
            r'logistic\s+regression\s+with\s+random',
        ],
        'cox_regression': [
            r'shared.frailty\s+Cox',
            r'Cox\s+proportional\s+hazards',
            r'Cox\s+regression',
            r'Cox\s+model',
        ],
        'survival': [
            r'Kaplan.Meier',
            r'KM\s+curves?',
            r'log.rank\s+test',
        ]
    }

    results = {}
    for method_type, patterns in method_groups.items():
        variants = {}
        for p in patterns:
            matches = re.findall(p, text, re.IGNORECASE)
            if matches:
                canonical = matches[0].strip()
                variants[canonical] = len(matches)
        if variants:
            results[method_type] = variants

    return results


def generate_report(text, output_path=None):
    """Run all checks and generate audit report."""
    report = []
    report.append("# Protocol Audit: Automated Checks\n")
    report.append(f"Generated by `run_audit.py`\n")

    # Part B: Cross-references
    report.append("## Part B: Cross-Reference Inventory\n")
    refs = find_cross_references(text)
    sections = extract_sections(text)
    report.append(f"Found {len(refs)} cross-references and {len(sections)} sections.\n")

    if refs:
        report.append("| # | Target | Context | Section Exists? |")
        report.append("|---|--------|---------|----------------|")
        for i, ref in enumerate(refs):
            exists = "Yes" if ref['target'] in sections else "**NO**"
            context = ref['context'].replace('|', '\\|')[:80]
            report.append(f"| {i+1} | {ref['target']} | {context} | {exists} |")
        report.append("")

    # Part E: Content issues
    report.append("## Part E: Garbled Text Detection\n")
    garbled = find_garbled_text(text)
    if garbled:
        report.append(f"Found {len(garbled)} potential issues:\n")
        for issue in garbled:
            ctx = issue['context'].replace('|', '\\|')
            report.append(f"- **{issue['type']}**: `{ctx}`")
    else:
        report.append("No garbled text detected.\n")

    report.append("\n## Part E: Duplicate Fragments\n")
    dupes = find_duplicate_fragments(text)
    if dupes:
        for d in dupes:
            report.append(f"- **{d['overlap_ratio']} overlap**: `{d['sentence1']}` / `{d['sentence2']}`")
    else:
        report.append("No duplicate fragments detected.\n")

    # Part F: Terminology consistency
    report.append("\n## Part F: Abbreviation Consistency\n")
    abbrevs = check_abbreviation_consistency(text)
    if abbrevs:
        report.append("| Abbreviation | Uses | Full Form Uses | Defined Before First Use? |")
        report.append("|-------------|------|---------------|--------------------------|")
        for abbr, info in sorted(abbrevs.items()):
            defined = "Yes" if info['defined_before_use'] else "**NO**"
            report.append(f"| {abbr} | {info['count']} | {info['full_form_count']} | {defined} |")
    report.append("")

    report.append("## Part F: Arm/Group Naming Consistency\n")
    arms = check_arm_naming(text)
    for arm_type, variants in arms.items():
        if variants:
            report.append(f"### {arm_type.title()} arm variants:")
            for name, count in sorted(variants.items(), key=lambda x: -x[1]):
                report.append(f"- \"{name}\" ({count} uses)")
            report.append("")
        else:
            report.append(f"### {arm_type.title()}: no explicit arm naming found\n")

    report.append("## Part F: Statistical Method Naming\n")
    methods = check_statistical_method_naming(text)
    for method_type, variants in methods.items():
        if len(variants) > 1:
            report.append(f"### {method_type} -- **INCONSISTENT** ({len(variants)} variants):")
        else:
            report.append(f"### {method_type}:")
        for name, count in sorted(variants.items(), key=lambda x: -x[1]):
            report.append(f"- \"{name}\" ({count} uses)")
        report.append("")

    report_text = '\n'.join(report)

    if output_path:
        with open(output_path, 'w') as f:
            f.write(report_text)
        print(f"Audit report saved to {output_path}")
    else:
        print(report_text)

    return report_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CIHR Protocol Audit')
    parser.add_argument('input_file', help='Plain text file of the protocol')
    parser.add_argument('--output', '-o', default=None, help='Output markdown file')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    generate_report(text, args.output)
