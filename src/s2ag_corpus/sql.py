CREATE_ABSTRACTS_TABLE = """
create table abstracts
(
    corpusid       integer not null,
    openaccessinfo jsonb   not null,
    abstract       text    not null
);
"""

ADD_KEYS_TO_ABSTRACTS = """
ALTER TABLE abstracts
ADD PRIMARY KEY (corpusid);
"""

UPSERT_ABSTRACTS = """
INSERT INTO abstracts (corpusid, openaccessinfo, abstract)
VALUES (%s, %s, %s)
ON CONFLICT (corpusid)
DO UPDATE SET openaccessinfo = EXCLUDED.openaccessinfo,
              abstract = EXCLUDED.abstract;
"""

CREATE_AUTHORS_TABLE = """
create table authors (
    authorid bigint not null,
    name text,
    author_json jsonb
);
"""

ADD_KEYS_TO_AUTHORS = """
alter table public.authors
    add constraint authors_pk
        primary key (authorid);;
create index name_idx on authors (name);
"""

UPSERT_AUTHORS = """
INSERT INTO authors (authorid, name, author_json)
VALUES (%s, %s, %s)
ON CONFLICT (authorid)
DO UPDATE SET name = EXCLUDED.name,
              author_json = EXCLUDED.author_json;
"""


CREATE_CITATIONS_TABLE = """
create table public.citations (
  citationid bigint not null,
  citingcorpusid integer not null,
  citedcorpusid integer,
  isinfluential boolean,
  contexts text,
  intents text
);
"""

ADD_KEYS_TO_CITATIONS = """
alter table citations
    add constraint citations_pk
        primary key (citationid);

create index citations_citedcorpusid_index
    on citations (citedcorpusid);

create index citations_citingcorpusid_index
    on citations (citingcorpusid);
"""

UPSERT_CITATIONS = """
INSERT INTO citations (citationid, citingcorpusid, citedcorpusid, isinfluential, contexts, intents)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (citationid)
DO UPDATE SET citingcorpusid = EXCLUDED.citingcorpusid,
              citedcorpusid = EXCLUDED.citedcorpusid,
              isinfluential = EXCLUDED.isinfluential,
              contexts = EXCLUDED.contexts,
              intents = EXCLUDED.intents;
"""

CREATE_PAPERS_TABLE = """
CREATE TABLE papers
    (corpusid int4  not null, paper_json jsonb not null)
"""

ADD_KEY_TO_PAPERS = """
alter table papers
    add constraint papers_pk
        primary key (corpusid);"""

UPSERT_PAPERS = """
INSERT INTO papers (corpusid, paper_json)
VALUES (%s, %s)
ON CONFLICT (corpusid)
DO UPDATE SET paper_json = EXCLUDED.paper_json;
"""


CREATE_PAPER_IDS_TABLE = """
create table public.paperids (
    sha text not null,
    corpusid integer not null,
    is_primary boolean not null)
"""

ADD_KEYS_TO_PAPER_IDS = """
alter table paperids
    add constraint paperids_pk
        primary key (sha);
create index corpus_index on paperids(corpusid);
"""

UPSERT_PAPER_IDS = """
INSERT INTO paperids (sha, corpusid, is_primary)
VALUES (%s, %s, %s)
ON CONFLICT (sha)
DO UPDATE SET corpusid = EXCLUDED.corpusid,
              is_primary = EXCLUDED.is_primary
"""

CREATE_PUBLICATION_VENUES_TABLE = """
CREATE TABLE publication_venues (
    id text not null,
    pv_json jsonb not null)
"""

ADD_KEY_TO_PUBLICATION_VENUES = """
alter table publication_venues
    add constraint pubv_pk
        primary key (id)
"""

UPSERT_PUBLICATION_VENUES = """
INSERT INTO publication_venues (id, pv_json)
VALUES (%s, %s)
ON CONFLICT (id)
DO UPDATE SET pv_json = EXCLUDED.pv_json;
"""


CREATE_TLDRS_TABLE = """
CREATE TABLE tldrs
    (corpusid int4  not null, tldr_json jsonb not null)
"""

ADD_KEY_TO_TLDRS = """
alter table tldrs
 add constraint tldrs_pk
    primary key (corpusid);
"""

UPSERT_TLDRS = """
INSERT INTO tldrs (corpusid, tldr_json)
VALUES (%s, %s)
ON CONFLICT (corpusid)
DO UPDATE SET tldr_json = EXCLUDED.tldr_json;
"""
