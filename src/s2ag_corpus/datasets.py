import json
from dataclasses import dataclass

from s2ag_corpus.sql import CREATE_PAPERS_TABLE_WITHOUT_KEYS, ADD_KEY_TO_PAPERS
from s2ag_corpus.sql import CREATE_CITATIONS_TABLE_WITHOUT_INDICES, ADD_KEYS_TO_CITATIONS


@dataclass(frozen=True)
class Dataset:
    table: str
    json_to_tuple: callable
    create_table: str
    add_indices: str


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


papers_dataset = Dataset(table="papers",
                         json_to_tuple=paper_json_to_tuple,
                         create_table= CREATE_PAPERS_TABLE_WITHOUT_KEYS,
                         add_indices=ADD_KEY_TO_PAPERS
                         )

citations_dataset = Dataset(table="citations",
                            json_to_tuple=citation_json_to_tuple,
                            create_table=CREATE_CITATIONS_TABLE_WITHOUT_INDICES,
                            add_indices=ADD_KEYS_TO_CITATIONS
                    )
DATASETS = {"papers" : papers_dataset,
            "citations" : citations_dataset}
