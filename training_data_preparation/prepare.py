#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals, print_function

LABELS = ["ROLE", "GOAL", "ORG", "DOC"]

rawData = [
    dict(sentence="Руководитель это отсветственость", entities=[
        dict(phrase="Руководитель", label=0),
    ]),
    dict(sentence="Цель руководителя находить решения", entities=[
        dict(phrase="находить решения", label=1),
    ]),
]

def main(labels=LABELS, rawData=rawData):
    resultData = []
    for line in rawData:
        rawEntities = line['entities']
        resultEntities = []
        for entity in rawEntities:
            startPlace = line['sentence'].find(entity['phrase'])
            endPlace = startPlace + len(entity['phrase'])
            label = labels[entity['label']]
            resultEntities.append((startPlace, endPlace, label))
        resultLine = (
            line['sentence'],
            {"entities": resultEntities}
        )
        resultData.append(resultLine)
    print(resultData)
    return resultData

if __name__ == "__main__":
    main()