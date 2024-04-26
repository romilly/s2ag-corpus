import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Dataset:
    table: str
    json_to_tuple: callable


def paper_json_to_tuple(line):
    jd = json.loads(line)
    record = (jd['corpusid'], line)
    return record


def citation_json_to_tuple(line):
    jd = json.loads(line)
    return (jd['citationid'],
              jd['citingcorpusid'],
              jd['citedcorpusid'],
              jd['isinfluential'],
              jd['contexts'],
              jd['intents'])


DATASETS = {"papers" : Dataset(table="papers", json_to_tuple = paper_json_to_tuple),
            "citations" : Dataset(table="citations", json_to_tuple = citation_json_to_tuple)}
