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


DATASETS = {"papers" : Dataset(table="papers", json_to_tuple = paper_json_to_tuple)}
