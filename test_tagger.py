# Test script for the pre-trained Ancient Greek POS tagger (SuperPeitho-FLAIR-v2)
# Requires: pip install flair
# Note: final-model.pt must be downloaded manually via Git LFS

from flair.models import SequenceTagger
from flair.data import Sentence

# Load the pre-trained POS tagger (~90% accuracy on Ancient Greek treebanks)
tagger = SequenceTagger.load('SuperPeitho-FLAIR-v2/final-model.pt')

# Fix compatibility issue: old flair stored OCR flags that are not needed for BERT
for emb in tagger.embeddings.embeddings:
    if hasattr(emb, 'needs_manual_ocr'):
        emb.needs_manual_ocr = False
    if hasattr(emb, 'tokenizer_needs_ocr_boxes'):
        emb.tokenizer_needs_ocr_boxes = False

# Example Ancient Greek sentence: "I release the horses"
sentence = Sentence("Γνῶθι σεαυτόν.")
tagger.predict(sentence)

POS = {'n': 'Nomen', 'v': 'Verb', 'a': 'Adjektiv', 'd': 'Adverb', 'l': 'Artikel',
       'g': 'Partikel', 'c': 'Konjunktion', 'r': 'Präposition', 'p': 'Pronomen',
       'm': 'Numeral', 'i': 'Interjektion', 'u': 'Satzzeichen'}
PERSON = {'1': '1. Person', '2': '2. Person', '3': '3. Person'}
NUMBER = {'s': 'Singular', 'p': 'Plural', 'd': 'Dual'}
TENSE  = {'p': 'Präsens', 'i': 'Imperfekt', 'r': 'Perfekt', 'l': 'Plusquamperfekt',
           'f': 'Futur', 'a': 'Aorist', 't': 'Futur II'}
MOOD   = {'i': 'Indikativ', 's': 'Konjunktiv', 'o': 'Optativ',
           'n': 'Infinitiv', 'm': 'Imperativ', 'p': 'Partizip'}
VOICE  = {'a': 'Aktiv', 'p': 'Passiv', 'm': 'Medium', 'e': 'Medio-Passiv'}
GENDER = {'m': 'Maskulin', 'f': 'Feminin', 'n': 'Neutrum'}
CASE   = {'n': 'Nominativ', 'g': 'Genitiv', 'd': 'Dativ', 'a': 'Akkusativ', 'v': 'Vokativ'}
DEGREE = {'c': 'Komparativ', 's': 'Superlativ'}

def decode_tag(tag):
    if len(tag) < 9:
        return ''
    p = list(tag)
    parts = []
    if p[0] != '-': parts.append(POS.get(p[0], p[0]))
    if p[1] != '-': parts.append(PERSON.get(p[1], p[1]))
    if p[2] != '-': parts.append(NUMBER.get(p[2], p[2]))
    if p[3] != '-': parts.append(TENSE.get(p[3], p[3]))
    if p[4] != '-': parts.append(MOOD.get(p[4], p[4]))
    if p[5] != '-': parts.append(VOICE.get(p[5], p[5]))
    if p[6] != '-': parts.append(GENDER.get(p[6], p[6]))
    if p[7] != '-': parts.append(CASE.get(p[7], p[7]))
    if p[8] != '-': parts.append(DEGREE.get(p[8], p[8]))
    return ', '.join(parts)

def print_table(rows):
    w1 = max(len(r[0]) for r in rows)
    w2 = max(len(r[1]) for r in rows)
    w3 = max(len(r[2]) for r in rows)
    w1 = max(w1, 4)  # min header width
    w2 = max(w2, 3)
    w3 = max(w3, 8)

    def row(a, b, c, l='│', m='│', r='│'):
        return f"  {l} {a:<{w1}} {m} {b:<{w2}} {m} {c:<{w3}} {r}"

    sep = lambda l, m, r: f"  {l}{'─'*(w1+2)}{m}{'─'*(w2+2)}{m}{'─'*(w3+2)}{r}"

    print(sep('┌', '┬', '┐'))
    print(row('Wort', 'Tag', 'Bedeutung'))
    print(sep('├', '┼', '┤'))
    for i, (a, b, c) in enumerate(rows):
        print(row(a, b, c))
        if i < len(rows) - 1:
            print(sep('├', '┼', '┤'))
    print(sep('└', '┴', '┘'))

# Collect results and print as table
rows = [(t.text, t.get_label('pos').value, decode_tag(t.get_label('pos').value))
        for t in sentence.tokens]
print_table(rows)
