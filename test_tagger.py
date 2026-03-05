# Test script for the pre-trained Ancient Greek POS tagger (SuperPeitho-FLAIR-v2)
# Requires: pip install flair
# Note: final-model.pt must be downloaded manually via Git LFS

from flair.models import SequenceTagger
from flair.data import Sentence

# Load the pre-trained POS tagger (~90% accuracy on Ancient Greek treebanks)
tagger = SequenceTagger.load('SuperPeitho-FLAIR-v2/final-model.pt')

# Example Ancient Greek sentence: "I release the horses"
sentence = Sentence("λύω τοὺς ἵππους")
tagger.predict(sentence)

# Print each token with its predicted POS tag
for token in sentence.tokens:
    print(token.text, token.get_tag('pos').value)
