#!/usr/bin/env python3
"""
OOXML tracked-change utilities using body-swap serialization.

Body-swap approach:
  1. Parse document.xml with lxml
  2. Modify <w:body> (add w:del, w:ins, commentRangeStart/End)
  3. Serialize only the body via etree.tostring
  4. Replace <w:body>...</w:body> in the original XML string
  This preserves namespace declarations that lxml mangles on re-serialization.

Usage:
    from docx_tracked_changes import DocumentEditor
    editor = DocumentEditor('unpacked/word/document.xml')
    editor.find_replace('old text', 'new text', 'label')
    editor.add_comment('search text', 'Comment content here')
    editor.save()
    editor.save_comments('unpacked/word/comments.xml')
    editor.add_author_to_people('unpacked/word/people.xml')
"""

from lxml import etree
import copy
import re

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def qn(tag):
    return f'{{{W}}}{tag}'


class DocumentEditor:
    def __init__(self, document_xml_path, author="Claude (Audit)", date="2026-02-21T00:00:00Z"):
        self.path = document_xml_path
        self.author = author
        self.date = date
        self.tc_id = 1500
        self.comment_id = 500
        self.comments_to_add = []

        with open(document_xml_path, 'r', encoding='utf-8') as f:
            self.original_xml = f.read()

        self.tree = etree.parse(document_xml_path)
        self.root = self.tree.getroot()
        self.body = self.root.find(qn('body'))

    def _next_tc_id(self):
        self.tc_id += 1
        return str(self.tc_id)

    def _next_comment_id(self):
        self.comment_id += 1
        return str(self.comment_id)

    def _is_in_del(self, elem):
        p = elem
        while p is not None:
            if p.tag == qn('del'):
                return True
            p = p.getparent()
        return False

    def _is_in_ins(self, elem):
        p = elem
        while p is not None:
            if p.tag == qn('ins'):
                return True
            p = p.getparent()
        return False

    def _get_visible_runs(self, para):
        runs = []
        for r in para.iter(qn('r')):
            if self._is_in_del(r):
                continue
            t = r.find(qn('t'))
            if t is not None and t.text:
                runs.append((r, t))
        return runs

    def find_replace(self, old_text, new_text, label=""):
        """Find old_text across w:t elements and replace with tracked change."""
        for para in self.body.iter(qn('p')):
            runs = self._get_visible_runs(para)
            if not runs:
                continue
            texts = [t.text for r, t in runs]
            concat = ''.join(texts)
            if old_text not in concat:
                continue

            idx = concat.index(old_text)
            end_idx = idx + len(old_text)

            pos = 0
            affected = []
            for ri, (r, t) in enumerate(runs):
                rs = pos
                re_ = pos + len(texts[ri])
                if re_ > idx and rs < end_idx:
                    s = max(0, idx - rs)
                    e = min(len(texts[ri]), end_idx - rs)
                    affected.append((r, t, ri, s, e))
                pos = re_
            if not affected:
                continue

            # If inside an INS block, modify in place
            any_ins = any(self._is_in_ins(r) for r, t, ri, s, e in affected)
            if any_ins:
                for r, t, ri, s, e in affected:
                    orig = t.text
                    t.text = orig[:s] + orig[e:]
                    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                if new_text:
                    ft = affected[0][1]
                    ft.text = (ft.text or "") + new_text
                    ft.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                print(f"  + {label} (INS)")
                return True

            first_before = texts[affected[0][2]][:affected[0][3]]
            last_after = texts[affected[-1][2]][affected[-1][4]:]
            rpr_e = affected[0][0].find(qn('rPr'))
            rpr = copy.deepcopy(rpr_e) if rpr_e is not None else None
            parent_elem = affected[0][0].getparent()
            insert_idx = list(parent_elem).index(affected[0][0])

            for r, t, ri, s, e in affected:
                rp = r.getparent()
                if rp is not None:
                    rp.remove(r)

            elems = []
            if first_before:
                br = etree.Element(qn('r'))
                if rpr is not None:
                    br.append(copy.deepcopy(rpr))
                bt = etree.SubElement(br, qn('t'))
                bt.text = first_before
                bt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                elems.append(br)

            de = etree.Element(qn('del'))
            de.set(qn('id'), self._next_tc_id())
            de.set(qn('author'), self.author)
            de.set(qn('date'), self.date)
            dr = etree.SubElement(de, qn('r'))
            if rpr is not None:
                dr.append(copy.deepcopy(rpr))
            dt = etree.SubElement(dr, qn('delText'))
            dt.text = old_text
            dt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            elems.append(de)

            if new_text:
                ie = etree.Element(qn('ins'))
                ie.set(qn('id'), self._next_tc_id())
                ie.set(qn('author'), self.author)
                ie.set(qn('date'), self.date)
                ir = etree.SubElement(ie, qn('r'))
                if rpr is not None:
                    ir.append(copy.deepcopy(rpr))
                it = etree.SubElement(ir, qn('t'))
                it.text = new_text
                it.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                elems.append(ie)

            if last_after:
                ar = etree.Element(qn('r'))
                if rpr is not None:
                    ar.append(copy.deepcopy(rpr))
                at = etree.SubElement(ar, qn('t'))
                at.text = last_after
                at.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                elems.append(ar)

            for i, elem in enumerate(elems):
                parent_elem.insert(insert_idx + i, elem)

            print(f"  + {label}")
            return True

        print(f"  - {label}: not found")
        return False

    def add_comment(self, search_text, comment_text):
        """Add a comment anchored to a paragraph containing search_text."""
        cid = self._next_comment_id()
        for para in self.body.iter(qn('p')):
            runs = self._get_visible_runs(para)
            if not runs:
                continue
            concat = ''.join(t.text for r, t in runs)
            if search_text not in concat:
                continue

            first_run = runs[0][0]
            parent = first_run.getparent()
            idx = list(parent).index(first_run)

            crs = etree.Element(qn('commentRangeStart'))
            crs.set(qn('id'), cid)
            parent.insert(idx, crs)

            last_run = runs[-1][0]
            last_idx = list(parent).index(last_run)

            cre = etree.Element(qn('commentRangeEnd'))
            cre.set(qn('id'), cid)
            parent.insert(last_idx + 1, cre)

            ref_run = etree.Element(qn('r'))
            rpr_ref = etree.SubElement(ref_run, qn('rPr'))
            rs = etree.SubElement(rpr_ref, qn('rStyle'))
            rs.set(qn('val'), 'CommentReference')
            cr = etree.SubElement(ref_run, qn('commentReference'))
            cr.set(qn('id'), cid)
            parent.insert(last_idx + 2, ref_run)

            self.comments_to_add.append((cid, comment_text))
            print(f"  + Comment {cid}: {comment_text[:60]}...")
            return cid

        print(f"  - Comment not placed: {search_text[:40]}...")
        return None

    def save(self):
        """Save document.xml using body-swap serialization."""
        body_xml = etree.tostring(self.body, encoding='unicode')
        body_start = self.original_xml.index('<w:body')
        body_end = self.original_xml.rindex('</w:body>') + len('</w:body>')
        result = self.original_xml[:body_start] + body_xml + self.original_xml[body_end:]
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Saved {self.path}")

    def save_comments(self, comments_xml_path):
        """Append comments to comments.xml."""
        if not self.comments_to_add:
            return

        with open(comments_xml_path, 'r', encoding='utf-8') as f:
            comments_xml = f.read()

        close_tag = '</w:comments>'
        insert_pos = comments_xml.rindex(close_tag)

        new_comments = ""
        for cid, text in self.comments_to_add:
            # Escape XML special characters in comment text
            escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            new_comments += (
                f'<w:comment w:id="{cid}" w:author="{self.author}" '
                f'w:date="{self.date}" w:initials="CA">'
                f'<w:p><w:pPr><w:pStyle w:val="CommentText"/></w:pPr>'
                f'<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>'
                f'<w:annotationRef/></w:r>'
                f'<w:r><w:t xml:space="preserve">{escaped}</w:t></w:r>'
                f'</w:p></w:comment>\n'
            )

        comments_xml = comments_xml[:insert_pos] + new_comments + comments_xml[insert_pos:]
        with open(comments_xml_path, 'w', encoding='utf-8') as f:
            f.write(comments_xml)
        print(f"Added {len(self.comments_to_add)} comments to {comments_xml_path}")

    def add_author_to_people(self, people_xml_path):
        """Add author to people.xml, detecting the correct namespace prefix."""
        with open(people_xml_path, 'r') as f:
            people = f.read()

        if self.author in people:
            print(f"{self.author} already in people.xml")
            return

        # Detect namespace prefix (w15: or w:)
        if 'w15:people' in people:
            prefix = 'w15'
            close_tag = '</w15:people>'
        elif 'w:people' in people:
            prefix = 'w'
            close_tag = '</w:people>'
        else:
            print("WARNING: Could not detect people.xml namespace prefix")
            return

        entry = (
            f'<{prefix}:person {prefix}:author="{self.author}">'
            f'<{prefix}:presenceInfo {prefix}:providerId="None" '
            f'{prefix}:userId="{self.author}"/>'
            f'</{prefix}:person>'
        )
        people = people.replace(close_tag, entry + close_tag)
        with open(people_xml_path, 'w') as f:
            f.write(people)
        print(f"Added {self.author} to people.xml (prefix: {prefix})")
