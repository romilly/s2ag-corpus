import json
from dataclasses import dataclass

from s2ag_corpus.sql import CREATE_PAPERS_TABLE_WITHOUT_KEYS, ADD_KEY_TO_PAPERS
from s2ag_corpus.sql import CREATE_CITATIONS_TABLE_WITHOUT_INDICES, ADD_KEYS_TO_CITATIONS
from s2ag_corpus.sql import CREATE_PAPER_IDS_TABLE_WITHOUT_KEYS, ADD_KEYS_TO_PAPER_IDS
from s2ag_corpus.sql import CREATE_TABLE_ABSTRACTS, ADD_KEYS_TO_ABSTRACTS
from s2ag_corpus.sql import CREATE_TABLE_TLDRS, ADD_KEY_TO_TLDRS


@dataclass(frozen=True)
class Dataset:
    table: str
    json_to_tuple: callable
    create_table: str
    add_indices: str


def tldrs_json_to_tuple(line):
    jd = json.loads(line)
    record = (jd['corpusid'], line)
    return record

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
              jd['intents']
            )

def paper_ids_json_to_tuple(line):
    jd = json.loads(line)
    return (
        jd['sha'],
        jd['corpusid'],
        jd['primary']
    )


def abstract_json_to_tuple(line):
    jd = json.loads(line)
    return jd['corpusid'], json.dumps(jd['openaccessinfo']),jd['abstract']

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

paper_ids_dataset = Dataset(table="paperids",
                            json_to_tuple= paper_ids_json_to_tuple,
                            create_table=CREATE_PAPER_IDS_TABLE_WITHOUT_KEYS,
                            add_indices=ADD_KEYS_TO_PAPER_IDS
                    )

abstracts_dataset = Dataset(table="abstracts",
                            json_to_tuple=abstract_json_to_tuple,
                            create_table=CREATE_TABLE_ABSTRACTS,
                            add_indices=ADD_KEYS_TO_ABSTRACTS)

tldrs_dataset = Dataset(table="tldrs",
                        json_to_tuple=tldrs_json_to_tuple,
                        create_table=CREATE_TABLE_TLDRS,
                        add_indices=ADD_KEY_TO_TLDRS)

DATASETS = {
    "abstracts": abstracts_dataset,
    "citations" : citations_dataset,
    "papers" : papers_dataset,
    "paper-ids" : paper_ids_dataset,
    "tldrs" : tldrs_dataset
}
