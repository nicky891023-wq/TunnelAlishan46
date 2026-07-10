#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tracked.py -- helpers to write Word TRACKED CHANGES (w:ins / w:del revisions) into a .docx
via python-docx's underlying lxml, since python-docx has no native revision support.

  * tracked_replace_par(par, old, new)  -- inline delete(old)+insert(new), preserving run rPr
  * insert_paragraphs_after(ref, items) -- add fully-inserted paragraphs (mark + content tracked)
Every revision carries w:id / w:author / w:date so Word shows author + timestamp.
"""
import copy
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

AUTHOR = "Claude (Ch5 批改)"
DATE   = "2026-07-09T12:00:00Z"
_rid = [9000]


def _next_id():
    _rid[0] += 1
    return str(_rid[0])


def _run(text, rpr=None, deltext=False):
    r = OxmlElement('w:r')
    if rpr is not None:
        r.append(copy.deepcopy(rpr))
    t = OxmlElement('w:delText' if deltext else 'w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = text
    r.append(t)
    return r


def _revwrap(tag, author, date):
    el = OxmlElement(tag)
    el.set(qn('w:id'), _next_id())
    el.set(qn('w:author'), author)
    el.set(qn('w:date'), date)
    return el


def make_ins(text, rpr=None, author=AUTHOR, date=DATE):
    ins = _revwrap('w:ins', author, date)
    ins.append(_run(text, rpr))
    return ins


def make_del(text, rpr=None, author=AUTHOR, date=DATE):
    d = _revwrap('w:del', author, date)
    d.append(_run(text, rpr, deltext=True))
    return d


def tracked_replace_par(par, old, new, author=AUTHOR, date=DATE):
    """Inline tracked replace of every `old` -> `new` inside a paragraph's runs.
    Handles the term contained within a single run (the common case for these compound
    terms); returns the number of replacements made."""
    n = 0
    for run in list(par.runs):
        if old not in run.text:
            continue
        rpr = run._r.find(qn('w:rPr'))
        parts = run.text.split(old)
        r_el = run._r
        parent = r_el.getparent()
        at = list(parent).index(r_el)
        parent.remove(r_el)
        nodes = []
        for i, seg in enumerate(parts):
            if seg:
                nodes.append(_run(seg, rpr))       # untouched text -> plain run
            if i < len(parts) - 1:
                nodes.append(make_del(old, rpr, author, date))
                nodes.append(make_ins(new, rpr, author, date))
                n += 1
        for j, node in enumerate(nodes):
            parent.insert(at + j, node)
    return n


def tracked_replace_par_terms(par, terms, author=AUTHOR, date=DATE):
    """Tracked replace of MANY terms in one paragraph in a single rebuild, robust to terms
    that span multiple runs (Chinese runs are split by proofing markers / per-glyph runs).
    `terms` = ordered list of (old, new); earlier (more specific) terms win on overlap.
    Works on the paragraph's concatenated run text; preserves each source run's formatting
    for untouched text, wraps each matched original term in <w:del> and its replacement in
    <w:ins>, and keeps surrounding bookmarks/pPr in place. Returns {old: count}."""
    runs = par.runs
    if not runs:
        return {}
    text = ''.join(r.text for r in runs)
    if not any(old in text for old, _ in terms):
        return {}
    p = par._p
    for pe in list(p.findall(qn('w:proofErr'))):      # drop proofing markers (Word regenerates)
        p.remove(pe)
    runs = par.runs
    text = ''.join(r.text for r in runs)
    idxmap = []
    rpr_list = [r._r.find(qn('w:rPr')) for r in runs]
    for ri, r in enumerate(runs):
        idxmap.extend([ri] * len(r.text))
    claimed = [False] * len(text)
    matches = []
    for old, new in terms:
        st = 0
        while True:
            k = text.find(old, st)
            if k == -1:
                break
            if not any(claimed[k:k + len(old)]):
                for m in range(k, k + len(old)):
                    claimed[m] = True
                matches.append((k, k + len(old), new, old))
            st = k + len(old)
    if not matches:
        return {}
    matches.sort()
    first = runs[0]._r
    anchor = first.getprevious()
    parent = first.getparent()
    for r in runs:
        parent.remove(r._r)
    nodes = []

    def emit_plain(a, b):
        j = a
        while j < b:
            ri = idxmap[j]; k = j
            while k < b and idxmap[k] == ri:
                k += 1
            nodes.append(_run(text[j:k], rpr_list[ri]))
            j = k

    cur = 0; counts = {}
    for a, b, new, old in matches:
        emit_plain(cur, a)
        rpr = rpr_list[idxmap[a]]
        nodes.append(make_del(text[a:b], rpr, author, date))
        nodes.append(make_ins(new, rpr, author, date))
        counts[old] = counts.get(old, 0) + 1
        cur = b
    emit_plain(cur, len(text))
    if anchor is None:
        for j, node in enumerate(nodes):
            parent.insert(j, node)
    else:
        ref = anchor
        for node in nodes:
            ref.addnext(node); ref = node
    return counts


def append_ins_to_par(par, text, author=AUTHOR, date=DATE):
    """Append a tracked-inserted run to the END of an existing paragraph's content
    (an inline sentence insertion). Inherits the last run's rPr for formatting."""
    rpr = par.runs[-1]._r.find(qn('w:rPr')) if par.runs else None
    par._p.append(make_ins(text, rpr, author, date))
    return par


def insert_paragraphs_after(ref_par, items, author=AUTHOR, date=DATE):
    """Insert fully-tracked (inserted) paragraphs after ref_par.
    items = list of (style_obj_or_None, text). Both the paragraph mark and its content are
    wrapped as insertions so Word shows the whole added paragraph as a tracked insertion.
    Returns the last inserted Paragraph (to chain further inserts)."""
    cursor = ref_par
    for style, text in items:
        new_p = OxmlElement('w:p')
        cursor._p.addnext(new_p)
        par = Paragraph(new_p, ref_par._parent)
        if style is not None:
            par.style = style
        pPr = par._p.get_or_add_pPr()
        rPr = pPr.find(qn('w:rPr'))
        if rPr is None:
            rPr = OxmlElement('w:rPr')
            pPr.append(rPr)
        rPr.append(_revwrap('w:ins', author, date))   # mark the paragraph glyph as inserted
        par._p.append(make_ins(text, None, author, date))
        cursor = par
    return cursor
