import re
from typing import List

import spacy
from spacy.tokens import Doc
from spacy.language import Language


def regex_patterns() -> List:
    """Define and compile regex patterns to capture citations."""
    patterns = [
        # Year of publication inside parentheses, with optional page numbers : https://regex101.com/r/vr4Adl/1
        r"\(\d{4},? ?s?\.? ?\d*-?\d*\)",

        # One or more names in parentheses, with the year of publication: https://regex101.com/r/Od7g55/2
        r"\(([A-ZØÆÅ][a-zæøå]+( ?\d+[,: ]*))+\)",

        # Explicit referencing of name and year, with optional Med eksplisitt henvisning (jf., se f.eks., sjå t.d.): https://regex101.com/r/z2CS6R/1
        r"\((jf\.|sjå også|se for eksempel|sjå t\.d\.) [A-ZØÆÅ][a-zæøå]+ \d+[\:s\.,]* ?\d+?\)",

        # Navn utenfor parentes, årstall inni: https://regex101.com/r/daYhiM/2
        r"([A-ZØÆÅ][a-zæøå]*,? [og& etal\.]*)+\((\d+[,:]? ?)+\)",

        # Alt inni parenteser
        r"\(.*?\)",
    ]
    return [re.compile(reg) for reg in patterns]


def match_regex_spans(text: str) -> list:
    """Apply all regex patterns on the texts, and only keep non-empty matches."""
    return [
        m.span()
        for regx in regex_patterns()
        for m in re.finditer(regx, text)
    ]


@Language.component("regex_span_finder")
def regex_span_finder(doc: Doc, spans_key: str = "regex") -> Doc:
    """Populate the doc.spans attribute with regex matches."""
    for (start, end) in match_regex_spans(doc.text):
        span= doc.char_span(start, end)
        if spans_key in doc.spans:
            doc.spans[spans_key] += (span,)
        else:
            doc.spans[spans_key] = (span,)
    return doc

