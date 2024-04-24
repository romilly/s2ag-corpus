INSERT_PAPER_SQL = 'INSERT INTO papers(corpusid, paper_json) VALUES (%s, %s) on conflict(corpusid) do nothing'
INSERT_PAPER_IDS_SQL = 'INSERT INTO paperids(sha, corpusid, is_primary) VALUES (%s, %s, %s) on conflict do nothing'
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
CREATE_CITATIONS_TABLE_WITH_INDICES = """
create table public.citations (
  citationid bigint not null,
  citingcorpusid integer not null,
  citedcorpusid integer,
  isinfluential boolean
);
create index citations_citationid_index on citations using btree (citationid);
create index citations_citedcorpusid_index on citations using btree (citedcorpusid);
create index citations_citingcorpusid_index on citations using btree (citingcorpusid);
"""
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
CREATE_EXTENDED_CITATIONS_TABLE_WITHOUT_INDICES = """
create table public.citations (
  citationid bigint not null,
  citingcorpusid integer not null,
  citedcorpusid integer,
  isinfluential boolean,
  contexts text,
  intents text
);
"""