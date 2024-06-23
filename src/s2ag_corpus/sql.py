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

CREATE_PAPERS_TABLE = """
CREATE TABLE papers
    (corpusid int4  not null, paper_json jsonb not null)
"""

ADD_KEY_TO_PAPERS = """
alter table papers
    add constraint papers_pk
        primary key (corpusid);"""

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

CREATE_TLDRS_TABLE = """
CREATE TABLE tldrs
    (corpusid int4  not null, tldr_json jsonb not null)
"""

ADD_KEY_TO_TLDRS = """
alter table tldrs
 add constraint tldrs_pk
    primary key (corpusid);
"""
