
# Ancient Greek BERT

*Note: The Morphological Analysis Tagger has issues loading on some machines and gives incorrect outputs due to an issue with the FLAIR Toolkit. If you run into this problem, please open an issue and we can try to help!*

<img src="https://ichef.bbci.co.uk/images/ic/832xn/p02m4gzb.jpg"/>

The first and only available Ancient Greek sub-word BERT model!

State-of-the-art post fine-tuning on Part-of-Speech Tagging and Morphological Analysis.

Pre-trained weights are made available for a standard 12 layer, 768d BERT-base model.

You can also use the model directly on the HuggingFace Model Hub [here](https://huggingface.co/pranaydeeps/Ancient-Greek-BERT).

Please refer to our paper titled: "A Pilot Study for BERT Language Modelling and Morphological Analysis for Ancient and Medieval Greek". In Proceedings of The 5th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature (LaTeCH-CLfL 2021).

## Installation & Setup

### 1. Python-Umgebung erstellen

```bash
git clone https://github.com/tioannidis/Ancient-Greek-BERT.git
cd Ancient-Greek-BERT
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Abhängigkeiten installieren

Alle Abhängigkeiten sind in `requirements.txt` hinterlegt und können mit einem Befehl installiert werden:

```bash
pip install -r requirements.txt
```

Alternativ einzeln:

```bash
pip install flair==0.15.1
pip install "transformers>=4.25.0,<5.0.0"
pip install torch==2.10.0
```

> **Hinweis:** `flair==0.15.1` benötigt `transformers<5.0.0`. `transformers>=5.0.0` ist **nicht** kompatibel. `huggingface_hub` wird automatisch in der richtigen Version mitinstalliert und darf nicht manuell auf `>=1.0` fixiert werden.

### 3. FLAIR-Patch anwenden

Einmalig ausführen, um den Namenskonflikt in der FLAIR-Bibliothek zu beheben:

```bash
python -c "
import site, os
p = os.path.join(site.getsitepackages()[0], 'flair/embeddings/transformer.py')
t = open(p).read()
open(p, 'w').write(t.replace('LayoutLMv2FeatureExtractor,', 'LayoutLMv2ImageProcessor as LayoutLMv2FeatureExtractor,'))
print('Patch erfolgreich.')
"
```

### 4. POS-Tagger-Modell herunterladen

Das Modell (`final-model.pt`, ~448 MB) ist nicht im Repository enthalten und muss manuell heruntergeladen werden, da es die GitHub-Dateigrößenbegrenzung überschreitet.

**Option A – Git LFS (empfohlen, falls verfügbar):**
```bash
brew install git-lfs  # macOS; Linux: sudo apt install git-lfs
git lfs install
git remote add upstream https://github.com/pranaydeeps/Ancient-Greek-BERT.git
git lfs fetch upstream
git lfs checkout
```

**Option B – Manuell:**
Lade `final-model.pt` und `best-model.pt` direkt aus dem [Original-Repository](https://github.com/pranaydeeps/Ancient-Greek-BERT) herunter und lege sie in den Ordner `SuperPeitho-FLAIR-v2/`.

### 5. BERT-Basismodell herunterladen

Das FLAIR-Modell benötigt intern das Ancient-Greek-BERT-Basismodell, das von HuggingFace geladen wird:

```bash
python -c "
from transformers import AutoTokenizer, AutoModel
path = '../LM/SuperPeitho-v1'
AutoTokenizer.from_pretrained('pranaydeeps/Ancient-Greek-BERT').save_pretrained(path)
AutoModel.from_pretrained('pranaydeeps/Ancient-Greek-BERT').save_pretrained(path)
print('Fertig.')
"
```

> Das Modell (~450 MB) wird unter `../LM/SuperPeitho-v1` (relativ zum Projektordner) gespeichert, da dieser Pfad beim Training fest eingebaut wurde.

### 6. Tagger testen

```bash
python test_tagger.py
```

Erwartete Ausgabe für `Γνῶθι σεαυτόν.`:

```
  ┌──────────┬───────────┬────────────────────────────────────┐
  │ Wort     │ Tag       │ Bedeutung                          │
  ├──────────┼───────────┼────────────────────────────────────┤
  │ Γνῶθι   │ v2saima-- │ Verb, 2. Person, Singular, Aorist, Imperativ, Aktiv │
  ├──────────┼───────────┼────────────────────────────────────┤
  │ σεαυτόν │ p-s---ma- │ Pronomen, Singular, Maskulin, Akkusativ │
  └──────────┴───────────┴────────────────────────────────────┘
```

---

## How to use (original)

Can be directly used from the HuggingFace Model Hub with:

```python
from transformers import AutoTokenizer, AutoModel
tokeniser = AutoTokenizer.from_pretrained("pranaydeeps/Ancient-Greek-BERT")
model = AutoModel.from_pretrained("pranaydeeps/Ancient-Greek-BERT")
```

## Fine-tuning for POS/Morphological Analysis

- **finetune_pos.py** can be used to finetune the BERT model for POS tagging on your own data. We provide sample files from the Gold standard treebanks, however the full treebanks can't be made available at this time. Please contact the authors for more details.
- Even though the full treebanks aren't made available, we provide a pre-trained POS Tagging model in the directory SuperPeitho-FLAIR-v2, which can directly be used for inference and has an accuracy of ~90 percent on the 3 treebanks available. You can import the pre-trained model in FLAIR with:

```python
from flair.models import SequenceTagger
tagger = SequenceTagger.load('SuperPeitho-FLAIR-v2/final-model.pt')
```

## Training data

The model was initialised from [AUEB NLP Group's Greek BERT](https://huggingface.co/nlpaueb/bert-base-greek-uncased-v1)
and subsequently trained on monolingual data from the First1KGreek Project, Perseus Digital Library, PROIEL Treebank and
Gorman's Treebank

## Training and Eval details

Standard de-accentuating and lower-casing for Greek as suggested in [AUEB NLP Group's Greek BERT](https://huggingface.co/nlpaueb/bert-base-greek-uncased-v1).
The model was trained on 4 NVIDIA Tesla V100 16GB GPUs for 80 epochs, with a max-seq-len of 512 and results in a perplexity of 4.8 on the held out test set.
It also gives state-of-the-art results when fine-tuned for PoS Tagging and Morphological Analysis on all 3 treebanks averaging >90% accuracy. Please consult our paper or contact [me](mailto:pranaydeep.singh@ugent.be) for further questions!

## Cite

If you end up using Ancient-Greek-BERT in your research, please cite the paper:

```
@inproceedings{ancient-greek-bert,
author = {Singh, Pranaydeep and Rutten, Gorik and Lefever, Els},
title = {A Pilot Study for BERT Language Modelling and Morphological Analysis for Ancient and Medieval Greek},
year = {2021},
booktitle = {The 5th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature (LaTeCH-CLfL 2021)}
}
```
