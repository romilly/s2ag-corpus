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