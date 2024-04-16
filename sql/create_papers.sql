create table if not exists public.papers
(
    corpusid int4  not null
        constraint papers_pk
            primary key,
    paper_json jsonb not null
);