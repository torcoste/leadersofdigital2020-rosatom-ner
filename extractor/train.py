#!/usr/bin/env python
# coding: utf8
"""
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities
Compatible with: spaCy v2.1.0+
Last tested with: v2.2.4
"""
from __future__ import unicode_literals, print_function

import plac
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

LABEL1 = "ЖИВОТНОЕ"
TRAIN_DATA1 = [
    (
        "Лошади такие высокие",
        {"entities": [(0, 6, LABEL1)]},
    ),
    ("Do they bite?", {"entities": []}),
    (
        "лошади такие высокие",
        {"entities": [(0, 6, LABEL1)]},
    ),
    ("лошади никогда не предают", {"entities": [(0, 6, LABEL1)]}),
    (
        "ох уж эти лошади",
        {"entities": [(10, 16, LABEL1)]},
    ),
    ("лошади?", {"entities": [(0, 6, LABEL1)]}),
]

LABEL2 = "РЕКА"
TRAIN_DATA2 = [
    (
        "Обь течет во мне",
        {"entities": [(0, 3, LABEL2)]},
    ),
    ("Do they bite?", {"entities": []}),
    (
        "обь течет во мне",
        {"entities": [(0, 3, LABEL2)]},
    ),
    ("обь или не обь", {"entities": [(0, 3, LABEL2), (11, 14, LABEL2)]}),
    (
        "ох уж эта обь",
        {"entities": [(10, 13, LABEL2)]},
    ),
    ("обь!", {"entities": [(0, 3, LABEL2)]}),
]


TRAIN_DATA = [{
    'data': TRAIN_DATA1,
    'label': LABEL1
},{
    'data': TRAIN_DATA2,
    'label': LABEL2
},]

@plac.annotations(
    model=("Model name. Defaults to blank 'ru' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, new_model_name="rosatom-docs", output_dir='./model', n_iter=30):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    random.seed(0)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("ru")  # create blank Language class
        print("Created blank 'ru' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    for train_data in TRAIN_DATA:
        print("Train data '%s'" % train_data['label'])
        ner.add_label(train_data['label'])  # add new entity label to entity recognizer
        if model is None:
            optimizer = nlp.begin_training()
        else:
            optimizer = nlp.resume_training()
        move_names = list(ner.move_names)
        # get names of other pipes to disable them during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
        # only train NER
        with nlp.disable_pipes(*other_pipes) and warnings.catch_warnings():
            # show warnings for misaligned entity spans once
            warnings.filterwarnings("once", category=UserWarning, module='spacy')

            sizes = compounding(1.0, 4.0, 1.001)
            # batch up the examples using spaCy's minibatch
            for itn in range(n_iter):
                random.shuffle(train_data['data'])
                batches = minibatch(train_data['data'], size=sizes)
                losses = {}
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
                print("Losses", losses)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta["name"] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)


if __name__ == "__main__":
    plac.call(main)