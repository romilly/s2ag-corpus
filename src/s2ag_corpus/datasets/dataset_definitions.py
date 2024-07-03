import json
from dataclasses import dataclass

from s2ag_corpus.database.sql import CREATE_ABSTRACTS_TABLE, ADD_KEYS_TO_ABSTRACTS, UPSERT_ABSTRACTS
from s2ag_corpus.database.sql import CREATE_AUTHORS_TABLE, ADD_KEYS_TO_AUTHORS, UPSERT_AUTHORS
from s2ag_corpus.database.sql import CREATE_CITATIONS_TABLE, ADD_KEYS_TO_CITATIONS, UPSERT_CITATIONS
from s2ag_corpus.database.sql import CREATE_PAPERS_TABLE, ADD_KEY_TO_PAPERS, UPSERT_PAPERS
from s2ag_corpus.database.sql import CREATE_PAPER_IDS_TABLE, ADD_KEYS_TO_PAPER_IDS, UPSERT_PAPER_IDS
from s2ag_corpus.database.sql import CREATE_PUBLICATION_VENUES_TABLE, ADD_KEY_TO_PUBLICATION_VENUES, UPSERT_PUBLICATION_VENUES
from s2ag_corpus.database.sql import CREATE_TLDRS_TABLE, ADD_KEY_TO_TLDRS, UPSERT_TLDRS


@dataclass(frozen=True)
class Dataset:
    table: str
    json_to_tuple: callable
    create_table: str
    add_indices: str
    upsert: str
    primary_key: str


    @property
    def delete_row(self) -> str:
        return f"DELETE FROM {self.table} where {self.primary_key} = (%s)"


def abstract_json_to_tuple(line):
    jd = json.loads(line)
    return jd['corpusid'], json.dumps(jd['openaccessinfo']), jd['abstract']


def authors_json_to_tuple(line):
    jd = json.loads(line)
    return jd['authorid'], jd['name'], line


def citation_json_to_tuple(line):
    jd = json.loads(line)
    return (jd['citationid'],
              jd['citingcorpusid'],
              jd['citedcorpusid'],
              jd['isinfluential'],
              json.dumps(jd['contexts']),
              json.dumps(jd['intents'])
            )


def paper_json_to_tuple(line):
    jd = json.loads(line)
    record = (jd['corpusid'], line)
    return record


def paper_ids_json_to_tuple(line):
    jd = json.loads(line)
    return (
        jd['sha'],
        jd['corpusid'],
        jd['primary']
    )


def pv_json_to_tuple(line):
    jd = json.loads(line)
    return jd['id'], line


def tldrs_json_to_tuple(line):
    jd = json.loads(line)
    record = (jd['corpusid'], line)
    return record


abstracts_dataset = Dataset(table="abstracts",
                            json_to_tuple=abstract_json_to_tuple,
                            create_table=CREATE_ABSTRACTS_TABLE,
                            add_indices=ADD_KEYS_TO_ABSTRACTS,
                            upsert=UPSERT_ABSTRACTS,
                            primary_key='corpusid'
                            )

authors_dataset = Dataset(table="authors",
                          json_to_tuple=authors_json_to_tuple,
                          create_table=CREATE_AUTHORS_TABLE,
                          add_indices=ADD_KEYS_TO_AUTHORS,
                          upsert=UPSERT_AUTHORS,
                          primary_key='authorid')

citations_dataset = Dataset(table="citations",
                            json_to_tuple=citation_json_to_tuple,
                            create_table=CREATE_CITATIONS_TABLE,
                            add_indices=ADD_KEYS_TO_CITATIONS,
                            upsert=UPSERT_CITATIONS,
                            primary_key='citationid')

papers_dataset = Dataset(table="papers",
                         json_to_tuple=paper_json_to_tuple,
                         create_table= CREATE_PAPERS_TABLE,
                         add_indices=ADD_KEY_TO_PAPERS,
                         upsert=UPSERT_PAPERS,
                         primary_key='corpusid')

paper_ids_dataset = Dataset(table="paperids",
                            json_to_tuple= paper_ids_json_to_tuple,
                            create_table=CREATE_PAPER_IDS_TABLE,
                            add_indices=ADD_KEYS_TO_PAPER_IDS,
                            upsert=UPSERT_PAPER_IDS,
                            primary_key='sha')

publication_venues_dataset = Dataset(table="publication_venues",
                                     json_to_tuple= pv_json_to_tuple,
                                     create_table=CREATE_PUBLICATION_VENUES_TABLE,
                                     add_indices=ADD_KEY_TO_PUBLICATION_VENUES,
                                     upsert=UPSERT_PUBLICATION_VENUES,
                                     primary_key='id')

tldrs_dataset = Dataset(table="tldrs",
                        json_to_tuple=tldrs_json_to_tuple,
                        create_table=CREATE_TLDRS_TABLE,
                        add_indices=ADD_KEY_TO_TLDRS,
                        upsert=UPSERT_TLDRS,
                        primary_key='corpusid')

DATASETS = {
    "abstracts": abstracts_dataset,
    "authors": authors_dataset,
    "citations" : citations_dataset,
    "papers" : papers_dataset,
    "paper-ids" : paper_ids_dataset,
    "publication-venues": publication_venues_dataset,
    "tldrs" : tldrs_dataset,
}
