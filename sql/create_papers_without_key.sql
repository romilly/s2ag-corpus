create table if not exists public.papers
(
    corpusid int4  not null,
    paper_json jsonb not null
);