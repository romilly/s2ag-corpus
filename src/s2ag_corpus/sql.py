INSERT_PAPER_SQL = 'INSERT INTO papers(corpusid, paper_json) VALUES (%s, %s) on conflict(corpusid) do nothing'

INSERT_PAPER_IDS_SQL = 'INSERT INTO paperids(sha, corpusid, is_primary) VALUES (%s, %s, %s) on conflict do nothing'

CREATE_TABLE_TLDRS = """
CREATE TABLE IF NOT EXISTS tldrs
    (corpusid int4  not null, tldr_json jsonb not null)
"""

ADD_KEY_TO_TLDRS = """
alter table tldrs
    add constraint tldrs_pk
        primary key (corpusid);"""

CREATE_PAPERS_TABLE_WITH_KEYS = """
CREATE TABLE IF NOT EXISTS papers
    (corpusid int4  not null constraint papers_pk primary key, paper_json jsonb not null)
"""

CREATE_PAPERS_TABLE_WITHOUT_KEYS = """
CREATE TABLE IF NOT EXISTS papers
    (corpusid int4  not null, paper_json jsonb not null)
"""

ADD_KEY_TO_PAPERS = """
alter table papers
    add constraint papers_pk
        primary key (corpusid);"""

CREATE_EXTENDED_CITATIONS_TABLE_WITH_INDICES = """
create table public.citations (
  citationid bigint not null,
  citingcorpusid integer not null,
  citedcorpusid integer,
  isinfluential boolean,
  contexts text,
  intents text
);
create index citations_citationid_index on citations using btree (citationid);
create index citations_citedcorpusid_index on citations using btree (citedcorpusid);
create index citations_citingcorpusid_index on citations using btree (citingcorpusid);
"""

CREATE_CITATIONS_TABLE_WITHOUT_INDICES = """
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
create index citations_citationid_index
    on citations (citationid);

create index citations_citedcorpusid_index
    on citations (citedcorpusid);

create index citations_citingcorpusid_index
    on citations (citingcorpusid);
"""

CREATE_PAPER_IDS_TABLE = """
create table public.paperids (
    sha text not null,
    corpusid integer not null,
    is_primary boolean not null)
"""

ADD_KEYS_TO_PAPER_IDS = """
create index sha_index on public.paperids (sha);
create index corpus_index on public.paperids using btree(corpusid);
"""

CREATE_TABLE_ABSTRACTS = """
create table abstracts
(
    corpusid       integer not null,
    openaccessinfo jsonb   not null,
    abstract       text    not null
);
"""

ADD_KEYS_TO_ABSTRACTS = """
create index abstracts_idx on abstracts using btree(corpusid);
"""